

def configureSimulation(sim):
    import random
    random.seed()
    import CompuCellSetup
    from XMLUtils import ElementCC3D
    
    numCellTypes = random.randint(1, 3)
    
    CompuCell3DElmnt=ElementCC3D("CompuCell3D",{"Revision":"20150808","Version":"3.7.4"})
    PottsElmnt=CompuCell3DElmnt.ElementCC3D("Potts")
    PottsElmnt.ElementCC3D("Dimensions",{"x":"100","y":"100","z":"1"})
    PottsElmnt.ElementCC3D("Steps",{},"10000")
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
    for cell in range(1, numCellTypes + 1):
        PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":str(cell),"LambdaVolume": str(random.uniform(1.0, 2.0)),"TargetVolume": str(random.randint(1, 25))})
    
    PluginElmnt_2=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Surface"})
    
    # Define surface for cell types
    for cell in range(1, numCellTypes + 1):
        PluginElmnt_2.ElementCC3D("SurfaceEnergyParameters",{"CellType":str(cell),"LambdaSurface":str(random.uniform(1.0, 2.0)),"TargetSurface":str(random.randint(1, 25))})
    
    CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CenterOfMass"})
    PluginElmnt_3=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Contact"})
    PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"Medium"},"10.0")
    
    # Define contact for cell types
    for cell in range(1, numCellTypes + 1):
        PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":str(cell)},"16.0")
        for cell2 in range(cell + 1, numCellTypes + 1):
            PluginElmnt_3.ElementCC3D("Energy",{"Type1":str(cell),"Type2":str(cell2)},str(random.uniform(2.0, 16.0)))
    PluginElmnt_3.ElementCC3D("NeighborOrder",{},"1")
    
    PluginElmnt_4=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Chemotaxis"})
    # Select chemical field?
    ChemicalFieldElmnt=PluginElmnt_4.ElementCC3D("ChemicalField",{"Name":"FDS","Source":"FlexibleDiffusionSolverFE"})
    
    # Define chemotaxis for cell type
    # TODO: iterate over cell types
    ChemicalFieldElmnt.ElementCC3D("ChemotaxisByType",{"ChemotactTowards":"1","Lambda":"300.0","Type":"1"})
    
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
    RegionElmnt.ElementCC3D("BoxMin",{"x":"20","y":"20","z":"0"})
    RegionElmnt.ElementCC3D("BoxMax",{"x":"80","y":"80","z":"1"})
    RegionElmnt.ElementCC3D("Gap",{},"0")
    RegionElmnt.ElementCC3D("Width",{},"5")
    print("STRING: " + ",".join(str(i) for i in range(1, numCellTypes + 1)))
    RegionElmnt.ElementCC3D("Types",{},",".join(str(i) for i in range(1, numCellTypes + 1)))

    CompuCellSetup.setSimulationXMLDescription(CompuCell3DElmnt)    
    


import sys
from os import environ
from os import getcwd
import string

sys.path.append(environ["PYTHON_MODULE_PATH"])


import CompuCellSetup


sim,simthread = CompuCellSetup.getCoreSimulationObjects()
configureSimulation(sim)
            
# add extra attributes here
            
CompuCellSetup.initializeSimulationObjects(sim,simthread)
# Definitions of additional Python-managed fields go here
        
#Add Python steppables here
steppableRegistry=CompuCellSetup.getSteppableRegistry()
        
from NewSimulationSteppables import NewSimulationSteppable
steppableInstance=NewSimulationSteppable(sim,_frequency=1)
steppableRegistry.registerSteppable(steppableInstance)
        
CompuCellSetup.mainLoop(sim,simthread,steppableRegistry)
        
        