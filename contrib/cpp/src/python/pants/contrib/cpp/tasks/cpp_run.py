# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import os

from pants.base.workunit import WorkUnit
from pants.util.dirutil import safe_mkdir

from pants.contrib.cpp.targets.cpp_binary import CppBinary
from pants.contrib.cpp.tasks.cpp_task import CppTask


class CppRun(CppTask):
  """Runs a cpp binary"""

  @classmethod
  def register_options(cls, register):
    super(CppRun, cls).register_options(register)
    register('--args',
             action='append',
             help='Append these options to the executable command line.')

  @classmethod
  def supports_passthru_args(cls):
    return True

  @classmethod
  def prepare(cls, options, round_manager):
    super(CppRun, cls).prepare(options, round_manager)
    # Require that an executable has been built.
    round_manager.require_data('exe')

  def execute(self):
    binary = self.require_single_root_target()
    if isinstance(binary, CppBinary):
      with self.context.new_workunit(name='cpp-run', labels=[WorkUnit.TASK]):
        cmd = [os.path.join(binary.workdir, binary.id, binary.name)]
        args = self.get_options().args + self.get_passthru_args()
        if args != None:
          cmd.extend(args)

        self.run_command(cmd)
