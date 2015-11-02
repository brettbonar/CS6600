import sys
from os import environ
from os import getcwd
import string

sys.path.append(environ["PYTHON_MODULE_PATH"])

import CompuCellSetup

sim,simthread = CompuCellSetup.getCoreSimulationObjects()
from configureSimulation import *
xml = configureSimulation(sim)

xmlFile = open("C:/Dev/CS6600/Project/Test/Output/simulation.xml", "w+")
xmlFile.write(xml.getCC3DXMLElementString())
xmlFile.close()

            
# add extra attributes here
            
CompuCellSetup.initializeSimulationObjects(sim,simthread)
# Definitions of additional Python-managed fields go here
        
#Add Python steppables here
steppableRegistry=CompuCellSetup.getSteppableRegistry()
        
from NewSimulationSteppables import NewSimulationSteppable
steppableInstance=NewSimulationSteppable(sim,_frequency=1000)
steppableRegistry.registerSteppable(steppableInstance)
        
CompuCellSetup.mainLoop(sim,simthread,steppableRegistry)
