#
# Copyright 2022 The XLS Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for xls.fuzzer.run_fuzz."""

import os
from typing import Optional

from absl import flags

from absl.testing import parameterized
from xls.common import test_base
from xls.fuzzer import run_fuzz
from xls.fuzzer.python import cpp_ast_generator as ast_generator
from xls.fuzzer.python import cpp_sample as sample

_CALLS_PER_SAMPLE = 8
_SAMPLE_COUNT = 20

_WIDE = flags.DEFINE_boolean(
    'wide', default=False, help='Run with wide bits types.')


def _get_crasher_dir() -> Optional[str]:
  """Returns the directory in which to write crashers.

  Crashers are written to the undeclared outputs directory, if it is
  available. Otherwise a temporary directory is created.
  """
  if 'TEST_UNDECLARED_OUTPUTS_DIR' in os.environ:
    crasher_dir = os.path.join(os.environ['TEST_UNDECLARED_OUTPUTS_DIR'],
                               'crashers')
    os.mkdir(crasher_dir)
    return crasher_dir
  return None


class RunFuzzTest(parameterized.TestCase):

  def setUp(self):
    super(RunFuzzTest, self).setUp()
    self._crasher_dir = _get_crasher_dir()

  def _get_ast_options(self) -> ast_generator.AstGeneratorOptions:
    return ast_generator.AstGeneratorOptions(
        emit_gate=False, max_width_bits_types=128 if _WIDE.value else 64)

  def _get_sample_options(self) -> sample.SampleOptions:
    return sample.SampleOptions(
        input_is_dslx=True,
        ir_converter_args=['--top=main'],
        calls_per_sample=_CALLS_PER_SAMPLE,
        convert_to_ir=True,
        optimize_ir=True,
        use_system_verilog=False,
        codegen=True,
        simulate=True)

  @parameterized.named_parameters(*tuple(
      dict(testcase_name='seed_{}'.format(x), seed=x) for x in range(50)))
  def test_first_n_seeds(self, seed):
    for i in range(_SAMPLE_COUNT):
      run_fuzz.generate_sample_and_run(
          ast_generator.ValueGenerator(seed * _SAMPLE_COUNT + i),
          self._get_ast_options(),
          self._get_sample_options(),
          run_dir=self.create_tempdir().full_path,
          crasher_dir=self._crasher_dir)


if __name__ == '__main__':
  test_base.main()
