// Copyright 2020 The XLS Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Dead Function Elimination.
//
#ifndef XLS_PASSES_DFE_PASS_H_
#define XLS_PASSES_DFE_PASS_H_

#include "absl/status/statusor.h"
#include "xls/ir/function.h"
#include "xls/passes/passes.h"

namespace xls {

// class DeadCodeEliminationPass iterates up from a functions result
// nodes and marks all visited node. After that, all unvisited nodes
// are considered dead.
class DeadFunctionEliminationPass : public Pass {
 public:
  explicit DeadFunctionEliminationPass()
      : Pass("dfe", "Dead Function Elimination") {}
  ~DeadFunctionEliminationPass() override = default;

 protected:
  // Iterate all nodes and mark and eliminate unreachable functions.
  absl::StatusOr<bool> RunInternal(Package* p, const PassOptions& options,
                                   PassResults* results) const override;
};

}  // namespace xls

#endif  // XLS_PASSES_DFE_PASS_H_
