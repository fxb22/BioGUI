# Copyright 2010 by Ahmet Sacan.  All rights reserved.
import os,errno
def filemtime(path):
  try:
    return os.path.getmtime(path)
  except OSError, e:
    if e.errno==errno.ENOENT: return 0
    else: raise