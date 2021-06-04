from core.runner import Runner
from core.director import Director
from core.system import PyedSTDIN, PyedSTDOUT
from core.operators import PyedEquals, PyedCutNode, PyedAddNode
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


def __simple_math():
  a = PyedConst(5)
  b = PyedConst(7)

  add = PyedAddNode(inputs=[['left_object', a], ['right_object', b]])

  stdoutput = PyedSTDOUT(inputs=[add])

  # runner = Runner(root=stdinput, nodes=[stdinput, stdoutput, newline, cut1, pick1, count1])
  director = Director(start_nodes=[stdoutput], all_nodes=[stdoutput, add, a, b])
  director.step()


if __name__ == '__main__':
  __simple_math()
