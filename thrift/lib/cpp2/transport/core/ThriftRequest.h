/*
 * Copyright 2017-present Facebook, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#pragma once

#include <stdint.h>

#include <atomic>
#include <chrono>
#include <memory>
#include <string>
#include <utility>

#include <glog/logging.h>

#include <folly/io/IOBuf.h>
#include <thrift/lib/cpp/TApplicationException.h>
#include <thrift/lib/cpp/protocol/TProtocolException.h>
#include <thrift/lib/cpp/protocol/TProtocolTypes.h>
#include <thrift/lib/cpp/transport/THeader.h>
#include <thrift/lib/cpp2/async/ResponseChannel.h>
#include <thrift/lib/cpp2/protocol/Serializer.h>
#include <thrift/lib/cpp2/server/Cpp2ConnContext.h>
#include <thrift/lib/cpp2/server/ServerConfigs.h>
#include <thrift/lib/cpp2/transport/core/ThriftChannelIf.h>
#include <thrift/lib/thrift/gen-cpp2/RpcMetadata_types.h>

namespace apache {
namespace thrift {

/**
 * Manages per-RPC state.  There is one of these objects for each RPC.
 *
 * TODO: RSocket currently has a dependency to this class. We may want
 * to clean up our APIs to avoid the dependency to a ResponseChannel
 * object.
 */
class ThriftRequestCore : public ResponseChannelRequest {
 public:
  ThriftRequestCore(
      const apache::thrift::server::ServerConfigs& serverConfigs,
      std::unique_ptr<RequestRpcMetadata> metadata,
      std::unique_ptr<Cpp2ConnContext> connContext)
      : ThriftRequestCore(
            serverConfigs,
            std::move(metadata),
            std::shared_ptr<Cpp2ConnContext>(std::move(connContext))) {}

  ThriftRequestCore(
      const apache::thrift::server::ServerConfigs& serverConfigs,
      std::unique_ptr<RequestRpcMetadata> metadata,
      std::shared_ptr<Cpp2ConnContext> connContext)
      : serverConfigs_(serverConfigs),
        name_(std::move(metadata)->name_ref().value_or({})),
        kind_(metadata->kind_ref().value_or(
            RpcKind::SINGLE_REQUEST_SINGLE_RESPONSE)),
        seqId_(metadata->seqId_ref().value_or(0)),
        active_(true),
        connContext_(
            connContext ? std::move(connContext)
                        : std::make_shared<Cpp2ConnContext>()),
        reqContext_(connContext_.get(), &header_),
        queueTimeout_(serverConfigs_),
        taskTimeout_(serverConfigs_) {
    // Note that method name, RPC kind, and serialization protocol are validated
    // outside the ThriftRequestCore constructor.
    header_.setProtocolId(static_cast<int16_t>(
        metadata->protocol_ref().value_or(ProtocolId::BINARY)));
    header_.setSequenceNumber(seqId_);

    if (auto clientTimeoutMs = metadata->clientTimeoutMs_ref()) {
      clientTimeout_ = std::chrono::milliseconds(*clientTimeoutMs);
      header_.setClientTimeout(clientTimeout_);
    }
    if (auto queueTimeoutMs = metadata->queueTimeoutMs_ref()) {
      clientQueueTimeout_ = std::chrono::milliseconds(*queueTimeoutMs);
      header_.setClientQueueTimeout(clientQueueTimeout_);
    }
    if (auto priority = metadata->priority_ref()) {
      header_.setCallPriority(static_cast<concurrency::PRIORITY>(*priority));
    }
    if (auto otherMetadata = metadata->otherMetadata_ref()) {
      header_.setReadHeaders(std::move(*otherMetadata));
    }

    reqContext_.setMessageBeginSize(0);
    reqContext_.setMethodName(name_);
    reqContext_.setProtoSeqId(seqId_);

    if (auto observer = serverConfigs_.getObserver()) {
      observer->receivedRequest();
    }
  }

  ~ThriftRequestCore() override {
    cancelTimeout();
  }

  bool isActive() const final {
    return active_.load();
  }

  void cancel() override {
    if (active_.exchange(false)) {
      cancelTimeout();
    }
  }

  bool isOneway() const final {
    return kind_ == RpcKind::SINGLE_REQUEST_NO_RESPONSE ||
        kind_ == RpcKind::STREAMING_REQUEST_NO_RESPONSE;
  }

  protocol::PROTOCOL_TYPES getProtoId() const {
    return static_cast<protocol::PROTOCOL_TYPES>(header_.getProtocolId());
  }

  Cpp2RequestContext* getRequestContext() {
    return &reqContext_;
  }

  const std::string& getMethodName() const {
    return name_;
  }

  void sendReply(
      std::unique_ptr<folly::IOBuf>&& buf,
      apache::thrift::MessageChannel::SendCallback* cb = nullptr) final {
    if (active_.exchange(false)) {
      cancelTimeout();
      sendReplyInternal(std::move(buf), cb);

      auto observer = serverConfigs_.getObserver();
      if (observer) {
        observer->sentReply();
      }
    }
  }

  void sendStreamReply(
      ResponseAndSemiStream<
          std::unique_ptr<folly::IOBuf>,
          std::unique_ptr<folly::IOBuf>>&& result,
      MessageChannel::SendCallback* cb) final {
    if (active_.exchange(false)) {
      cancelTimeout();
      sendReplyInternal(
          std::move(result.response), std::move(result.stream), cb);

      auto observer = serverConfigs_.getObserver();
      if (observer) {
        observer->sentReply();
      }
    }
  }

  void sendErrorWrapped(
      folly::exception_wrapper ew,
      std::string exCode,
      apache::thrift::MessageChannel::SendCallback* cb = nullptr) final {
    if (active_.exchange(false)) {
      cancelTimeout();
      sendErrorWrappedInternal(std::move(ew), exCode, cb);
    }
  }

 protected:
  virtual void sendThriftResponse(
      std::unique_ptr<ResponseRpcMetadata> metadata,
      std::unique_ptr<folly::IOBuf> response) noexcept = 0;

  virtual void sendStreamThriftResponse(
      std::unique_ptr<ResponseRpcMetadata> metadata,
      std::unique_ptr<folly::IOBuf> response,
      apache::thrift::SemiStream<std::unique_ptr<folly::IOBuf>>
          stream) noexcept = 0;

  virtual folly::EventBase* getEventBase() noexcept = 0;

  void scheduleTimeouts() {
    queueTimeout_.request_ = this;
    taskTimeout_.request_ = this;
    std::chrono::milliseconds queueTimeout;
    std::chrono::milliseconds taskTimeout;
    auto differentTimeouts = serverConfigs_.getTaskExpireTimeForRequest(
        clientQueueTimeout_, clientTimeout_, queueTimeout, taskTimeout);

    auto reqContext = getRequestContext();
    reqContext->setRequestTimeout(taskTimeout);

    if (differentTimeouts) {
      if (queueTimeout > std::chrono::milliseconds(0)) {
        getEventBase()->timer().scheduleTimeout(&queueTimeout_, queueTimeout);
      }
    }
    if (taskTimeout > std::chrono::milliseconds(0)) {
      getEventBase()->timer().scheduleTimeout(&taskTimeout_, taskTimeout);
    }
  }

 private:
  void sendReplyInternal(
      std::unique_ptr<folly::IOBuf> buf,
      apache::thrift::MessageChannel::SendCallback* cb = nullptr) {
    if (checkResponseSize(*buf)) {
      sendThriftResponse(createMetadata(), std::move(buf));
    } else {
      sendResponseTooBigEx(cb);
    }
  }

  void sendReplyInternal(
      std::unique_ptr<folly::IOBuf> buf,
      apache::thrift::SemiStream<std::unique_ptr<folly::IOBuf>> stream,
      apache::thrift::MessageChannel::SendCallback* cb = nullptr) {
    if (checkResponseSize(*buf)) {
      sendStreamThriftResponse(
          createMetadata(), std::move(buf), std::move(stream));
    } else {
      sendResponseTooBigEx(cb);
    }
  }

  void sendResponseTooBigEx(apache::thrift::MessageChannel::SendCallback* cb) {
    sendErrorWrappedInternal(
        folly::make_exception_wrapper<TApplicationException>(
            TApplicationException::TApplicationExceptionType::INTERNAL_ERROR,
            "Response size too big"),
        kResponseTooBigErrorCode,
        cb);
  }

  std::unique_ptr<ResponseRpcMetadata> createMetadata() {
    auto metadata = std::make_unique<ResponseRpcMetadata>();
    metadata->seqId_ref() = seqId_;
    auto writeHeaders = header_.releaseWriteHeaders();
    if (auto* eh = header_.getExtraWriteHeaders()) {
      writeHeaders.insert(eh->begin(), eh->end());
    }
    if (!writeHeaders.empty()) {
      metadata->otherMetadata_ref() = std::move(writeHeaders);
    }
    return metadata;
  }

  void sendErrorWrappedInternal(
      folly::exception_wrapper ew,
      const std::string& exCode,
      apache::thrift::MessageChannel::SendCallback* /*cb*/) {
    DCHECK(ew.is_compatible_with<TApplicationException>());
    header_.setHeader("ex", exCode);
    ew.with_exception([&](TApplicationException& tae) {
      std::unique_ptr<folly::IOBuf> exbuf;
      auto proto = header_.getProtocolId();
      try {
        exbuf = serializeError(proto, tae, name_, seqId_);
      } catch (const protocol::TProtocolException& pe) {
        // Should never happen.  Log an error and return an empty
        // payload.
        LOG(ERROR) << "serializeError failed. type=" << pe.getType()
                   << " what()=" << pe.what();
      }

      if (tae.getType() ==
              TApplicationException::TApplicationExceptionType::UNKNOWN &&
          !checkResponseSize(*exbuf)) {
        sendResponseTooBigEx(nullptr);
        return;
      }

      switch (kind_) {
        case RpcKind::SINGLE_REQUEST_SINGLE_RESPONSE:
        case RpcKind::STREAMING_REQUEST_SINGLE_RESPONSE:
          sendThriftResponse(createMetadata(), std::move(exbuf));
          break;
        case RpcKind::SINGLE_REQUEST_STREAMING_RESPONSE:
        case RpcKind::STREAMING_REQUEST_STREAMING_RESPONSE:
          sendStreamThriftResponse(createMetadata(), std::move(exbuf), {});
          break;
        default: // Don't send error back for one-way.
          break;
      }
    });
  }

  void cancelTimeout() {
    queueTimeout_.canceled_ = true;
    taskTimeout_.canceled_ = true;
    if (queueTimeout_.isScheduled()) {
      queueTimeout_.cancelTimeout();
    }
    if (taskTimeout_.isScheduled()) {
      taskTimeout_.cancelTimeout();
    }
  }

  bool checkResponseSize(const folly::IOBuf& buf) {
    auto maxResponseSize = serverConfigs_.getMaxResponseSize();
    return maxResponseSize == 0 ||
        buf.computeChainDataLength() <= maxResponseSize;
  }

  class QueueTimeout : public folly::HHWheelTimer::Callback {
    ThriftRequestCore* request_;
    bool canceled_{false};
    const apache::thrift::server::ServerConfigs& serverConfigs_;
    QueueTimeout(const apache::thrift::server::ServerConfigs& serverConfigs)
        : serverConfigs_(serverConfigs) {}
    void timeoutExpired() noexcept override {
      if (!canceled_ && !request_->reqContext_.getStartedProcessing() &&
          request_->active_.exchange(false) && !request_->isOneway()) {
        const auto& observer = serverConfigs_.getObserver();
        if (observer) {
          observer->queueTimeout();
        }
        request_->sendErrorWrappedInternal(
            TApplicationException(
                TApplicationException::TApplicationExceptionType::TIMEOUT,
                "Queue Timeout"),
            kTaskExpiredErrorCode,
            nullptr);
      }
    }
    friend class ThriftRequestCore;
  };
  class TaskTimeout : public folly::HHWheelTimer::Callback {
    ThriftRequestCore* request_;
    bool canceled_{false};
    const apache::thrift::server::ServerConfigs& serverConfigs_;
    TaskTimeout(const apache::thrift::server::ServerConfigs& serverConfigs)
        : serverConfigs_(serverConfigs) {}
    void timeoutExpired() noexcept override {
      if (!canceled_ && request_->active_.exchange(false) &&
          !request_->isOneway()) {
        const auto& observer = serverConfigs_.getObserver();
        if (observer) {
          observer->taskTimeout();
        }
        request_->sendErrorWrappedInternal(
            TApplicationException(
                TApplicationException::TApplicationExceptionType::TIMEOUT,
                "Task expired"),
            kTaskExpiredErrorCode,
            nullptr);
      }
    }
    friend class ThriftRequestCore;
  };
  friend class QueueTimeout;
  friend class TaskTimeout;
  friend class ThriftProcessor;

 protected:
  const apache::thrift::server::ServerConfigs& serverConfigs_;

 private:
  const std::string name_;
  const RpcKind kind_;
  const int32_t seqId_;
  std::atomic<bool> active_;
  transport::THeader header_;
  std::shared_ptr<Cpp2ConnContext> connContext_;
  Cpp2RequestContext reqContext_;

  QueueTimeout queueTimeout_;
  TaskTimeout taskTimeout_;
  std::chrono::milliseconds clientQueueTimeout_{0};
  std::chrono::milliseconds clientTimeout_{0};
};

class ThriftRequest final : public ThriftRequestCore {
 public:
  ThriftRequest(
      const apache::thrift::server::ServerConfigs& serverConfigs,
      std::shared_ptr<ThriftChannelIf> channel,
      std::unique_ptr<RequestRpcMetadata> metadata,
      std::unique_ptr<Cpp2ConnContext> connContext)
      : ThriftRequestCore(
            serverConfigs,
            std::move(metadata),
            std::move(connContext)),
        channel_(std::move(channel)) {
    scheduleTimeouts();
  }

 private:
  void sendThriftResponse(
      std::unique_ptr<ResponseRpcMetadata> metadata,
      std::unique_ptr<folly::IOBuf> response) noexcept override {
    channel_->sendThriftResponse(std::move(metadata), std::move(response));
  }

  void sendStreamThriftResponse(
      std::unique_ptr<ResponseRpcMetadata> metadata,
      std::unique_ptr<folly::IOBuf> response,
      apache::thrift::SemiStream<std::unique_ptr<folly::IOBuf>>
          stream) noexcept override {
    channel_->sendStreamThriftResponse(
        std::move(metadata), std::move(response), std::move(stream));
  }

  folly::EventBase* getEventBase() noexcept override {
    return channel_->getEventBase();
  }

 private:
  std::shared_ptr<ThriftChannelIf> channel_;
};

} // namespace thrift
} // namespace apache
