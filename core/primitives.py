from typing import List

from .bases import PyedNode, PyedValue, PyedNulladic
from .util import UNSET


class PyedConst(PyedNulladic, PyedNode):
  """
  Const nodes output their value forever once set.
  """
  def __init__(self, source: PyedNode, *args, **kwargs):
    self.source = source
    self.output = UNSET
    super().__init__(*args, **kwargs)

  def prepare(self):
    self.output = self.source.take()

  def take(self) -> PyedValue:
    return self.output


class PyedContainerNode(PyedNode):
  def __init__(self, inner_nodes: List[PyedNode], *args, **kwargs):
    self.inner_nodes = inner_nodes
    self.output = UNSET
    super().__init__(*args, **kwargs)


class PyedResumable(PyedContainerNode):
  pass
