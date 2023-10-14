# DW5Tools
 Tools in python to access datafiles in KOEI game Dynasty warriors 5
 The main tool of note is the lzp2Extract file which is a successful reverse engineering of the decompression algorithm for files with the LZP2 header in the game files.

## Unpacking LZP2 files
 use lzp2Extract.py
 ```
 python lzp2Extract.py /inputfile /outputDirectory/
 ```
This works with the English, Japanese, and Chinese versions of the game files.
