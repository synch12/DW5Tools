###
###   Unpacks .lpf files
###
###
###




import sys
import struct
from typing import BinaryIO, Dict
import math
import os

def unpack(in_stream: BinaryIO, out_path):
    in_stream.seek(0, 2)
    filesize = in_stream.tell()
    in_stream.seek(0)
    out_path = out_path+ '\\'
    print("unpacking")
    os.mkdir(out_path)
    bytesIn = in_stream.read()
    iterator = 0
    fileCount = int.from_bytes(bytesIn[0:4],byteorder='little')
    lengths =  dict()
    for i in range(fileCount):
        lengths[i] = int.from_bytes(bytesIn[((i+1)<<2):(((i+1)<<2) +4)],byteorder='little') << 4
    print(lengths)
    readOffset = (fileCount+1) * 4
    readOffset = readOffset + ((0x10 -(readOffset % 0x10))&0xf)
    iterator = math.ceil(readOffset)
    index = 0
    filecount = 0
    
    print(hex(iterator))
    print("Offset " + str(readOffset) +'\nFile Size' + str( filesize))
    while(readOffset <= filesize):
        for i in range(fileCount):
            print(lengths)
            buffer = bytearray()
            for j in range(lengths[i]):
                buffer += bytesIn[readOffset + j].to_bytes(1, byteorder='little')
                index+=1
            print(buffer)
            out_stream = open(out_path +'\\'+ str(filecount)+'_ORIGINAL' + getExtension(buffer), 'wb')
            out_stream.write(buffer)
            out_stream.close()
            filecount += 1
            readOffset+=lengths[i]

        

def getExtension(buffer):
    extensions = {
        "TIM2": ".tm2",
        "GT1G": ".g1t",
        "MESC": ".strings"

    }
    try:
        return extensions.get(buffer[0:4].decode("utf-8"),'.dat')
    except:
        return '.dat'





def unpack_file(in_path, out_path):
    with open(in_path, 'rb') as in_file:
        unpack(in_file, out_path)

def main():
    unpack_file(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
