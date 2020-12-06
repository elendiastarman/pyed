from typing import List
# from types import GeneratorType
from uuid import uuid4


class UNSET:
  def __str__(self):
    return '<UNSET>'
  __repr__ = __str__


class RunnerNode:
  SEEN_NODES = dict()

  @classmethod
  def get_or_create(cls, node):
    if node.id in cls.SEEN_NODES:
      return cls.SEEN_NODES[node.id]
    else:
      return RunnerNode(node)

  def __init__(self, node):
    self.id = uuid4()
    self.SEEN_NODES[node.id] = self

    self.node = node
    self.dependents = []
    self.scratchpads = {}


class Runner:
  def __init__(self, root, nodes):
    self.root = RunnerNode.get_or_create(root)
    self.nodes = [*map(RunnerNode.get_or_create, nodes)]
    self.link_nodes()

    self.stage_counter = 0
    self.queue: List[RunnerNode] = [self.root]
    self.queue_counter = 0

  def link_nodes(self):
    for curr_node in [self.root, *self.nodes]:
      for _input in curr_node.node.inputs:
        if isinstance(_input, list):
          _input = _input[1]

        runner_node = RunnerNode.get_or_create(_input)
        runner_node.dependents.append(curr_node)

  def run(self):
    while self.queue_counter < len(self.queue):
      self.step()

  def step(self):
    curr_node = self.queue[self.queue_counter]
    self.queue_counter += 1

    if curr_node.node.ready():
      scratchpad = curr_node.scratchpads.pop(curr_node.id, {})
      result = {}

      curr_node.node.prepare()
      curr_node.node.perform(scratchpad, result)

      curr_node.result = result
      curr_node.scratchpads[curr_node.id] = scratchpad

      self.queue.extend(curr_node.dependents)


def set_from(*args):
  return next((_ for _ in args if _ is not UNSET), UNSET)


class PyedNode:
  _input_specs = UNSET
  _output_specs = UNSET
  waiting_inputs = UNSET
  ready_inputs = UNSET

  def __init__(self, inputs=UNSET):
    assert not (inputs is UNSET) ^ (self._input_specs in [UNSET, None])

    self.id = uuid4()

    self.inputs = set_from(inputs, list())
    self.waiting_inputs = set_from(self.waiting_inputs, dict())
    self.ready_inputs = set_from(self.ready_inputs, dict())

    if self.inputs:
      self.assign_inputs()

  def assign_inputs(self):
    unassigned = []
    for _input in self.inputs:
      # taking care of named inputs first
      if not isinstance(_input, list):
        unassigned.append(_input)

      else:
        _key, _input = _input
        assert _key in self._input_specs and self._input_specs[_key](_input)
        self.waiting_inputs[_key] = _input

    any_assigned = True
    while unassigned and any_assigned:
      still_unassigned = []
      any_assigned = False

      for _input in unassigned:
        for _key, _spec in self._input_specs.items():
          # TODO: make this bit more sophisticated
          if _spec(_input):  # _spec.matches(_input):
            self.waiting_inputs[_key] = _input
            any_assigned = True
            break

        else:
          still_unassigned.append(_input)

      unassigned = still_unassigned

    assert unassigned == []

    # any remaining keys should have defaults
    for _key, _spec in self._input_specs.items():
      if _key not in self.waiting_inputs:
        assert _key in self._input_defaults
        default = self._input_defaults[_key]
        self.waiting_inputs[_key] = default() if callable(default) else default

  def unready(self):
    self.waiting_inputs = {**self.ready_inputs, **self.waiting_inputs}
    self.ready_inputs = dict()

  def ready(self):
    still_waiting = dict()

    for _key, _input in [*self.waiting_inputs.items()]:
      target = self.ready_inputs if _input.ready() else still_waiting
      target[_key] = self.waiting_inputs.pop(_key)

    self.waiting_inputs = still_waiting
    return len(self.waiting_inputs) == 0

  def prepare(self):
    self.ready_values = dict()
    for _key, _input in self.ready_inputs.items():
      if _input is UNSET:
        continue

      elif isinstance(_input, PyedNode):
        self.ready_values[_key] = _input.take()

      else:
        self.ready_values[_key] = _input

  def perform(self, scratchpad, result):
    pass

  def _peek(self):
    if self._latest is not UNSET:
      return self._latest
    else:
      return self.take()

  def peek(self):
    raise NotImplementedError()

  def _take(self):
    _ = self.take()
    self._latest = _
    return _

  def take(self):
    raise NotImplementedError()


class PyedNulladic(object):
  _input_specs = None
  ready = lambda self: True


class PyedConst(PyedNulladic, PyedNode):
  def __init__(self, const, *args, **kwargs):
    self.const = const
    super().__init__(*args, **kwargs)

  def take(self):
    return self.const


class PyedStream(PyedNode):
  pass


class PyedSTDIN(PyedNulladic, PyedStream):
  message = UNSET

  def __init__(self, message=UNSET, *args, **kwargs):
    self.message = set_from(self.message, message, '<input> ')
    self.given = UNSET
    super().__init__(*args, **kwargs)

  def perform(self, scratchpad, result):
    self.given = input(self.message)

  def take(self):
    return self.given


class PyedSTDOUT(PyedStream):
  _input_specs = dict(
    _output=lambda _: True,
  )

  def perform(self, scratchpad, result):
    printed = []
    for _key, _input in self.ready_inputs.items():
      _ = _input.take()
      print(_)
      printed.append(_)
    result['printed'] = printed


class PyedCutNode(PyedNode):
  _input_specs = dict(
    object=lambda _: True,
    cond=lambda _: isinstance(_, PyedNode),
    spacing=lambda _: isinstance(_, PyedNode),
    invert=lambda _: isinstance(_, bool)
  )

  _input_defaults = dict(
    cond=UNSET,
    spacing=UNSET,
    invert=False,
  )

  def perform(self, scratchpad, result):
    gap = next(self.ready_values['spacing'], None) if self.ready_inputs['spacing'] is not UNSET else None
    fresh_seq = lambda: '' if isinstance(self.ready_inputs['object'], str) else []
    seq = []

    for _ in self.ready_inputs['object']:
      if gap is not None:
        gap = gap - 1

      if ((self.ready_inputs['cond'] is not UNSET and self.ready_values['cond'](_)) or (gap == 0)) ^ self.ready_values['invert']:
        if seq:
          yield seq
        seq = fresh_seq()
      else:
        if isinstance(seq, str):
          seq += _
        else:
          seq.append(_)

      if gap == 0:
        gap = next(self.ready_values['spacing'], None)

    if seq:
      yield seq


class PyedComp(PyedNode):
  pass


class PyedEquals(PyedComp):
  _input_specs = dict(
    referent=lambda _: isinstance(_, PyedNode)
  )

  # def __init__(self, node):
  #   self.comp = lambda _: _ == node.take()

  def take(self):
    return lambda _: _ == self.ready_values['referent']


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

"""


def cycle_single(anything):
  while 1:
    yield anything


def cycle_many(anything):
  while 1:
    yield from anything


def cycle_mod(modulo, start=0, step=1):
  x = start
  while 1:
    yield x
    x += step
    if x >= modulo:
      x -= modulo


def eq(anything):
  return lambda _: _ == anything


def mod(modulo):
  return lambda _: _ % modulo


def mod_eq(modulo, anything):
  return lambda _: _ % modulo == anything


def count(obj, cond=None, spacing=None, invert=False):
  gap = next(spacing, None) if spacing is not None else None
  total = 0

  for _ in obj:
    if gap is not None:
      gap = gap - 1

    if ((cond is not None and cond(_)) or (gap is not None and gap == 0)) ^ invert:
      total += 1

    if gap == 0:
      gap = next(spacing, None)

  yield total


def pick(obj, cond=None, spacing=None, invert=False):
  gap = next(spacing, None) if spacing is not None else None

  for _ in obj:
    if gap is not None:
      gap = gap - 1

    if ((cond is not None and cond(_)) or (gap is not None and gap == 0)) ^ invert:
      yield _

    if gap == 0:
      gap = next(spacing, None)


def cut(obj, cond=None, spacing=None, invert=False):
  gap = next(spacing, None) if spacing is not None else None
  fresh_seq = lambda: '' if isinstance(obj, str) else []
  seq = []

  for _ in obj:
    if gap is not None:
      gap = gap - 1

    if ((cond is not None and cond(_)) or (gap is not None and gap == 0)) ^ invert:
      if seq:
        yield seq
      seq = fresh_seq()
    else:
      if isinstance(seq, str):
        seq += _
      else:
        seq.append(_)

    if gap == 0:
      gap = next(spacing, None)

  if seq:
    yield seq


def foreach(source, operation):
  for _ in source:
    yield from operation(_)


print('abc'.split('b'))
print(list(cut('abc', eq('b'))))
print(list(cut(range(10), mod_eq(3, 0))))

s = " ""
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
" ""

print([*map(list,
  # count(
    map(
      lambda _: pick(_[0], spacing=_[1]),
      zip(
        cut(s, cond=eq('\n')),
        cycle_mod(modulo=11, step=3),
      ),
    ),
    # cond=eq('#'),
  ),
])

print([*
  count(
    map(
      lambda _: pick(_[0], spacing=_[1]),
      zip(
        cut(s, cond=eq('\n')),
        cycle_mod(modulo=11, step=3),
      ),
    ),
    cond=eq('#'),
  ),
])

"""
