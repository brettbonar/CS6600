
from PySteppables import *
import CompuCell
import sys
class NewSimulationSteppable(SteppableBasePy):    

    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)              
    #def step(self,mcs): 
    #    if (mcs >= 500):
    #        self.stopSimulation()

    def start(self):
        # any code in the start function runs before MCS=0
        pass
