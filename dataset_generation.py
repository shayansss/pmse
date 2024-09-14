from abaqus import *
from abaqusConstants import *
import time
import os
import numpy as np
import time

class main_tools(object):
    def __init__(self, jobName, partName, instanceName, modelName, mdb, session, viewportObj1 = 'Viewport: 1'):
        self.jobName = jobName
        self.odbName = jobName + '.odb'
        self.partName = partName
        self.modelName = modelName
        self.instanceName = instanceName
        self.mdb = mdb
        self.session = session
        self.viewportObj1 = self.session.viewports[viewportObj1]
    
    def job_submit(self, jobName):
        FirstJob = self.mdb.jobs[jobName]
        FirstJob.submit(consistencyChecking=OFF)
        FirstJob.waitForCompletion()
    
    def open_odb(self, odbName, readOnly = True):
        try:
            return self.session.openOdb(name = odbName, readOnly = readOnly)
        except:
            time.sleep(5)
            print 'open_odb() did not work.'
            return self.session.openOdb(name = odbName, readOnly = readOnly)
    
    def close_odb(self, odbName = ''):
        if odbName == '': odbName = self.odbName
        try:
            self.session.odbs[odbName].close()
        except:
            print 'close_odb did not work.'
    

# Basic settings
inputPath = 'input_2d.csv'
outputPath = 'output_2d.csv'
iterationNumber = 200

# Open CAE file
os.chdir(r"C:\Temp\PointMSE")
FileName = 'abq'
openMdb(pathName = FileName + '.cae')
mdb.saveAs(pathName = FileName + '-Backup.cae')
openMdb(pathName=FileName + '.cae')


# Start model
jobName, partName, instanceName, modelName = 'Job', 'part', 'part', 'Model-1'
mt = main_tools(jobName, partName, instanceName, modelName, mdb, session) # main tools of Abaqus
modelObj = mdb.models[modelName]


# Design of experiments
np.random.seed(41)
u1List = np.random.uniform(-3.0,3.0,iterationNumber)
np.random.seed(42)
u2List = np.random.uniform(-0.1,-3,iterationNumber)
np.random.seed(43)
c10List = np.random.uniform(0.001,1000.0,iterationNumber)

# Generate data
i = 0
t = 0
for u1, u2, c10 in zip(u1List, u2List, c10List):
	i += 1
	
	modelObj.boundaryConditions['indenter'].setValuesInStep(stepName='static', u1 = u1, u2 = u2)
	modelObj.materials['Material'].hyperelastic.setValues(table=((c10, 0.0), ))
	temp = np.array([[u1, u2 ,c10, i]], dtype="float32")
	with open(inputPath, 'a') as inputFile: np.savetxt(inputFile, temp, delimiter=",")
	
	t0 = time()
	mt.job_submit(jobName)
	t1 = time()
	with open('time_' + outputPath, 'a') as outputFile: np.savetxt(outputFile, [t1 - t0], delimiter=",")
	
	odb = mt.open_odb(mt.odbName)
	frameObjT = odb.steps['static'].frames[-1]
	
	region = odb.rootAssembly.instances['PART']
	Sarrays = frameObjT.fieldOutputs['S'].getSubset(region = region, position = ELEMENT_NODAL).values
	
	temp = []
	for S in Sarrays:
		temp.append(np.array([S.data[1], i], dtype="float32"))
	
	temp = np.array(temp, dtype="float32")
	with open(outputPath, 'a') as outputFile: np.savetxt(outputFile, temp, delimiter=",")
	
	print i, temp.shape
	
	mt.close_odb()
