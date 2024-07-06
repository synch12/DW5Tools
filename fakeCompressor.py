###
###
###
###



import packer
import os
import sys
from typing import BinaryIO

def compress(in_stream: BinaryIO, out_path):
    out_stream = open(in_stream.name[:-4] + '.lzp', 'wb')
    length = os.path.getsize(in_stream.name)
    out_stream.write('LZP2'.encode('ASCII'))
    out_stream.write(0x3F8147AE.to_bytes(4,'little'))
    out_stream.write(length.to_bytes(4,'little'))
    out_stream.write((0).to_bytes(4,'little'))
    while length > 0:
        read = 0x3F if length > 0x3F else length
        out_stream.write(read.to_bytes(1,'little'))
        out_stream.write(in_stream.read(read))
        if not read == 0x3F:
            print(read)
        length -= 0x3F
    out_stream.write((0).to_bytes(1024,'little'))
    out_stream.seek(0,2)
    length = out_stream.tell() - 0x10
    out_stream.seek(0x0C)
    out_stream.write(length.to_bytes(4,'little'))
    out_stream.close()

def main():
    in_file = open(sys.argv[1], 'rb')
    compress(in_file, sys.argv[2])


if __name__ == "__main__":
    main()
