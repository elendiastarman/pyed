# from typing import List
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

    self.ready_nodes = set()
    # self.pending_nodes = {'dep_counts': [], 0: []}
    self.pending_nodes = dict()
    self.downstream = {}

  def make_node_graph(self, start_nodes, all_nodes):
    node_graph: dict = {}

    for node_desc in all_nodes:
      # in this first iteration, node_desc are basically Python instances of classes
      # such as PyedConst, PyedAddNode, and PyedSTDOUT

      scratchpad: dict = {}  # this is shared between self.parse_desc and self.make_node
      signature, references = self.parse_desc(node_desc, scratchpad)  # do interesting stuff here

      if signature in node_graph:
        # we've already scanned these nodes, move along, move along
        continue

      node = self.make_node(node_desc, scratchpad, signature=signature)  # do more interesting stuff here
      node_data = {
        'node': node,
        'refs': {ref: None for ref in references},
        'output_ready': False,
        'scratchpad': {},
      }
      node_graph[signature] = node_data

    self.resolve_graph_references(node_graph)

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
          refs[ref_signature] = node_graph[ref_signature]

  def initialize(self):
    for signature, data in self.node_graph.items():
      print(f'{signature=}')
      data['node'].initialize()
      data['node'].reset()

    start_signatures = [self.parse_desc(start_node, {}, signature_only=True) for start_node in self.start_nodes]
    self.add_pending_nodes(start_signatures)

  def add_pending_nodes(self, signatures):
    while signatures:
      dep_signatures = set()

      for signature in signatures:
        print('signature', signature)
        if signature in self.ready_nodes or signature in self.pending_nodes:
          continue

        data = self.node_graph[signature]
        print('data', data)
        deps = set()

        for ref_signature in data['refs']:
          ref_data = self.node_graph[ref_signature]

          if ref_data['output_ready']:
            continue

          deps.add(ref_signature)
          dep_signatures.add(ref_signature)
          self.downstream.setdefault(ref_signature, set()).add(signature)

        print('deps', deps)
        if not deps:
          self.ready_nodes.add(signature)

        else:
          self.pending_nodes[signature] = deps

      signatures = dep_signatures

  def step(self):
    # nodes with 0 dependencies can be evaluated immediately
    # after each such node is evaluated, we update deps for downstream nodes

    print('(before)')
    print('ready signatures', self.ready_nodes)
    print('pending nodes')
    for sg, d in self.pending_nodes.items():
      print('    ', sg, d)

    still_ready = set()
    for signature in self.ready_nodes:
      print('ready', signature)
      data = self.node_graph[signature]
      print('ready', signature, data['node'], data['refs'])

      data['output_ready'] = data['node'].perform(data['scratchpad'])

      if not data['output_ready']:
        continue

      # downstream nodes need to know that this one just finished
      for downstream_signature in self.downstream.get(signature, set()):
        if downstream_signature in self.pending_nodes:
          self.pending_nodes[downstream_signature].remove(signature)

      # if data['node'].resumable:
      #   still_ready.add(signature)

    self.ready_nodes = still_ready

    still_pending = {}
    for signature, deps in self.pending_nodes.items():
      print('waiting', signature, deps)
      if deps:
        still_pending[signature] = deps
      else:
        self.ready_nodes.add(signature)

    self.pending_nodes = still_pending

    print('(after)')
    print('ready signatures', self.ready_nodes)
    print('pending nodes')
    for sg, d in self.pending_nodes.items():
      print('    ', sg, d)
