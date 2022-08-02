###
###  Extracts lzp2 files contents as '.dat' files specific tools are needed to access the .dat
###
###
import Unpacker
import tempfile

import sys
import struct
from typing import BinaryIO

def decompress_lzp2(in_stream: BinaryIO, out_path):
    gap = 0
    searchvalue = 0x218F
    file_count = 0
    Raw = False
    bytesIn = in_stream.read()
    datasize = len(bytesIn)
    iterator = 0x10
    length = struct.unpack('<I', bytesIn[12:0x10])[0]
    print(hex(length))
    buffer = bytearray()
    #buffer += 0x00.to_bytes(1, byteorder='little')
    while(length+0x10>iterator):
        if gap == 0:
            flag  = bytesIn[iterator] &0XC0
            gap = bytesIn[iterator] if not flag else 0
            iterator += 1 if gap >0 else 0
        for i in range(gap):
            buffer += bytesIn[iterator].to_bytes(1, byteorder='little')
            iterator += 1
        gap, iterator = handlereference(iterator,length,buffer,bytesIn)
        iterator +=1

    if(not Raw):
        temp = tempfile.TemporaryFile('w+b')
        temp.write(buffer)
        temp.seek(0)
        Unpacker.unpack(temp,out_path)
    else:
        out_stream = open(out_path + str(file_count) + '.lpf', 'wb')
        out_stream.write(buffer)
        out_stream.close()

def handlereference(iterator,length,buffer,bytesIn):
    #print(iterator,'/', length)
    gap = 0
    if(bytesIn[iterator] & 0x80):
        #print('symbol == ' + hex(bytesIn[iterator]))
        currentByte = bytesIn[iterator]
        flag = 3
        flag += 1 if currentByte & 0x08 else 0
        flag += 2 if currentByte & 0x10 else 0
        flag += 4 if currentByte & 0x20 else 0
        flag += 8 if currentByte & 0x40 else 0
        iterator +=1
        Offset = bytesIn[iterator]
        #print('offset == ' + hex(bytesIn[iterator]))
        temp =0
        temp +=bytesIn[iterator - 1]&7
        Offset += temp<<8
        Offset += 1
        if Offset == 1:
            byte = buffer[-1]
            for i in range(flag):
                buffer += byte.to_bytes(1, byteorder='little')
        else:
            for i in range(flag):
                buffer += buffer[-Offset:-Offset+1]
    elif bytesIn[iterator] & 0x40:
        iterator = RLEread(iterator,length,buffer,bytesIn)
    else:
        gap = bytesIn[iterator]
    return gap, iterator

def RLEread(iterator,length,buffer,bytesIn):
    iterator += 1
    temp = bytesIn[iterator-1]&0x3f
    amount = bytesIn[iterator] + 3 +(temp <<8)
    iterator += 1
    value = bytesIn[iterator]
    for i in range(amount + 1):
        buffer += value.to_bytes(1, byteorder='little')
    
    return  iterator


def decompress_lzp2_file(in_path, out_path):
    with open(in_path, 'rb') as in_file:
        decompress_lzp2(in_file, out_path)

def main():
    decompress_lzp2_file(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()

