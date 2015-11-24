
from PySteppables import *
import CompuCell
import sys
class NewSimulationSteppable(SteppableBasePy):    

    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)   
        #self.simulator = simulator           
    #def step(self,mcs): 
        #if (mcs >= 200):
          #self.stopSimulation()
          #self.simulator.finish()
          #self.simulator.cleanAfterSimulation()
          #self.simulator.unloadModules()
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
          #sim.start()


    def start(self):
        # any code in the start function runs before MCS=0
        #self.buildWall(self.WALL)
        print("test")
