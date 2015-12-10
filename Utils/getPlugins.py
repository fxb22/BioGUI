import sys
import os

def GetPlugIns(dirt):
    sys.path.append(dirt)
    views = {}
    for f in os.listdir(dirt):
        (name, ext) = os.path.splitext(f)
        if ext == '.py':
            v = __import__(str(name))
            views[v.GetName()] = v
    return views
