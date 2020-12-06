UNSET = object()


class Runner:
  def __init__(self, nodes, links, root):
    self.nodes = nodes
    self.links = links
    self.root = root
    self.stage_counter = 0
    self.queue = []
    self.queue_counter = 0

  def run(self):
    while self.queue_counter < len(self.queue):
      curr_node = self.queue[self.queue_counter]

      if curr_node.ready():
        pass


def set_from(*args):
  return next((_ for _ in args if _ is not UNSET), UNSET)


class PyedNode:
  _input_specs = UNSET
  _output_specs = UNSET
  waiting_inputs = UNSET
  ready_inputs = UNSET

  def __init__(self, waiting_inputs=UNSET):
    self.waiting_inputs = set_from(waiting_inputs, self.waiting_inputs, [])

  def unready(self):
    self.waiting_inputs = [*self.ready_inputs, *self.waiting_inputs]

  def ready(self):
    still_waiting = []
    for _input in self.waiting_inputs:
      if _input.ready():
        self.ready_inputs.append(_input)
      else:
        still_waiting.append(_input)

    self.waiting_inputs = still_waiting
    return bool(self.waiting_inputs)

  def peek(self):
    raise NotImplementedError()

  def take(self):
    raise NotImplementedError()


class PyedNulladic:
  _input_specs = None
  ready = lambda: True


class PyedConst(PyedNulladic):
  def __init__(self, const):
    self.const = const

  def peek(self):
    return self.const

  def take(self):
    return self.const


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

s = """
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
"""

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
