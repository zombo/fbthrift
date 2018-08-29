/*
 * Copyright 2018-present Facebook, Inc.
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements. See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership. The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License. You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

#include <thrift/compiler/lib/cpp2/util.h>

#include <gmock/gmock.h>
#include <gtest/gtest.h>

using namespace apache::thrift::compiler;

class UtilTest : public testing::Test {};

TEST_F(UtilTest, get_gen_namespace_components_cpp2) {
  t_program p("path/to/program.thrift");
  p.set_namespace("cpp2", "foo.bar");
  p.set_namespace("cpp", "baz.foo");
  EXPECT_THAT(
      cpp2::get_gen_namespace_components(p),
      testing::ElementsAreArray({"foo", "bar"}));
}

TEST_F(UtilTest, get_gen_namespace_components_cpp) {
  t_program p("path/to/program.thrift");
  p.set_namespace("cpp", "baz.foo");
  EXPECT_THAT(
      cpp2::get_gen_namespace_components(p),
      testing::ElementsAreArray({"baz", "foo", "cpp2"}));
}

TEST_F(UtilTest, get_gen_namespace_components_none) {
  t_program p("path/to/program.thrift");
  EXPECT_THAT(
      cpp2::get_gen_namespace_components(p),
      testing::ElementsAreArray({"cpp2"}));
}

TEST_F(UtilTest, get_gen_namespace__cpp2) {
  t_program p("path/to/program.thrift");
  p.set_namespace("cpp2", "foo.bar");
  p.set_namespace("cpp", "baz.foo");
  EXPECT_EQ("foo::bar", cpp2::get_gen_namespace(p));
}

TEST_F(UtilTest, get_gen_namespace_cpp) {
  t_program p("path/to/program.thrift");
  p.set_namespace("cpp", "baz.foo");
  EXPECT_EQ("baz::foo::cpp2", cpp2::get_gen_namespace(p));
}

TEST_F(UtilTest, get_gen_namespace_none) {
  t_program p("path/to/program.thrift");
  EXPECT_EQ("cpp2", cpp2::get_gen_namespace(p));
}