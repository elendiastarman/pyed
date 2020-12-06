from typing import List
# from types import GeneratorType
from uuid import uuid4


class RunnerNode:
  SEEN_NODES = dict()

  @classmethod
  def get_or_create(cls, node):
    if node.id in cls.SEEN_NODES:
      return cls.SEEN_NODES[node.id]
    else:
      return RunnerNode(node)

  def __init__(self, node):
    self.id = uuid4()
    self.SEEN_NODES[node.id] = self

    self.node = node
    self.dependents = []
    self.scratchpads = {}


class Runner:
  def __init__(self, root, nodes):
    self.root = RunnerNode.get_or_create(root)
    self.nodes = [*map(RunnerNode.get_or_create, nodes)]
    self.link_nodes()

    self.stage_counter = 0
    self.queue: List[RunnerNode] = [self.root]
    self.queue_counter = 0

  def link_nodes(self):
    for curr_node in [self.root, *self.nodes]:
      for _input in curr_node.node.inputs:
        if isinstance(_input, list):
          _input = _input[1]

        runner_node = RunnerNode.get_or_create(_input)
        runner_node.dependents.append(curr_node)

  def run(self):
    while self.queue_counter < len(self.queue):
      self.step()

  def step(self):
    curr_node = self.queue[self.queue_counter]
    self.queue_counter += 1

    if curr_node.node.ready():
      scratchpad = curr_node.scratchpads.pop(curr_node.id, {})
      result = {}

      curr_node.node.prepare()
      curr_node.node.perform(scratchpad, result)

      curr_node.result = result
      curr_node.scratchpads[curr_node.id] = scratchpad

      self.queue.extend(curr_node.dependents)
