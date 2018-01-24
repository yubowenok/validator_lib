# input validator lib methods

import sys, re

debug_line = ''
debug_line_number = 0

if len(sys.argv) >= 2 and sys.argv[1] == 'input':
  sys.stdin = open('input', 'r')

def abort(err='error', code=-1):
  print >> sys.stderr, '%s on line %d: %s' % (err, debug_line_number, debug_line)
  sys.exit(code)

def get_int(s, low=-int(1e100), high=int(1e100)):
  """Parses a string token s into an integer between [low, high]
     s may not contain newline at the end. Use get_line to read the line.
  """
  if re.match('^-?\d+$', s) == None:
    abort('couldn\'t match integer "%s"' % (s,))
  try:
    x = int(s)
  except Exception:
    abort('couldn\'t parse int "%s"' % (s,))
  if (x == 0 and s != '0') or (x != 0 and s[0] == '0'):
    abort('leading zeroes before integer "%s"' % (s,))
  if x < low or x > high:
    abort('int %d out of range [%d, %d]' % (x, low, high))
  return x

def get_ints(line, n=-1, low=-int(1e100), high=int(1e100)):
  """Parses a line string into exactly n single space separated integers.
     The value of each integer should be between [low, high].
     line may not contain newline at the end. Use get_line to read the line.
  """
  if re.match('^(?:-?\d+ )*-?\d+ *$', line) == None:
    abort('not a line with integers separated by single spaces')
  ints = [get_int(s, low, high) for s in re.split('\s+', line.strip())]
  if len(ints) != n and n != -1:
    abort('number of integers on a line is not %d' % (n,))
  return ints

def get_float(s, low=-1e100, high=1e100):
  """Parses a string token s into a float between [low, high]
     s may not contain new line at the end. Use get_line to read the line.
  """
  if re.match('^-?\d*(\.\d*)?$', s) == None:
    abort('couldn\'t match floating number "%s"' % (s,))
  try:
    x = float(s)
  except Exception:
    abort('couldn\'t parse float "%s"' % (s,))
  if re.match('^00', s) != None:
    abort('extra leading zeroes before float "%s"' % (s,))
  if x < low or x > high:
    abort('float %f out of range [%f, %f]' % (x, low, high))
  return x

def get_floats(line, n, low=-1e100, high=1e100):
  """Parses a line string into exactly n single space separated floats.
     The value of each float should be between [low, high].
     line may not contain newline at the end. Use get_line to read the line.
  """
  if re.match('^(-?\d*(\.\d*)? )*-?\d*(\.\d*)?$', line) == None:
    abort('not a line with floats separated by single spaces')
  floats = [get_float(s, low, high) for s in line.split(' ')]
  if len(floats) != n:
    abort('number of floats on a line is not %d' % (n,))
  return floats

def get_line(expectEOF=False):
  """Parses a line and return the line content.
     Newline characters at the end of the line is removed.
     None is returned if EOF is reached.
  """
  global debug_line, debug_line_number
  line = sys.stdin.readline()
  if line == '' and not expectEOF:
    abort()  # unexpected EOF reached, empty line is '\n'
  if line == '':
    return None
  if line.find('\r') != -1:
    abort()  # cannot contain windows line ending
  debug_line_number += 1
  debug_line = line
  return line.rstrip('\n')


def get_EOF():
  if get_line(True) != None:
    abort('extra empty line before EOF')
