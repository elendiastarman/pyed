from typing import List

from .bases import PyedNode, PyedValue, PyedNulladic
from .util import UNSET


class PyedConst(PyedNulladic, PyedNode):
  """
  Const nodes output their value forever once set.
  """
  def __init__(self, *args, source: PyedNode = UNSET, hardcoded: object = UNSET, **kwargs):
    self.source = source
    self.hardcoded = hardcoded
    self.output = UNSET
    super().__init__(*args, **kwargs)

  def initialize(self):
    self.emit('value', self.hardcoded)


class PyedGroupNode(PyedNode):
  def __init__(self, inner_nodes: List[PyedNode], *args, **kwargs):
    self.inner_nodes = inner_nodes
    self.inner_root = inner_nodes[0]
    self.output = UNSET
    super().__init__(*args, **kwargs)


class PyedResumable(PyedGroupNode):
  pass
