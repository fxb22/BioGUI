import cPickle
import os

def spickle(filename,data):
    fp = open(filename,'wb')
    cPickle.dump(data,fp,cPickle.HIGHEST_PROTOCOL)
    fp.close()

    os.system('attrib +h ' + filename)



def opickle(filename):
    fp = open(filename,'rb')
    retData = cPickle.load(fp)
    fp.close()
    return retData
    
