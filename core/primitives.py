from .bases import PyedNode, PyedNulladic


class PyedConst(PyedNulladic, PyedNode):
  def __init__(self, const, *args, **kwargs):
    self.const = const
    super().__init__(*args, **kwargs)

  def take(self):
    return self.const
