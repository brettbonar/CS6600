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
import random
random.seed()
from PIL import Image
import CompuCellSetup
from XMLUtils import *
import CC3DXML
from CC3DXML import *
  
import copy

path = "C:/Dev/CS6600/Project/Test/Output/"
#path = "C:/Users/Brett/CC3DWorkspace"
simulationSize = 100
numCellTypes = random.randint(1, 2)
ncells = random.randint(100,200)

def randomFloatStr(start, end):
  return str(random.uniform(start, end))

def randomIntStr(start, end):
  return str(random.randint(start, end))

def addChemotaxis(CompuCell3DElmnt):
  PluginElmnt_4=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Chemotaxis"})
  # Select chemical field?
  ChemicalFieldElmnt=PluginElmnt_4.ElementCC3D("ChemicalField",{"Name":"FDS","Source":"DiffusionSolverFE"})
    
  # Define chemotaxis for cell type
  # TODO: iterate over cell types
  for cell in range(1, numCellTypes + 1):
      for cell2 in range(cell, numCellTypes + 1):
          if random.choice([True, False]):
              ChemicalFieldElmnt.ElementCC3D("ChemotaxisByType",{"ChemotactTowards":str(cell),"Lambda":str(random.uniform(2.0, 200000.0)),"Type":str(cell2)})
    
  # Define chemical field?
  SteppableElmnt=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"DiffusionSolverFE"})
  DiffusionFieldElmnt=SteppableElmnt.ElementCC3D("DiffusionField",{"Name":"FDS"})
  DiffusionDataElmnt=DiffusionFieldElmnt.ElementCC3D("DiffusionData")
  DiffusionDataElmnt.ElementCC3D("FieldName",{},"FDS")
  DiffusionDataElmnt.ElementCC3D("GlobalDiffusionConstant",{},"0.1")
  DiffusionDataElmnt.ElementCC3D("GlobalDecayConstant",{},"1e-05")
  DiffusionDataElmnt.ElementCC3D("DiffusionCoefficient",{"CellType":"Wall"},"0")
  DiffusionDataElmnt.ElementCC3D("DoNotDiffuseTo",{"CellType":"Wall"},"Wall")

  for cell in range(1, numCellTypes + 1):
    DiffusionDataElmnt.ElementCC3D("SecretionData",{"Type":str(cell)}, randomFloatStr(0.1, 100))

  BoundaryConditionsElmnt=DiffusionFieldElmnt.ElementCC3D("BoundaryConditions")
  PlaneElmnt=BoundaryConditionsElmnt.ElementCC3D("Plane",{"Axis":"X"})
  PlaneElmnt.ElementCC3D("ConstantValue",{"PlanePosition":"Min","Value":"10.0"})
  PlaneElmnt.ElementCC3D("ConstantValue",{"PlanePosition":"Max","Value":"5.0"})
  PlaneElmnt_1=BoundaryConditionsElmnt.ElementCC3D("Plane",{"Axis":"Y"})
  PlaneElmnt_1.ElementCC3D("ConstantDerivative",{"PlanePosition":"Min","Value":"10.0"})
  PlaneElmnt_1.ElementCC3D("ConstantDerivative",{"PlanePosition":"Max","Value":"5.0"})

def configureSimulation():    
  CompuCell3DElmnt=ElementCC3D("CompuCell3D",{"Revision":"20150808","Version":"3.7.4"})
  PottsElmnt=CompuCell3DElmnt.ElementCC3D("Potts")
  PottsElmnt.ElementCC3D("Dimensions",{"x":str(simulationSize),"y":str(simulationSize),"z":"1"})
  PottsElmnt.ElementCC3D("Steps",{},"1010")
  PottsElmnt.ElementCC3D("Temperature",{},"10.0")
  PottsElmnt.ElementCC3D("NeighborOrder",{},"2")
  PottsElmnt.ElementCC3D("RandomSeed",{},str(random.randint(1, 9999999)))
  SettingsPlugin=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"PlayerSettings"})
  SettingsPlugin.ElementCC3D("VisualControl",{"ScreenshotFrequency":"1000"})
  PluginElmnt=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CellType"})
  PluginElmnt.ElementCC3D("CellType",{"TypeId":"0","TypeName":"Medium"})
  PluginElmnt.ElementCC3D("CellType",{"TypeId":"9","TypeName":"Wall","Freeze":""})
    
  # Define cell types
  # TODO use variable ratio of cell types
  for cell in range(1, numCellTypes + 1):
      PluginElmnt.ElementCC3D("CellType",{"TypeId":str(cell),"TypeName":str(cell)})
    
  PluginElmnt_1=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Volume"})
    
  # Define volume for cell types
  for cell in range(1, numCellTypes + 1):
      width = random.randint(2, 5)
      PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":str(cell),"LambdaVolume": str(random.uniform(1.0, 2.0)),"TargetVolume": str(width * width)})
    
  PluginElmnt_2=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Surface"})
    
  # Define surface for cell types
  for cell in range(1, numCellTypes + 1):
      PluginElmnt_2.ElementCC3D("SurfaceEnergyParameters",{"CellType":str(cell),"LambdaSurface":str(random.uniform(1.0, 2.0)),"TargetSurface":str(random.randint(12, 25))})
    
  CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CenterOfMass"})
  PluginElmnt_3=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Contact"})
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"Medium"},"0.0")
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Wall","Type2":"Wall"},"0.0")
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Wall","Type2":"Medium"},"0.0")
    
  # Define contact for cell types
  for cell in range(1, numCellTypes + 1):
      PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":str(cell)},str(random.uniform(0, 30.0)))
      PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Wall","Type2":str(cell)},"50.0")
      for cell2 in range(cell, numCellTypes + 1):
          PluginElmnt_3.ElementCC3D("Energy",{"Type1":str(cell),"Type2":str(cell2)},str(random.uniform(0, 30.0)))
  PluginElmnt_3.ElementCC3D("NeighborOrder",{},"2")
    
  if random.choice([True, False]):
    addChemotaxis(CompuCell3DElmnt)

  # Define initialization parameters
  SteppableElmnt_1=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"RandomFieldInitializer"})
  SteppableElmnt_1.ElementCC3D("offset",{"x":"10","y":"10","z":"0"})
  SteppableElmnt_1.ElementCC3D("growthsteps",{},"10")
  SteppableElmnt_1.ElementCC3D("order",{},"2")
  SteppableElmnt_1.ElementCC3D("types",{},",".join(str(i) for i in range(1, numCellTypes + 1)))
  SteppableElmnt_1.ElementCC3D("ncells",{},str(ncells))
  #SteppableElmnt_1=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"UniformInitializer"})
  #RegionElmnt=SteppableElmnt_1.ElementCC3D("Region")
  #RegionElmnt.ElementCC3D("BoxMin",{"x":"10","y":"10","z":"0"})
  #RegionElmnt.ElementCC3D("BoxMax",{"x":str(simulationSize - 10),"y":str(simulationSize - 10),"z":"1"})
  #RegionElmnt.ElementCC3D("Gap",{},"5")
  #RegionElmnt.ElementCC3D("Width",{},str(width))
  #RegionElmnt.ElementCC3D("Types",{},",".join(str(i) for i in range(1, numCellTypes + 1)))
 
  CompuCell3DElmnt.CC3DXMLElement.saveXML("C:/Dev/CS6600/Project/Test/Simulation/NewSimulation.xml")
  return CompuCell3DElmnt

def cellSorting():
  import CompuCellSetup
  from XMLUtils import ElementCC3D
    
  CompuCell3DElmnt=ElementCC3D("CompuCell3D",{"Revision":"20150808","Version":"3.7.4"})
  PottsElmnt=CompuCell3DElmnt.ElementCC3D("Potts")
  PottsElmnt.ElementCC3D("Dimensions",{"x":str(simulationSize),"y":str(simulationSize),"z":"1"})
  PottsElmnt.ElementCC3D("Steps",{},"10010")
  PottsElmnt.ElementCC3D("Temperature",{},"10.0")
  PottsElmnt.ElementCC3D("NeighborOrder",{},"2")
  PottsElmnt.ElementCC3D("RandomSeed",{},str(random.randint(1, 9999999)))
  SettingsPlugin=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"PlayerSettings"})
  SettingsPlugin.ElementCC3D("VisualControl",{"ScreenshotFrequency":"100"})
  PluginElmnt=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CellType"})
  PluginElmnt.ElementCC3D("CellType",{"TypeId":"0","TypeName":"Medium"})
  PluginElmnt.ElementCC3D("CellType",{"TypeId":"1","TypeName":"1"})
  PluginElmnt.ElementCC3D("CellType",{"TypeId":"2","TypeName":"2"})
  
  PluginElmnt_1=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Volume"})
  PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":"1","LambdaVolume":"1.5","TargetVolume": "25"})
  PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":"2","LambdaVolume":"1.5"," TargetVolume": "25"})
  
  PluginElmnt_1=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Surface"})
  PluginElmnt_1.ElementCC3D("SurfaceEnergyParameters",{"CellType":"1","LambdaSurface":"1.5","TargetSurface": "25"})
  PluginElmnt_1.ElementCC3D("SurfaceEnergyParameters",{"CellType":"2","LambdaSurface":"1.5","TargetSurface": "25"})
    
  PluginElmnt_3=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Contact"})
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"Medium"},"0.0")
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"1"},"16.0")
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"1","Type2":"1"},"14.0")
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"2"},"16.0")
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"2","Type2":"2"},"2.0")
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"1","Type2":"2"},"11.0")
  PluginElmnt_3.ElementCC3D("NeighborOrder",{},"2")

  
  SteppableElmnt_1=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"RandomFieldInitializer"})
  SteppableElmnt_1.ElementCC3D("offset",{"x":"10","y":"10","z":"0"})
  SteppableElmnt_1.ElementCC3D("growthsteps",{},"10")
  SteppableElmnt_1.ElementCC3D("order",{},"2")
  SteppableElmnt_1.ElementCC3D("types",{},"1,2")
  SteppableElmnt_1.ElementCC3D("ncells",{},str(ncells))

  return CompuCell3DElmnt

def randomWalk(node):
  converter = Xml2Obj()
  newNode = converter.ParseString(node)
  #newNode = Xml2Obj().Parse("C:/Dev/CS6600/Project/Test/Simulation/NewSimulation.xml")
  cellType1 = random.randint(1, numCellTypes + 1)
  print(numCellTypes)
  print(cellType1)
  type1 = str(cellType1)
  if cellType1 > numCellTypes:
    type1 = "Medium"
  cellType2 = randomIntStr(1, numCellTypes)
  type2 = str(cellType2)
  contact = newNode.getFirstElement("Plugin", CC3DXML.MapStrStr({"Name": "Contact"}))
  updateNode = contact.getFirstElement("Energy", CC3DXML.MapStrStr({ "Type1":type1, "Type2":type2 }))
  if updateNode == None:
    updateNode = contact.getFirstElement("Energy", CC3DXML.MapStrStr({ "Type1":type2, "Type2":type1 }))
  updateNode.updateElementValue(randomFloatStr(0, 30.0))
  newNode.saveXML("C:/Dev/CS6600/Project/Test/Simulation/NewSimulation.xml")

  print(type1)
  print(type2)
  
  return newNode.getCC3DXMLElementString()
    
def getFiles():
  all_subdirs = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
  latest_subdir = max(all_subdirs, key=os.path.getmtime)
  files = glob.glob(latest_subdir + "/*.png")
  #files.sort(key=os.path.getmtime)
  return files

def testNode(node):
  #xmlFile = open("C:/Dev/CS6600/Project/Test/Simulation/NewSimulation.xml", "w+")
  #xmlFile.write(node.getCC3DXMLElementString())
  #xmlFile.close()
  subprocess.call("C:/CompuCell3D/compucell3d.bat -i C:\\Dev\\CS6600\\Project\\Test\\Test.cc3d --exitWhenDone")
  file = max(getFiles(), key=os.path.getmtime)
  return os.path.getsize(file)

def run():
  element = configureSimulation()
  currentNode = element.CC3DXMLElement.getCC3DXMLElementString()
  currentComplexity = 100
  #currentComplexity = testNode(currentNode)
  #currentNode = cellSorting()
  #newNode = randomWalk(currentNode)

  #for i in range(9):
    #currentNode.CC3DXMLElement.getFirstElement("Potts").getFirstElement("RandomSeed").updateElementValue(str(random.randint(1, 9999999)))
    #testNode(currentNode)

  for i in range(50):
    newNode = randomWalk(currentNode)
    #newComplexity = testNode(newNode)
    newComplexity = currentComplexity - 1
    if (newComplexity < currentComplexity):
      currentNode = newNode
      currentComplexity = newComplexity


run()
#file2, size2 = run()
#print(setComplexity(files))
#file = max(files, key=os.path.getmtime)
#print(os.path.getsize(file))
