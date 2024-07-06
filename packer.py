###
###   packs files within a directory into .lpf files
###

from glob import glob
import sys
import struct
from typing import BinaryIO, Dict
import math
import os
import glob
from unicodedata import name


def pack_file(path,suffix):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    basefiles = [i.split('_', 1)[0] for i in onlyfiles]
    files = [*set(basefiles)]
    files.sort(key = int)
    namedfiles = [glob.glob(path+i+suffix+'*')[0] for i in files]
    outputfile = path.rstrip('\\') +'.dat'
    out_stream = open(outputfile, 'wb')
    out_stream.write(len(namedfiles).to_bytes(4,'little'))
    for i in namedfiles:
        out_stream.write((os.path.getsize(i) >>4).to_bytes(4,'little'))
    out_stream.write((0).to_bytes(((0x10 -(out_stream.tell() % 0x10))&0xf),'little'))
    for i in namedfiles:
        in_stream = open(i,'rb')
        out_stream.write(in_stream.read())
        in_stream.close()
    out_stream.close()
    
    print (outputfile)




def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)



def main():
    pack_file(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()