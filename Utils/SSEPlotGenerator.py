import numpy as np
from matplotlib.colors import colorConverter

def SSEPlot(sse, plotter):
    axes1 = plotter.add('figure 1').gca()
    axes1.axis('off')
    ps = plotter.GetSize()
    w = 200. / len(sse) * 892. / ps[0]
    lineDict = {'H':[.1,.9,'r',w],
                 'E':[.25,.75,'b',w],
                 '.':[.35,.65,'k',w/2.]}
    x = []
    tub = [[],[],[],[]]
    for j,l in enumerate(sse):
        x = [j * 892. / ps[0]]
        for i,t in enumerate(tub):
            tub[i] = [lineDict[l][i]]
        axes1.vlines(np.array(x),np.array(tub[0]),np.array(tub[1]),
                     colors=colorConverter.to_rgba(tub[2][0]),
                     linewidths=np.array(tub[3]))
    axes1.set_xlim(0,len(sse) * 892. / ps[0])
    axes1.set_ylim(0,1)
    return axes1
