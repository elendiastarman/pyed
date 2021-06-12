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

  def perform(self, scratchpad):
    self.given = input(self.message)

  def take(self):
    return self.given


class PyedSTDOUT(PyedStream):
  _input_specs = dict(
    _output=lambda _: True,
  )

  def perform(self, scratchpad):
    print('STDOUT')
    print('STDOUT self.ready_inputs', self.ready_inputs)
    printed = []
    for _key, _input in self.waiting_inputs.items():
      print('_input', _input)
      _ = _input.take()
      print(_)
      printed.append(_)
    self.emit('printed', printed)

  def take(self):
    return self.getval('printed')
