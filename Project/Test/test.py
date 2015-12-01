from __future__ import division
from __future__ import print_function
import sys
from os import environ
from os import getcwd
import string

import subprocess
import os
import glob
import random

path = sys.argv[1]
files = glob.glob(path + "/**/*.png")
files.sort(key=os.path.getmtime)

#print(files)
complexityList = []

xmlFile = open("C:/Dev/CS6600/Project/Test/chart.txt", "w+")
best = os.path.getsize(files[0])
for file in files:
  complexityList.append(os.path.getsize(file))
  size = os.path.getsize(file)
  if (size < best):
    best = size
  print(str(os.path.getsize(file)), file=xmlFile)
  #print(str(best), file=xmlFile)
  
xmlFile.close()
