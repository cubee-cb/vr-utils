#!/usr/bin/env python3

import sys
import re
from os import walk

# use argument as path
if len(sys.argv) > 1:
  mypath = sys.argv[1]
  print("Searching in " + mypath)
else:
  print("No path specified.")
  print("Run as: script.py ./path/to/folder/")
  exit()

# https://stackoverflow.com/a/3207973
# get a list of all files inside a folder, including subdirs
f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)

#print(f)

if len(f) == 0:
  print("No files found.")
  exit()

outstring = ""
charset = "cp1252"
output_file = "protv_playlist.txt"

# build ProTV3 playlist file from list based on yt-dlp filename format "<video name> [vidid_11chr]"
for filename in f:

  # skip file if there is not a square bracket section
  if not '[' in filename:
    continue;
  
  # extract video id and name from filename
  id_list = re.findall("\\[(.{11})\\]", filename)
  name = filename[0 : filename.index('[')].strip().replace('\u3010', '(').replace('\u3011', ')')

  # skip names that are empty like if they just had a square bracket in the name but not a video id
  if len(name) == 0 or len(id_list) == 0:
    continue;

  # build entry using last found id (in case filename has multiple; yt-dlp puts it at the end)
  id = id_list[-1]
  outstring += "@https://www.youtube.com/watch?v=" + id + "\n" + "~" + name + "\n\n"

print(outstring)

# write output to file, replacing invalid chars with '?'
with open(output_file, "w") as file:
  file.write(outstring.encode(charset, 'replace').decode(charset))

print("Wrote to " + output_file)
