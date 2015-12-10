import os
import sys
import errno
import time
from datetime import datetime
import filemtime as fmt
import Catche as mP

from xml.dom import minidom
import tarfile

def GetExec():
    try:
        for names in os.listdir(r'.\CurrentCel/'):
            os.remove(r'.\CurrentCel/'+names)
            os.removedirs(r'.\CurrentCel')
    except:
        errno
    Recs = os.listdir(os.getcwd())
    newList=[]
    j = 0
    PForm = ""
    listdata=dict()
    GeoUntar = []
    k = 0
    ftime = open('lastChecked.txt','r')
    prevTime = float(ftime.readline())
    ftime.close()
    f = open('lastChecked.txt','w')
    f.write(str(time.time()))
    f.close()
    for i in Recs:
        (nameLeft, ext) = os.path.splitext(i)
        if ext == '.tgz':
            newList.append([i])
            geoListFile = nameLeft + ".pickle"
            if not os.path.isfile(geoListFile) or float(fmt.filemtime(i)) > prevTime:
                filelib = tarfile.TarFile.gzopen(i)
                #Istar = i
                GeoUntar.append(filelib)
                #print Istar
                nameHolder = filelib.getnames()
                ''''for k,itsgo in enumerate(nameHolder):
                    try:
                        if itsgo[-4:] =='.txt' :
                            if itsgo[0:3] != r"GPL":
                                newList.append(itsgo)
                            elif itsgo[0:3] == r"GPL":
                                PForm = itsgo[:-10]
                        elif itsgo[-4:] == ".xml":
                            f = filelib.extractfile(itsgo)
                            minimal = minidom.parse(f).childNodes[0]
                            titleText = minimal.childNodes[-2].childNodes[3].childNodes[0].toxml()
                    except IOError, e:
                        print e'''
                #print nameHolder[:5]
                PForm = nameHolder[1][:-10]
                #i = nameHolder[0]
                #print i
                f = filelib.extractfile(nameHolder[0])
                minimal = minidom.parse(f).childNodes[0]
                titleText = minimal.childNodes[-2].childNodes[3].childNodes[0].toxml()
                #print len(minimal.childNodes)
                listdata[j] = str(nameLeft[:-4]),titleText, PForm, len(nameHolder)-2
                rHoward = [nameLeft,titleText,PForm,len(nameHolder)-2]
                mP.spickle(geoListFile,rHoward)

                j += 1
            else:
                rHoward = mP.opickle(geoListFile)
                listdata[j] = str(rHoward[0][:-4]),rHoward[1],rHoward[2],rHoward[3]
                
                j += 1
        elif ext == r'.tar':
            filelib = tarfile.TarFile.taropen(i)
            nameHolder = filelib.getnames()
            cels = 0
            for n in nameHolder:
                if n[-7:] == r'.CEL.gz':
                    cels += 1
                    """
            sys.path.append(r'..\plugins\Tools\ETOOLSPlugins')
            exTool = __import__('ESearch').GetExec('gds',str(nameLeft[:-4]))
            esTool = __import__('ESummary').GetExec('gds',str(exTool['IdList'][0]))

            titleText = ''
            PForm = ''
            for line in esTool.split('\n'):
                if len(line) > 32:
                    if line[:34] == '\t<Item Name="title" Type="String">':
                        titleText = line[34:-8]
                    elif line[:32] == '\t<Item Name="GPL" Type="String">':
                        PForm = 'GPL' + str(line[32:-7])
                        
            listdata[j] = str(nameLeft[:-4]),titleText, PForm, cels
            newList.append([i,PForm])"""
            
    return [newList,listdata]
