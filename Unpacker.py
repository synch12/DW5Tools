import sys
import struct
from typing import BinaryIO, Dict
import math


def unpack(in_stream: BinaryIO, out_path):
    
    bytesIn = in_stream.read()
    iterator = 0
    fileCount = int.from_bytes(bytesIn[0:4],byteorder='little')
    lengths =  dict()
    for i in range(fileCount):
        lengths[i] = int.from_bytes(bytesIn[((i+1)<<2):(((i+1)<<2) +4)],byteorder='little') << 4
    readOffset = (fileCount+1) * 4
    readOffset = readOffset + ((0x10 -(readOffset % 0x10))&0xf)
    iterator = math.ceil(readOffset)
    print(hex(iterator))
    for i in range(fileCount):
        print(i)
        buffer = bytearray()
        for j in range(lengths[i]):
            buffer += bytesIn[readOffset + j].to_bytes(1, byteorder='little')
        out_stream = open(out_path + str(i) + getExtension(buffer), 'wb')
        out_stream.write(buffer)
        out_stream.close()
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

