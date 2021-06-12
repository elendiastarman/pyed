from .util import UNSET, EMPTY, set_from
from uuid import uuid4


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

    self.result = {}

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

  # def unready(self):
  #   self.waiting_inputs = {**self.ready_inputs, **self.waiting_inputs}
  #   self.ready_inputs = dict()

  # def ready(self):
  #   still_waiting = dict()

  #   for _key, _input in [*self.waiting_inputs.items()]:
  #     target = self.ready_inputs if _input.ready() else still_waiting
  #     target[_key] = self.waiting_inputs.pop(_key)

  #   self.waiting_inputs = still_waiting
  #   return len(self.waiting_inputs) == 0

  # def prepare(self):
  #   self.ready_values = dict()
  #   for _key, _input in self.ready_inputs.items():
  #     if _input is UNSET:
  #       continue

  #     elif isinstance(_input, PyedNode):
  #       self.ready_values[_key] = _input.take()

  #     else:
  #       self.ready_values[_key] = _input

  # def perform(self, scratchpad, result):
  #   pass

  # def _peek(self):
  #   if self._latest is not UNSET:
  #     return self._latest
  #   else:
  #     return self.take()

  # def peek(self):
  #   raise NotImplementedError()

  # def _take(self):
  #   _ = self.take()
  #   self._latest = _
  #   return _

  # def take(self):
  #   raise NotImplementedError()

  ...

  @classmethod
  def define(cls, input_specs, output_specs):
    """Given a set of inputs and outputs, do things accordingly."""
    ...

  def emit(self, field, value):
    """Puts 'value' in the exposed slot for 'field'."""
    self.result[field] = value

  def getval(self, field):
    """Returns the value in the exposed slot for 'field'; mostly useful for internal node ops."""
    return self.result[field]

  def take(self, field: str = None):
    """Like getval, but defaults 'field' to 'value'. This method can also do more complex things if desired."""
    return self.getval(field or 'value')

  def initialize(self):
    """Does anything that is needed once at the start and then never again, or reused throughout."""
    pass

  def reset(self):
    """Reverts to a blank slate as if no operations were run."""
    self._base_reset()

  def _base_reset(self):
    self.errors = []

  def prepare(self, scratchpad):
    """Any setup work needed for an operation."""
    pass

  def perform(self, scratchpad):
    """Does the actual operation(s)."""
    # scratchpad persists across different runs

    # return True if there's new output to be consumed by downstream nodes
    # return False if e.g. an error (this will probably change in the future)
    return True

  def finish(self):
    """Closes out anything necessary."""
    ...
    self.emit('value', EMPTY)

  def resume(self):
    raise NotImplementedError()


class PyedValue(object):
  pass


class PyedNulladic(object):
  _input_specs = None
  ready = lambda self: True
