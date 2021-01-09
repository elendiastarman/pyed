import sys
import re

from ..system import PyedSTDIN


class BuiltInParser:
  def consume(self, _input, stack):
    name = ''

    for char in _input:
      if char == ' ':
        break
      else:
        name += char

    if name == 'STDIN':
      node = PyedSTDIN()
    elif name == 'LOOP':
      # node = PyedSTDIN()
      ...
    else:
      raise ValueError(f'Unknown builtin: `{name}`')

    return node, None


class LabelParser:
  def consume(self, _input, stack):
    label = ''

    for char in _input:
      if char == ':':
        return label, ExpressionParser()
      elif char == '/':
        return None, None
      else:
        label += char


class ExpressionParser:
  def consume(self, _input, stack):
    for char in _input:
      if char == '$':
        return None, [self, BuiltInParser()]
      elif char == '\n':
        return None, [self, LabelParser()]


class ProgramParser:
  def __init__(self, parsers=None):
    self.parsers = [] or parsers
    self.stack = []
    self.nodes = []

  def parse(self, _input):
    curr_parser = self.stack.pop()
    node, parsers = curr_parser.consume(_input, self.stack)

    if node:
      self.nodes.append(node)

    if parsers:
      self.stack.extend(parsers)


if __name__ == '__main__':
  args = sys.argv
  if len(args) < 2 or args[1].startswith('-'):
    print('Run it like this:')
    print('python run_example.py 00_truth_machine.pyedasm')

  filepath = args[1]
  with open(filepath, 'r') as file:
    contents = [*file]

  print('contents:')
  print(contents)
