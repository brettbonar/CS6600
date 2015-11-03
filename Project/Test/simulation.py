from __future__ import division
import sys
from os import environ
from os import getcwd
import string

sys.path.append(environ["PYTHON_MODULE_PATH"])
sys.path.append(environ["SWIG_LIB_INSTALL_DIR"])

import subprocess
import os
import glob
from PIL import Image

#path = "C:/Dev/CS6600/Project/Test/Output/"
path = "C:/Users/Brett/CC3DWorkspace"
simulationSize = 100


def configureSimulation():
  import random
  random.seed()
  import CompuCellSetup
  from XMLUtils import ElementCC3D
    
  numCellTypes = random.randint(1, 3)
    
  CompuCell3DElmnt=ElementCC3D("CompuCell3D",{"Revision":"20150808","Version":"3.7.4"})
  PottsElmnt=CompuCell3DElmnt.ElementCC3D("Potts")
  PottsElmnt.ElementCC3D("Dimensions",{"x":str(simulationSize),"y":str(simulationSize),"z":"1"})
  PottsElmnt.ElementCC3D("Steps",{},"1010")
  PottsElmnt.ElementCC3D("Temperature",{},"10.0")
  PottsElmnt.ElementCC3D("NeighborOrder",{},"2")
  PluginElmnt=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CellType"})
  PluginElmnt.ElementCC3D("CellType",{"TypeId":"0","TypeName":"Medium"})
    
  # Define cell types
  # TODO use variable ratio of cell types
  for cell in range(1, numCellTypes + 1):
      PluginElmnt.ElementCC3D("CellType",{"TypeId":str(cell),"TypeName":str(cell)})
    
  PluginElmnt_1=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Volume"})
    
  # Define volume for cell types
  width = 5
  for cell in range(1, numCellTypes + 1):
      PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":str(cell),"LambdaVolume": str(random.uniform(1.0, 2.0)),"TargetVolume": str(width * width)})
    
  PluginElmnt_2=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Surface"})
    
  # Define surface for cell types
  for cell in range(1, numCellTypes + 1):
      PluginElmnt_2.ElementCC3D("SurfaceEnergyParameters",{"CellType":str(cell),"LambdaSurface":str(random.uniform(1.0, 2.0)),"TargetSurface":str(random.randint(12, 25))})
    
  CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CenterOfMass"})
  PluginElmnt_3=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Contact"})
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"Medium"},"0.0")
    
  # Define contact for cell types
  for cell in range(1, numCellTypes + 1):
      PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":str(cell)},"16.0")
      for cell2 in range(cell, numCellTypes + 1):
          PluginElmnt_3.ElementCC3D("Energy",{"Type1":str(cell),"Type2":str(cell2)},str(random.uniform(-10, 14.0)))
  PluginElmnt_3.ElementCC3D("NeighborOrder",{},"2")
    
  PluginElmnt_4=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Chemotaxis"})
  # Select chemical field?
  ChemicalFieldElmnt=PluginElmnt_4.ElementCC3D("ChemicalField",{"Name":"FDS","Source":"FlexibleDiffusionSolverFE"})
    
  # Define chemotaxis for cell type
  # TODO: iterate over cell types
  if random.choice([True, False]):
      for cell in range(1, numCellTypes + 1):
          for cell2 in range(cell, numCellTypes + 1):
              if random.choice([True, False]):
                  ChemicalFieldElmnt.ElementCC3D("ChemotaxisByType",{"ChemotactTowards":str(cell),"Lambda":str(random.uniform(2.0, 300.0)),"Type":str(cell2)})
    
  # Define chemical field?
  SteppableElmnt=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"FlexibleDiffusionSolverFE"})
  DiffusionFieldElmnt=SteppableElmnt.ElementCC3D("DiffusionField",{"Name":"FDS"})
  DiffusionDataElmnt=DiffusionFieldElmnt.ElementCC3D("DiffusionData")
  DiffusionDataElmnt.ElementCC3D("FieldName",{},"FDS")
  DiffusionDataElmnt.ElementCC3D("DiffusionConstant",{},"0.1")
  DiffusionDataElmnt.ElementCC3D("DecayConstant",{},"1e-05")
  BoundaryConditionsElmnt=DiffusionFieldElmnt.ElementCC3D("BoundaryConditions")
  PlaneElmnt=BoundaryConditionsElmnt.ElementCC3D("Plane",{"Axis":"X"})
  PlaneElmnt.ElementCC3D("ConstantValue",{"PlanePosition":"Min","Value":"10.0"})
  PlaneElmnt.ElementCC3D("ConstantValue",{"PlanePosition":"Max","Value":"5.0"})
  PlaneElmnt_1=BoundaryConditionsElmnt.ElementCC3D("Plane",{"Axis":"Y"})
  PlaneElmnt_1.ElementCC3D("ConstantDerivative",{"PlanePosition":"Min","Value":"10.0"})
  PlaneElmnt_1.ElementCC3D("ConstantDerivative",{"PlanePosition":"Max","Value":"5.0"})
    
  # Define initialization parameters
  SteppableElmnt_1=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"UniformInitializer"})
  RegionElmnt=SteppableElmnt_1.ElementCC3D("Region")
  RegionElmnt.ElementCC3D("BoxMin",{"x":"0","y":"0","z":"0"})
  RegionElmnt.ElementCC3D("BoxMax",{"x":str(simulationSize),"y":str(simulationSize),"z":"1"})
  RegionElmnt.ElementCC3D("Gap",{},"5")
  RegionElmnt.ElementCC3D("Width",{},str(width))
  RegionElmnt.ElementCC3D("Types",{},",".join(str(i) for i in range(1, numCellTypes + 1)))
 
  xmlFile = open("C:/Dev/CS6600/Project/Test/Simulation/NewSimulation.xml", "w+")
  xmlFile.write(CompuCell3DElmnt.getCC3DXMLElementString())
  xmlFile.close()
  return CompuCell3DElmnt
    
def getNcd(file1, size1, file2, size2):
  image1 = Image.open(file1)
  image2 = Image.open(file2)

  x, y = image1.size
  newImage = Image.new(image1.mode, (x, y * 2))
  newImage.paste(image1, (0, 0))
  newImage.paste(image2, (0, y))
  newImage.save(path + "/testimage.png", "PNG")
  newSize = os.path.getsize(path + "/testimage.png")

  ncd = (newSize - min(size1, size2)) / (max(size1, size2))
  return ncd

def setComplexity(files):
  sumSize = sum([pair[1] for pair in files])
  print(sumSize)
  sumNcd = 0
  for file1, size1 in files:
    for file2, size2 in files:
      if file1 != file2:
        ncd = getNcd(file1, size1, file2, size2)
        sumNcd += (ncd * (1 - ncd))
  print(sumNcd)
  return (1 / (len(files) * (len(files) - 1))) * sumSize * sumNcd

def getSize():
  all_subdirs = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
  latest_subdir = max(all_subdirs, key=os.path.getmtime)
  file = glob.glob(latest_subdir + "/*.png")[0]
  size = os.path.getsize(glob.glob(latest_subdir + "/*.png")[0])
  return file, size

def run():
  subprocess.call("C:/CompuCell3D/compucell3d.bat -i C:\\Dev\\CS6600\\Project\\Test\\Test.cc3d --exitWhenDone")
  return getSize()

configureSimulation()
file1, size1 = run()
print(size1)
#file2, size2 = run()
#print(setComplexity([(file1, size1), (file2, size2)]))
