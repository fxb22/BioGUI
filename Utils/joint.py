# Copyright 2010 by Ahmet Sacan.  All rights reserved.
import os
def join(path,*arg):
  for a in arg:
    if path.endswith('/'): path += a
    else: path += '/' + a
  return path
