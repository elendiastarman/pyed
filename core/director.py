from typing import List
# from types import GeneratorType
from uuid import uuid4


class Director:
  def __init__(self, start_nodes, all_nodes):
    self.start_nodes = start_nodes
    self.all_nodes = all_nodes
    self.node_graph = self.make_node_graph(start_nodes, all_nodes)

    # import pprint
    # pprint.pprint(self.start_nodes)
    # pprint.pprint(self.node_graph)

  def make_node_graph(self, start_nodes, all_nodes):
    node_graph: dict = {}

    for node_desc in all_nodes:
      # in this first iteration, node_desc are basically Python instances of classes
      # such as PyedConst, PyedAddNode, and PyedSTDOUT

      scratchpad: dict = {}  # this is shared between self.parse_desc and self.make_node
      signature, references = self.parse_desc(node_desc, scratchpad)  # do interesting stuff here

      if signature in node_graph:
        # we've already scanned these nodes, move along move along
        continue

      node = self.make_node(node_desc, scratchpad, signature=signature)  # do more interesting stuff here
      node_graph[signature] = {'node': node, 'refs': {ref: None for ref in references}}

    self.resolve_graph_references(node_graph)

    for index, start_node in enumerate(self.start_nodes):
      signature = self.parse_desc(start_node, {}, signature_only=True)
      self.start_nodes[index] = node_graph[signature]

    return node_graph

  def parse_desc(self, node_desc, scratchpad: dict, *, signature_only=False):
    # scratchpad will be reused by self.make_node
    signature = uuid4()
    refs = []

    # in this first iteration, node_desc is a list where the first element is an input spec name
    # and the second element is a Python instance of a class like PyedConst
    # and those classes inherit from PyedNode which sets self.id on every instance

    signature = node_desc.id
    if signature_only:
      return signature

    for ref, node in [*node_desc.ready_inputs.items(), *node_desc.waiting_inputs.items()]:
      refs.append(node.id)

    #

    return signature, refs

  def make_node(self, node_desc, scratchpad, signature=None):
    # scratchpad was used by self.parse_desc

    # in this first iteration, node_desc is a Python instance of a class like PyedConst
    # so there's really nothing to do here
    return node_desc

  def resolve_graph_references(self, node_graph):
    # node_graph is expected to have *all* of the nodes, and each has a 'refs' item
    # so we can simply loop through them and resolve the ones that need to

    for signature, data in node_graph.items():
      refs = data['refs']

      for ref_signature, ref_data in refs.items():
        if ref_data is None:
          try:
            refs[ref_signature] = node_graph[ref_signature]
          except KeyError:
            import ipdb; ipdb.set_trace()
