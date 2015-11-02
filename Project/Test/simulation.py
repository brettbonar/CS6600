import subprocess
import os
import glob
from PIL import Image

path = "C:/Dev/CS6600/Project/Test/Output/"

#file2, size2 = run()

#print(size1)
#print(size2)

#image1 = Image.open(file1)
#image2 = Image.open(file2)

#x, y = image1.size
#newImage = Image.new(image1.mode, (x, y * 2))
#newImage.paste(image1, (0, 0))
#newImage.paste(image2, (0, y))
#newImage.save(path + "/testimage.png", "PNG")
#newSize = os.path.getsize(path + "/testimage.png")

#ncd = (newSize - min(size1, size2)) / (max(size1, size2))
#print(newSize)
#print(ncd)

def getSize():
  all_subdirs = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
  latest_subdir = max(all_subdirs, key=os.path.getmtime)
  file = glob.glob(latest_subdir + "/*.png")[0]
  size = os.path.getsize(glob.glob(latest_subdir + "/*.png")[0])
  return file, size

def run():
  subprocess.call("C:/CompuCell3D/compucell3d.bat -i C:\\Dev\\CS6600\\Project\\Test\\Simulation\\NewSimulation.py --exitWhenDone")
  return getSize()

file1, size1 = run()
print(size1)