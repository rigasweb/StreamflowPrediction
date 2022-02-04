from pcraster import *
from pcraster.framework import *
from build_model import MyFirstModel
import matplotlib.pyplot as plt

'''
Plots the observed and the simulated streamflow

Inputs
------
simulation model: MyFirstModel object
    dynamic model
streamflow : txt
    the observed streamflow

Parameters
----------
paramater set: int list
    value for each one of the parameters
nrOfTimeSteps: int
    number of timesteps for model to run
    
Output
------
plot of observed & simulated streamflow
'''

# choose the optimal paramaters
meltRateParameter =0.009 #initial value 0.003     
temperatureLapseRateParameter = 0.004 #initial value 0.005
seepageProportionParameter = 0.04 # initial value 0.06 
atmosphericLossParameter = 0.002 # initial value 0.002
infiltrationParameter =0.003 # initial value 0.0018

nrOfTimeSteps=1461
# read the observed streamflow from disk and store in numpy array
streamFlowObservedFile = open("streamflow.txt", "r")
streamFlowObserved = numpy.zeros(nrOfTimeSteps)
streamFlowObservedFileContent = streamFlowObservedFile.readlines()
for i in range(0,nrOfTimeSteps):
    splitted = str.split(streamFlowObservedFileContent[i])
    dischargeModelled = splitted[1]
    streamFlowObserved[i]=float(dischargeModelled)
streamFlowObservedFile.close()

# build dynamic model
myModel = MyFirstModel(meltRateParameter,temperatureLapseRateParameter, seepageProportionParameter, atmosphericLossParameter, infiltrationParameter)
dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
dynamicModel.setQuiet()
dynamicModel.run()

# obtain modelled streamflow  
streamFlowModelled = myModel.simulation
# calculate objective function, i.e. mean of sum of squares and ignore first year
SS = numpy.mean((streamFlowModelled[1095:] - streamFlowObserved[1095:])**2.0)
print(SS)

plt.plot(streamFlowModelled[1095:], color = 'b')
plt.plot(streamFlowObserved[1095:], color = "r")
plt.show()