
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
        #sim.start()


    def start(self):
      # any code in the start function runs before MCS=0
      self.buildWall(self.WALL)
      #print("test")
