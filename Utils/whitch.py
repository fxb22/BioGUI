# Copyright 2010 by Ahmet Sacan.  All rights reserved.
import os,errno
import resolvepatch
import joint

def which(fileSearch,root,i):
  alpha = joint.join(root,fileSearch)
  i+=1
  if os.path.exists(alpha):
    return root
  else:
    try:
      if os.path.exists(root):
        dirty = os.listdir(root)
        for dirT in dirty:
          i+=1
          if not dirT in ['MATLAB','Geneious']:
            gamma = joint.join(root, dirT)
            f = joint.join(root, dirT)
            beta = which(fileSearch,f,i)
            if beta>=0:
              delta = joint.join(f,fileSearch)
              return beta
      else:
        return -1
    except WindowsError:
      return -1

