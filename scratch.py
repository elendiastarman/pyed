from core.runner import Runner
from core.system import PyedSTDIN, PyedSTDOUT
from core.operators import PyedEquals, PyedCutNode
from core.primitives import PyedConst


def __cat():
  stdinput = PyedSTDIN()
  stdoutput = PyedSTDOUT(inputs=[stdinput])

  runner = Runner(root=stdinput, nodes=[stdinput, stdoutput])
  runner.run()


def __aoc_day3():
  stdinput = PyedSTDIN()
  newline = PyedEquals(inputs=[PyedConst('\n')])

  cut1 = PyedCutNode(inputs=[['object', stdinput], ['cond', newline]])
  # pick1 = PyedPickNode(inputs=[['object', cut1], '\n'])
  # count1 = PyedCountNode(inputs=[['object', cut1], '\n'])

  stdoutput = PyedSTDOUT(inputs=[cut1])

  # runner = Runner(root=stdinput, nodes=[stdinput, stdoutput, newline, cut1, pick1, count1])
  runner = Runner(root=stdinput, nodes=[stdinput, stdoutput, newline, cut1])
  runner.step()


if __name__ == '__main__':
  __aoc_day3()
