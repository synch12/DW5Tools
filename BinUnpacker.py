# -*- coding: utf-8 -*-

'''
Copyright © 2021  Bartłomiej Duda
License: GPL-3.0 License 
'''


# Program tested on Python 3.7.0
# This a is a rework of Duda's DW8 unpacker for DW5

# Ver    Date        Author               Comment
# v0.1   28.03.2021  Bartlomiej Duda      -

import os
import sys
import struct
import datetime


def bd_logger(in_str):
    '''
    Function for logging debug messages
    '''   
    now = datetime.datetime.now()
    print(now.strftime("%d-%m-%Y %H:%M:%S") + " " + in_str)    
   

def export_data(bin_in_file_path, idx_in_file_path, out_folder_path):
    '''
    Function for exporting data from BIN files
    '''    
    bd_logger("Starting export_data...")  
    
    if not os.path.exists(out_folder_path):
        os.makedirs(out_folder_path)      
    
    bin_file = open(bin_in_file_path, "rb")
    
    idx_file = open(idx_in_file_path, "rb")
    
    idx_size = os.path.getsize(idx_in_file_path)
    num_of_idx_entries = int(idx_size / 16) - 1
    section_start = 0
    f_count = 0
    idx_file.read(16)
    for i in range(num_of_idx_entries):
        Block1 = struct.unpack("<Q", idx_file.read(8))[0]
        Block2 = struct.unpack("<Q", idx_file.read(8))[0]
        section_start = (Block1& 0xffffffff)<<11
        comp_size = ((Block1&0xffffffff00000000) >>21)
        selection_end = Block2& 0xffffffff
        comp_flag = (Block2 >>32) & 0xffffffff
        # print("Block 2 "+ hex(Block2))
        # print("Comp size " + hex(comp_size))
        # print("<< Operation " + hex(temp1))
        # print("Offset from last = " + hex(temp2))
        # input()
        # print("Section Start " + hex(section_start))


        if comp_size != 0:
            f_count += 1            
            ext = ""

            if comp_flag == 1:
                ext = ".comp"
            else:
                ext = ".dat"
            bin_file.seek(section_start)
            ID = struct.unpack("<Q",bin_file.read(8))[0]
            if ID&0xffffffff == 0x53564F4B:
                ext = ".kovs"
            elif ID&0xffffffff == 0x47315447:
                ext = ".g1t"
            elif ID&0xffffffff == 0x324D4954:
                ext = ".tm2"
            elif ID&0xffffffff == 0x20336D74:
                ext = ".tm3"
            elif ID&0xffffffff == 0x32505A4C:
                ext = ".lzp"
            elif ID&0xffffffff == 0x47314d5f:
                ext = ".g1m_"
            elif ID&0xffffffff == 0x304b5042:
                ext = ".bpk"
            elif ID&0xffffffff == 0x4b5c484c:
                ext = ".lhsk"
            elif ID&0xffffffff == 0x4731415F:
                ext = ".g1a_"
            elif ID&0xffffffff == 0x6F6C675B:
                ext = ".lght"
            elif ID&0xffffffff == 0xC134CCCD:
                ext = ".weird"
            elif ID&0xffffffff == 0x4353454D:
                ext = ".strng"
            elif ID&0xffffffff == 0x20325350:
                ext = ".ps2"

            currentstart = section_start
            f_path = out_folder_path +str(f_count - 1).ljust(9)+hex(section_start) + ext 
            out_file = open(f_path, 'wb')
            bin_file.seek(currentstart)
            while selection_end > 0:
                if selection_end > 0xffff:
                    f_data = bin_file.read(0xffff)
                    out_file.write(f_data)
                    selection_end -= 0xffff
                else:
                    f_data = bin_file.read(selection_end)
                    out_file.write(f_data)
                    selection_end = 0
                #currentstart+=0xffff
            out_file.close()            
            f_path = out_folder_path + "file" + str(f_count) + ext 
            print(f_path)
   
    idx_file.close()
    bin_file.close()
    bd_logger("Ending export_data...")    
    
    
    
    
def main():
    '''
    Main function of this program. If you are planning to use it,
    you should adjust paths first.
    '''   
    main_switch = 1
    # 1 - data export 
    

    if main_switch == 1:
        p_bin_in_file_path = "E:\\Modding\\SSM4SPJa\\linkdata\\LINKDATA.BIN"
        p_idx_in_file_path = "E:\\Modding\\SSM4SPJa\\linkdata\\LINKDATA.IDX"
        p_out_folder_path =  "E:\\Modding\\SSM4SPJa\\STUFF\\LINKDATA0.BIN_OUT\\"
        export_data(p_bin_in_file_path, p_idx_in_file_path, p_out_folder_path)
        
    else:
        bd_logger("Wrong option selected!")
        
        
    
    bd_logger("End of main...")    
    
    
    
main()



# "E:\\Modding\\SSM4SPJa\\linkdata\\LINKDATA.BIN"
# "E:\\Modding\\SSM4SPJa\\linkdata\\LINKDATA.IDX"
# "E:\\Modding\\SSM4SPJa\\STUFF\\LINKDATA0.BIN_OUT\\"


# "E:\\Emulation\\Emulators\\iso\\dw5XL\\LINKDATA.BI
# "E:\\Emulation\\Emulators\\iso\\dw5XL\\LINKDATA.ID
# "E:\\Emulation\\Emulators\\iso\\dw5XL\\owow\\"




# "C:\\Users\\Malachi\\WorkDesktop\\Shin Sangokumusou 4 Special\\linkdata\\LINKDATA.BIN"
# "C:\\Users\\Malachi\\WorkDesktop\\Shin Sangokumusou 4 Special\\linkdata\\LINKDATA.IDX"
# "C:\\Users\\Malachi\\WorkDesktop\\Shin Sangokumusou 4 Special\\linkdata\\stoof\\"

# "E:\\Emulation\\Emulators\\iso\\dw5XL\\LINKDATA.BIN"
# "E:\\Emulation\\Emulators\\iso\\dw5XL\\LINKDATA.IDX"
# "E:\\Emulation\\Emulators\\iso\\dw5XL\\owow"


# "C:\\Users\\Malachi\\WorkDesktop\\Shin Sangokumusou 4 Special\\linkdata\\LINKDATA.BIN"    
# "C:\\Users\\Malachi\\WorkDesktop\\Shin Sangokumusou 4 Special\\linkdata\\LINKDATA.IDX"
# "C:\\Users\\Malachi\\WorkDesktop\\Shin Sangokumusou 4 Special\\STUFF\\LINKDATA.BIN_OUT\\"