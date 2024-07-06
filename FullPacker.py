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
    from os.path import isfile, join, isdir
    onlyfolders = [f for f in listdir(path) if isdir(join(path, f))]
    folders = [*set(onlyfolders)]
    folders.sort(key = int)
    print(folders)
    paths = [join(path, f + '\\') for f in folders]
    print(paths)

    out_stream = open(path+'.dat', 'wb')
  

    for p in paths:
        onlyfiles = [f for f in listdir(p) if isfile(join(p+'\\', f))]
        basefiles = [i.split('_', 1)[0] for i in onlyfiles]
        files = [*set(basefiles)]
        files.sort(key = int)
        namedfiles = [glob.glob(p+i+suffix+'*')[-1] for i in files]
        out_stream.write(len(namedfiles).to_bytes(4,'little'))
        for i in namedfiles:
            out_stream.write((os.path.getsize(i) >>4).to_bytes(4,'little'))
        out_stream.write((0).to_bytes(((0x10 -(out_stream.tell() % 0x10))&0xf),'little'))
        for i in namedfiles:
            in_stream = open(i,'rb')
            out_stream.write(in_stream.read())
            in_stream.close()
        out_stream.write( bytearray((0xC400-(out_stream.tell()%0xC400))if not(out_stream.tell()%0xC400) <= 0x10 else 0 ))
    out_stream.close()




def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)



def main():
    pack_file(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()