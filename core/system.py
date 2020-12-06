from .bases import PyedNode, PyedNulladic
from .util import UNSET, set_from


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
