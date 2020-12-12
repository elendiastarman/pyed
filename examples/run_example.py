import sys
import re


if __name__ == '__main__':
  args = sys.argv
  if len(args) < 2 or args[1].startswith('-'):
    print('Run it like this:')
    print('python run_example.py 00_truth_machine.pyed')

  filepath = args[1]
  with open(filepath, 'r') as file:
    contents = [*file]

  errors = []

  for index, line in enumerate(contents):
    print(f'[{index}]', line)
    # we're gonna parse each line in a super lazy way
    # apply regexes until one matches, then:
    #  * make a node
    #  * chop off the prefix and continue
    line_errors = []

    _str_id = re.match(r'(\w*):', line)
    if _str_id is None:
      line_errors.append('no colon!')
      continue
    else:
      _str_id = _str_id.groups()[0]
      print(f'_str_id: `{_str_id}`')
      line = line[len(_str_id) + 1:]

    args = []
    kwargs = {}
    while line:
      line = line.strip()
      print('line:', line)

      arg = re.match(r'(\$[A-Z]+|(\w+=)?(:?\w+))', line)
      print('arg:', arg)

      if arg is None:
        break
      else:
        print(arg.groups())
        line = line[len(arg.groups()[0]) + 1:]

    errors.append(line_errors)

  for err in errors:
    print('Error:', err)
