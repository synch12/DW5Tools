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
import tempfile
import fakeCompressor

def pack_file(path,suffix):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    basefiles = [i.split('_', 1)[0] for i in onlyfiles]
    files = [*set(basefiles)]
    files.sort(key = int)
    namedfiles = [glob.glob(path+i+suffix+'*')[0] for i in files]
    outputfile = path.rstrip('\\') +'.dat'
    temp = tempfile.TemporaryFile('w+b')
    temp.write(len(namedfiles).to_bytes(4,'little'))
    for i in namedfiles:
        temp.write((os.path.getsize(i) >>4).to_bytes(4,'little'))
    temp.write((0).to_bytes(((0x10 -(temp.tell() % 0x10))&0xf),'little'))
    for i in namedfiles:
        in_stream = open(i,'rb')
        temp.write(in_stream.read())
        in_stream.close()
    fakeCompressor.compress(temp,path.rstrip('\\')+'.lzp2')
    
    temp.close()
    
    print (outputfile)




def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)



def main():
    print(sys.argv[0])
    pack_file(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()