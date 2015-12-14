from __future__ import division
from __future__ import print_function
import sys
import shutil
from os import environ
from os import getcwd
import string
import zlib
import bz2

import subprocess
import os
import glob
import random
random.seed()
from PIL import Image

import setComplexity
    
lowest = 1.0
highest = 0.0

#def getNcd(file1, file2, path):
#  global lowest
#  global highest

#  #size1 = os.path.getsize(file1)
#  #size2 = os.path.getsize(file2)
#  size1 = os.path.getsize(file1)
#  size2 = os.path.getsize(file2)

#  image1 = Image.open(file1)
#  image2 = Image.open(file2)

#  #x, y = image1.size
#  #newImage = Image.new(image1.mode, (x, y * 2))
#  #newImage.paste(image1, (0, 0))
#  #newImage.paste(image2, (0, y))
#  #newImage.save(path + "/testimage.png", "PNG")
#  ##newSize = os.path.getsize(path + "/testimage.png")
#  #newSize = getCSize(path + "/testimage.png")

#  x, y = image1.size
#  newImage = Image.new(image1.mode, (x * 2, y))
#  newImage.paste(image1, (0, 0))
#  newImage.paste(image2, (x, 0))
#  newImage.save(path + "/testimage.png", "PNG")
#  #newSize = os.path.getsize(path + "/testimage.png")
#  newSize = os.path.getsize(path + "/testimage.png")


#  #print(size1)
#  #print(size2)
#  #print(newSize)

#  print(newSize)
#  print(size1)
#  print(size2)

#  ncd = (newSize - min(size1, size2)) / (max(size1, size2))
#  if (ncd < lowest):
#    lowest = ncd
#    shutil.copyfile(path + "/testimage.png", path + "/lowest.png")
#  if (ncd > highest):
#    highest = ncd
#    shutil.copyfile(path + "/testimage.png", path + "/highest.png")

#  return ncd

#def getNcd2(file1, file2, path):
#  size1 = getCSize2(file1, path)
#  size2 = getCSize2(file2, path)

#  with open(path + "/concatFile.test", "wb") as outfile:
#    outfile.write(open(file1, "rb").read())
#    outfile.write(open(file2, "rb").read())
#    outfile.close()

#  newSize = getCSize2(path + "/concatFile.test", path)

#  print(size1)
#  print(size2)
#  print(newSize)

#  ncd = (newSize - min(size1, size2)) / (max(size1, size2))
#  return ncd


##def getDataCSize(data):
##  compressed = zlib.compress(data, 9)
##  with open(path + "/testC", "wb") as out_file:
##      out_file.write(compressed)

##  return os.path.getsize(path + "/testC")


#def getCSize(file, path):
#  with open(file, "rb") as in_file:
#    compressed = zlib.compress(in_file.read(), 9)

#  with open(path + "/testC", "wb") as out_file:
#      out_file.write(compressed)

#  return os.path.getsize(path + "/testC")

#def getCSize2(file, path):
#  with open(file, "rb") as in_file:
#    compressed = bz2.compress(in_file.read(), 9)

#  with open(path + "/testC", "wb") as out_file:
#      out_file.write(compressed)

#  return os.path.getsize(path + "/testC")

#def setComplexity(files, path):
#  #sumSize = sum([pair[1] for pair in files])
#  #print(sumSize)
#  sumFiles = 0
#  for file1 in files:
#    #size1 = os.path.getsize(file1)
#    size1 = os.path.getsize(file1)
#    #sumNcd = 0
#    for file2 in files:
#      if file1 != file2:
#        ncd = getNcd(file1, file2, path)
#        print(ncd)
#        #sumFiles += size1 * ncd * (1 - ncd)
#        sumFiles += ncd * (1 - ncd)
#    #sumFiles += (size1 * sumNcd)
#  print(sumFiles)
#  return (1 / (len(files) * (len(files) - 1))) * sumFiles

#def getFiles():
#  all_subdirs = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
#  latest_subdir = max(all_subdirs, key=os.path.getmtime)
#  #files = glob.glob(latest_subdir + "/**/*.png")
#  files = glob.glob(latest_subdir + "/**/*.vtk")
#  return files

if __name__ == "__main__":
  import shutil
  complexityList = []
  path = sys.argv[1]

  best = 0
  for i in range(55):
    
    files = glob.glob(path + "/" + str(i) + "-*/*.png")
    print(files)
    files.sort(key=os.path.getmtime)

    testoutput = open(path + "/testoutput.txt", "w")
    #numSets = len(files) - 4
    #for i in range(0, numSets):
    #  filesSet = files[i:i+4]
    #  if (i == numSets - 1):
    #    filesSet = files[-4:]
    #  print(setComplexity(filesSet), file=testoutput)
    complexity = setComplexity.setComplexity(files, path)
    print(complexity)
    if (complexity > best):
      best = complexity
      shutil.copyfile(files[0], path + "/Best.png")


  #numSets = len(files) - 2
  #for i in range(0, numSets):
  #  print(getNcd(files[i], files[i+1]), file=testoutput)

  #for file in files:
  #  print(1 / os.path.getsize(file), file=testoutput)
