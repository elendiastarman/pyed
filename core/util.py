class Constant:
  def __init__(self, name):
    self.name = name

  def __str__(self):
    return f'<{self.name}>'
  __repr__ = __str__


UNSET = Constant('UNSET')
EMPTY = Constant('EMPTY')


def set_from(*args):
  return next((_ for _ in args if _ is not UNSET), UNSET)
