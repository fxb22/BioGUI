# Copyright 2010 by Ahmet Sacan.  All rights reserved.
# resolve path, getting rid of '../' and './'

import re
def resolvepath(path):
  if not path: return path
  paths = path.replace('\\','/').split('/')  
  changed = True;
  while changed:
    changed = False
    i = len(paths) - 1
    while i >= 0:
      if i >= 1 and paths[i] == '..' and paths[i - 1] not in ('..','.',''): #replace dir/../ with dir/
        paths = paths[:i - 1] + paths[i + 1:]
        i -= 1
        changed = True
      elif paths[i] == '.': #remove  ./
        paths = paths[:i] + paths[i + 1:]
        changed = True
      elif i >= 1 and not paths[i]: #replace // with / if it doesn't follow 'xx:'
        if not (i == 1 and re.search('..:$',paths[i - 1])):
          paths = paths[:i] + paths[i + 1:]
          changed = True
      i -= 1
  return '/'.join(paths)
