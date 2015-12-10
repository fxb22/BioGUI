# Copyright 2004 by Harry Zuzan.  All rights reserved.
# This code is part of the Biopython distribution and governed by its
# license.  Please see the LICENSE file that should have been included
# as part of this package.

#Edited for speed for BioGui. Core function was preserved.

"""
Classes for accessing the information in Affymetrix cel files.

Functions:
read      Read a cel file and store its contents in a Record

Classes:
Record    Contains the information from a cel file


"""

import numpy
import gzip

class Record:
    """
    Stores the information in a cel file
    """
    def __init__(self):
        self.intensities = None
        self.nrows = None
        self.ncols = None


def read(handle):
    """
    Read the information in a cel file, and store it in a Record.
    """
    # Needs error handling.
    # Needs to know the chip design.
    record = Record()
    for line in handle:
        if not line.strip():
            continue
        if line[:8]=="[HEADER]":
            section = "HEADER"
        elif line[:11]=="[INTENSITY]":
            section = "INTENSITY"
            record.intensities  = numpy.zeros((record.nrows, record.ncols))
        elif line[0]=="[":
            section = ""
        elif section=="HEADER":
            keyword, value = line.split("=", 1)
            if keyword=="Cols":
                record.ncols = int(value)
            elif keyword=="Rows":
                record.nrows = int(value)
        elif section=="INTENSITY":
            if "=" in line:
                continue
            words = line.split()
            y, x = map(int, words[:2])
            record.intensities[x,y]  = float(words[2])
    return record

def platform(handle):
    h = gzip.GzipFile(r'.\CurrentCel/'+handle)
    i = 0
    stopper = True
    pName = ''
    while stopper:
        line = h.readline()
        if line[:9] == 'DatHeader':
            for split in line.split():
                if r'.1sq' in split:
                    pName = split[:-4]
                    print pName
            stopper = False
    return pName
