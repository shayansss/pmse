from abaqus import *
from abaqusConstants import *
import displayGroupOdbToolset as dgo
import os
import numpy as np
import time


class MainTools(object):
    """
    A utility class for managing and interacting with ABAQUS output database (ODB) files and viewports.

    This class provides methods to:
    - Open an ODB file with error handling and retry mechanism.
    - Save and close an ODB file.
    - Set up and control viewport settings for displaying ODB data.

    Attributes:
        jobName (str): The name of the job associated with the ODB file.
        odbName (str): The name of the ODB file, derived from jobName.
        partName (str): The name of the part to be analyzed.
        modelName (str): The name of the model in the ABAQUS database.
        instanceName (str): The name of the instance within the model.
        mdb: The ABAQUS model database object.
        session: The ABAQUS session object.
        viewportObj1: The viewport object used for displaying ODB data.
    """

    def __init__(self, jobName, partName, instanceName, modelName, mdb, session, viewportObj1='Viewport: 1'):
        self.jobName = jobName
        self.odbName = jobName + '.odb'
        self.partName = partName
        self.modelName = modelName
        self.instanceName = instanceName
        self.mdb = mdb
        self.session = session
        self.viewportObj1 = self.session.viewports[viewportObj1]

    def open_odb(self, odbName, readOnly=True):
        """
        Open an ODB file with a retry mechanism in case of failure.
        """
        try:
            return self.session.openOdb(name=odbName, readOnly=readOnly)
        except Exception as e:
            time.sleep(5)
            print(f'open_odb() did not work: {e}')
            return self.session.openOdb(name=odbName, readOnly=readOnly)

    def save_and_close_odb(self, odbObj):
        """
        Save and close the ODB file.
        """
        odbObj.save()
        odbObj.close()


# Change the current working directory to the specified path and open the .cae file
os.chdir(r"C:\Temp\PointMSE")
FileName = 'abq'
openMdb(pathName=FileName + '.cae')
openMdb(pathName=FileName + '.cae')

# Initialize job, part, instance, and model names, and open an output database (ODB) file
jobName, partName, instanceName, modelName = 'Job', 'part', 'part', 'Model-1'
modelObj = mdb.models[modelName]
mt = MainTools(jobName, partName, instanceName, modelName, mdb, session)
odb = mt.open_odb(mt.odbName, readOnly=False)

# Configure the viewport settings for displaying the ODB and disable annotation options
viewportObj = session.viewports['Viewport: 1']
viewportObj.setValues(displayedObject=odb)
viewportObj.makeCurrent()
viewportObj.viewportAnnotationOptions.setValues(
    triad=OFF, legend=OFF, title=OFF, state=OFF, annotations=OFF, compass=OFF
)

# START OF AUTOMATICALLY GENERATED PYTHON CODE 1
path = "temp_visualization"
# END OF AUTOMATICALLY GENERATED PYTHON CODE 1

# Load data from the specified CSV file and reshape it
data = np.loadtxt(path, delimiter=",", dtype='float32')
data = data.reshape(-1, 1)

# Retrieve stress field data from the ODB for a specific region at the element nodal position
odbInstance = odb.rootAssembly.instances['PART']
Sarrays = odb.steps['static'].frames[-1].fieldOutputs['S'].getSubset(
    region=odbInstance, position=ELEMENT_NODAL).values
region = [i.nodeLabel for i in Sarrays]

# Generate a random field output name and add the reshaped data as a new field output to the ODB
name = 'temp_%s' % (np.random.random())
newFieldOutput = odb.steps['static'].frames[0].FieldOutput(
    name=name, description='', type=SCALAR)
newFieldOutput.addData(
    position=NODAL, instance=odbInstance, labels=region, data=data)
mt.save_and_close_odb(odb)
odb = mt.open_odb(mt.odbName, readOnly=False)

# Set the viewport to display the newly updated ODB and select the first step and frame
viewportObj = session.viewports['Viewport: 1']
viewportObj.setValues(displayedObject=odb)
viewportObj.makeCurrent()
viewportObj.odbDisplay.setFrame(step=0, frame=0)

# Set the contour plot display settings in the viewport
viewportObj.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF,))
leaf = dgo.LeafFromElementSets(elementSets=(' ALL ELEMENTS',))
viewportObj.odbDisplay.displayGroup.replace(leaf=leaf)

# START OF AUTOMATICALLY GENERATED PYTHON CODE 2
viewportObj.odbDisplay.contourOptions.setValues(maxAutoCompute=OFF, maxValue=4, minAutoCompute=OFF, minValue=0)
# END OF AUTOMATICALLY GENERATED PYTHON CODE 2

# Fit the view to the viewport, set contour display settings, and save the current viewport as an image
viewportObj.view.fitView()
viewportObj.odbDisplay.contourOptions.setValues(outsideLimitsMode=SPECTRUM)
viewportObj.odbDisplay.setPrimaryVariable(variableLabel=name, outputPosition=NODAL)
session.pngOptions.setValues(imageSize=(4000, 2536))
session.printOptions.setValues(reduceColors=False)
session.printToFile(fileName='%s' % (path), format=PNG, canvasObjects=(viewportObj,))
