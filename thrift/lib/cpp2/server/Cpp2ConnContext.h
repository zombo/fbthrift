/*
 * Copyright 2014-present Facebook, Inc.
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
#ifndef THRIFT_ASYNC_CPP2CONNCONTEXT_H_
#define THRIFT_ASYNC_CPP2CONNCONTEXT_H_ 1

#include <memory>

#include <folly/SocketAddress.h>
#include <thrift/lib/cpp/async/TAsyncTransport.h>
#include <thrift/lib/cpp/concurrency/ThreadManager.h>
#include <thrift/lib/cpp/server/TConnectionContext.h>
#include <thrift/lib/cpp/transport/THeader.h>
#include <wangle/ssl/SSLUtil.h>

using apache::thrift::concurrency::PriorityThreadManager;

namespace apache {
namespace thrift {

using ClientIdentityHook = std::function<std::unique_ptr<void, void (*)(void*)>(
    const folly::AsyncTransportWrapper* transport,
    X509* cert,
    const folly::SocketAddress& peerAddress)>;

class RequestChannel;
class TClientBase;

class Cpp2ConnContext : public apache::thrift::server::TConnectionContext {
 public:
  explicit Cpp2ConnContext(
      const folly::SocketAddress* address = nullptr,
      const folly::AsyncTransportWrapper* transport = nullptr,
      folly::EventBaseManager* manager = nullptr,
      const std::shared_ptr<RequestChannel>& duplexChannel = nullptr,
      const std::shared_ptr<X509> peerCert = nullptr /*overridden from socket*/,
      apache::thrift::ClientIdentityHook clientIdentityHook = nullptr)
      : userData_(nullptr, no_op_destructor),
        manager_(manager),
        duplexChannel_(duplexChannel),
        peerCert_(peerCert),
        peerIdentities_(nullptr, [](void*) {}),
        transport_(transport) {
    if (address) {
      peerAddress_ = *address;
    }
    if (transport) {
      transport->getLocalAddress(&localAddress_);
      peerCert_ = transport->getPeerCert();
      securityProtocol_ = transport->getSecurityProtocol();
    }

    if (clientIdentityHook) {
      peerIdentities_ =
          clientIdentityHook(transport_, peerCert_.get(), peerAddress_);
    }
  }

  void reset() {
    peerAddress_.reset();
    localAddress_.reset();
    userData_.reset();
  }

  const folly::SocketAddress* getPeerAddress() const final {
    return &peerAddress_;
  }

  const folly::SocketAddress* getLocalAddress() const {
    return &localAddress_;
  }

  void setLocalAddress(const folly::SocketAddress& localAddress) {
    localAddress_ = localAddress;
  }

  void setRequestHeader(apache::thrift::transport::THeader* header) {
    header_ = header;
  }

  folly::EventBaseManager* getEventBaseManager() override {
    return manager_;
  }

  std::string getPeerCommonName() const {
    if (peerCert_) {
      if (auto cnPtr = wangle::SSLUtil::getCommonName(peerCert_.get())) {
        return std::move(*cnPtr);
      }
    }
    return std::string();
  }

  virtual std::shared_ptr<X509> getPeerCertificate() const {
    return peerCert_;
  }

  template <typename Client>
  std::shared_ptr<Client> getDuplexClient() {
    DCHECK(duplexChannel_);
    auto client = std::dynamic_pointer_cast<Client>(duplexClient_);
    if (!client) {
      duplexClient_.reset(new Client(duplexChannel_));
      client = std::dynamic_pointer_cast<Client>(duplexClient_);
    }
    return client;
  }

  virtual const std::string& getSecurityProtocol() const {
    return securityProtocol_;
  }

  virtual void* getPeerIdentities() const {
    return peerIdentities_.get();
  }

  const folly::AsyncTransportWrapper* getTransport() const {
    return transport_;
  }

  /**
   * Get the user data field.
   */
  virtual void* getUserData() const override {
    return userData_.get();
  }

  /**
   * Set the user data field.
   *
   * @param data         The new value for the user data field.
   * @param destructor   A function pointer to invoke when the connection
   *                     context is destroyed.  It will be invoked with the
   *                     contents of the user data field.
   *
   * @return Returns the old user data value.
   */
  virtual void* setUserData(void* data, void (*destructor)(void*) = nullptr)
      override {
    auto oldData = userData_.release();
    userData_ = {data, destructor ? destructor : no_op_destructor};
    return oldData;
  }

 private:
  std::unique_ptr<void, void (*)(void*)> userData_;
  folly::SocketAddress peerAddress_;
  folly::SocketAddress localAddress_;
  folly::EventBaseManager* manager_;
  std::shared_ptr<RequestChannel> duplexChannel_;
  std::shared_ptr<TClientBase> duplexClient_;
  std::shared_ptr<X509> peerCert_;
  std::unique_ptr<void, void (*)(void*)> peerIdentities_;
  std::string securityProtocol_;
  const folly::AsyncTransportWrapper* transport_;

  static void no_op_destructor(void* /*ptr*/) {}
};

class Cpp2ClientRequestContext
    : public apache::thrift::server::TConnectionContext {
 public:
  Cpp2ClientRequestContext() = default;
  void setRequestHeader(transport::THeader* header) {
    header_ = header;
  }
};

// Request-specific context
class Cpp2RequestContext : public apache::thrift::server::TConnectionContext {
 public:
  explicit Cpp2RequestContext(
      Cpp2ConnContext* ctx,
      apache::thrift::transport::THeader* header = nullptr)
      : TConnectionContext(header),
        ctx_(ctx),
        requestData_(nullptr, no_op_destructor),
        startedProcessing_(false) {}

  void setConnectionContext(Cpp2ConnContext* ctx) {
    ctx_ = ctx;
  }

  // Forward all connection-specific information
  const folly::SocketAddress* getPeerAddress() const override {
    return ctx_->getPeerAddress();
  }

  const folly::SocketAddress* getLocalAddress() const {
    return ctx_->getLocalAddress();
  }

  void reset() {
    ctx_->reset();
  }

  PriorityThreadManager::PRIORITY getCallPriority() {
    return header_->getCallPriority();
  }

  virtual std::vector<uint16_t>& getTransforms() {
    return header_->getWriteTransforms();
  }

  folly::EventBaseManager* getEventBaseManager() override {
    return ctx_->getEventBaseManager();
  }

  void* getUserData() const override {
    return ctx_->getUserData();
  }

  void* setUserData(void* data, void (*destructor)(void*) = nullptr) override {
    return ctx_->setUserData(data, destructor);
  }

  typedef void (*void_ptr_destructor)(void*);
  typedef std::unique_ptr<void, void_ptr_destructor> RequestDataPtr;

  // This data is set on a per request basis.
  void* getRequestData() const {
    return requestData_.get();
  }

  // Returns the old request data context so the caller can clean up
  RequestDataPtr setRequestData(
      void* data,
      void_ptr_destructor destructor = no_op_destructor) {
    RequestDataPtr oldData(data, destructor);
    requestData_.swap(oldData);
    return oldData;
  }

  virtual Cpp2ConnContext* getConnectionContext() const {
    return ctx_;
  }

  bool getStartedProcessing() const {
    return startedProcessing_;
  }

  void setStartedProcessing() {
    startedProcessing_ = true;
  }

  std::chrono::milliseconds getRequestTimeout() const {
    return requestTimeout_;
  }

  void setRequestTimeout(std::chrono::milliseconds requestTimeout) {
    requestTimeout_ = requestTimeout;
  }

  void setMethodName(std::string methodName) {
    methodName_ = std::move(methodName);
  }

  const std::string& getMethodName() {
    return methodName_;
  }

  void setProtoSeqId(int32_t protoSeqId) {
    protoSeqId_ = protoSeqId;
  }

  int32_t getProtoSeqId() {
    return protoSeqId_;
  }

  void setMessageBeginSize(uint32_t messageBeginSize) {
    messageBeginSize_ = messageBeginSize;
  }

  uint32_t getMessageBeginSize() {
    return messageBeginSize_;
  }

 protected:
  static void no_op_destructor(void* /*ptr*/) {}

 private:
  Cpp2ConnContext* ctx_;
  RequestDataPtr requestData_;
  bool startedProcessing_ = false;
  std::chrono::milliseconds requestTimeout_{0};
  folly::Optional<std::chrono::steady_clock::time_point> processingStartTime_;
  std::string methodName_;
  int32_t protoSeqId_{0};
  uint32_t messageBeginSize_{0};
};

} // namespace thrift
} // namespace apache

#endif // #ifndef THRIFT_ASYNC_CPP2CONNCONTEXT_H_
