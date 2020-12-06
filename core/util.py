class UNSET:
  def __str__(self):
    return '<UNSET>'
  __repr__ = __str__


def set_from(*args):
  return next((_ for _ in args if _ is not UNSET), UNSET)
