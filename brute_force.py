from pcraster import *
from pcraster.framework import *
from build_model import MyFirstModel
import pandas

'''
Calibrates a simulation model on a set of parameters.
Imports model from build_model.py

Inputs
------
simulation model: MyFirstModel object
    dynamic model
streamflow : txt
    the observed streamflow
    
Parameters
----------
nrOfTimeSteps: int
    number of timesteps for model to run
range of values: list
    range of values for each paramter to do the calibration

Output
------
mse:  float
    mean square error for the calibrated model
'''

# helper function 1 to read values from a map
def getCellValue(Map, Row, Column):
    Value, Valid=cellvalue(Map, Row, Column)
    if Valid:
        return Value
    else:
        raise RuntimeError("missing value in input of getCellValue")

# helper function 2 to read values from a map
def getCellValueAtBooleanLocation(location,map):
# map can be any type, return value always float
    valueMap=mapmaximum(ifthen(location,scalar(map)))
    value=getCellValue(valueMap,1,1)
    return value


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


# function to create series of parameter values for which model is run
def createParValues(lower,upper,nrSteps):
    step = (upper - lower)/(nrSteps-1)
    return(numpy.arange(lower,upper + step, step))

# create melt rate parameters for which model is run; best one is --> 0.009 , MeanSquareError = 2.937
meltRateParameters = createParValues(0.0, 0.02, 21)

# create temperatureLapseRate parameter for which model is run; best one is --> 0.004, MeanSquareError = 2.618
temperatureLapseRateParameters = createParValues(0.0, 0.01, 21)

# create seepageProportion parameter for which model is run; best one is --> 0.04, MeanSquareError = 2.452
seepageProportionParameters = createParValues(0.0, 0.1, 21)

# create atmosphericLoss parameter for which model is run; best one is --> 0.002, MeanSquareError = 2.452
atmosphericLossParameters = createParValues(0.0, 0.005, 21)

# create infiltration parameter for which model is run; best one is --> 0.003, MeanSquareError = 2.222
infiltrationParameters = createParValues(0.0, 0.01, 21)

print("model will be run for values of infiltration: ", meltRateParameters)

f = open("calibration_.txt", "w")

# calibrate one parameter and keep the rest stable
meltRateParameter = 0.003 # optimal -> 0.009   
temperatureLapseRateParameter = 0.005 # optimal -> 0.004
seepageProportionParameter = 0.06 # optimal -> 0.04
atmosphericLossParameter = 0.002 # optimal -> 0.002
infiltrationParameter = 0.003 # optimal -> 0.0018

# calibrate one parameter each time
for meltRateParameter in meltRateParameters:
    myModel = MyFirstModel(meltRateParameter,temperatureLapseRateParameter, seepageProportionParameter, atmosphericLossParameter, infiltrationParameter)
    dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
    dynamicModel.setQuiet()
    dynamicModel.run()

    # obtain modelled streamflow  
    streamFlowModelled = myModel.simulation
    # calculate objective function, i.e. mean of sum of squares and ignore first year
    SS = numpy.mean((streamFlowModelled[365:] - streamFlowObserved[365:])**2.0)
    print("infiltrationParameter: ", meltRateParameter, ", mean squared error: ", SS)
    f.write(str(meltRateParameter) + " " + str(SS) + "\n")
    
f.close()
import matplotlib.pyplot as plt

# read the calibration results file
file = open("calibration_infiltrationParameter.txt", "r")
lines = file.readlines()

parValues = []
goalValues = []
for line in lines:
    splitted = str.split(line)
    parValues.append(float(splitted[0]))
    goalValues.append(float(splitted[1]))
file.close()

f = plt.figure()
plt.plot(parValues,goalValues)
plt.xlabel("parameter value")
plt.ylabel("RMSE")
f.savefig("plot_calibration_one_par_results.pdf")