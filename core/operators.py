from .bases import PyedNode
from .util import UNSET


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


# # #


class PyedAddNode(PyedNode):
  _input_specs = dict(
    left_object=lambda _: True,
    right_object=lambda _: True,
  )

  _input_defaults = dict(
  )

  def perform(self, scratchpad, result):
    # scratchpad persists across different runs
    # result is new every run
    
    return True


# # #


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
