import sys
from os import environ
from os import getcwd
import string

sys.path.append(environ["PYTHON_MODULE_PATH"])

import CompuCellSetup
import RestartManager

sim,simthread = CompuCellSetup.getCoreSimulationObjects()
            
# add extra attributes here
            
CompuCellSetup.initializeSimulationObjects(sim,simthread)
# Definitions of additional Python-managed fields go here
        
#Add Python steppables here
steppableRegistry=CompuCellSetup.getSteppableRegistry()
        
from NewSimulationSteppables import NewSimulationSteppable
steppableInstance=NewSimulationSteppable(sim,_frequency=100)
steppableRegistry.registerSteppable(steppableInstance)

CompuCellSetup.mainLoop(sim,simthread,steppableRegistry)

#sim.finish()
#sim.cleanAfterSimulation()
#sim.unloadModules()

import time
time.sleep(5) # delays for 5 seconds

#self.run()

#import sys
#from os import environ
#from os import getcwd
#import string

#sys.path.append(environ["PYTHON_MODULE_PATH"])

#import CompuCellSetup

#sim,simthread = CompuCellSetup.getCoreSimulationObjects()
##sim.setRestartEnabled(True)
            
## add extra attributes here
            
#CompuCellSetup.initializeSimulationObjects(sim,simthread)
## Definitions of additional Python-managed fields go here
        
##Add Python steppables here
#steppableRegistry=CompuCellSetup.getSteppableRegistry()
        
#from NewSimulationSteppables import NewSimulationSteppable
#steppableInstance=NewSimulationSteppable(sim,_frequency=100)
#steppableRegistry.registerSteppable(steppableInstance)
        
#CompuCellSetup.mainLoop(sim,simthread,steppableRegistry)