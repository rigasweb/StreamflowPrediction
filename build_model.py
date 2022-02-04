from pcraster import *
from pcraster.framework import *

'''
Creates a dynamic model for streamflow simulation.

Inputs
------
precipitation: txt
    input for the simulation model
temperature: txt
    input for the simulation model

Parameters
----------
meltRateParameter: float
    rate that snows melts
temperatureLapseRate : float
    rate that temperature drops with altitude
seepageProportion : float
    proportion of subsurface water that seeps out to surface water
atmosphericLoss : float
    potential loss of water to the atmosphere
infiltrationParameter : float
    infiltration capacity
    
Output
------
streamflow
'''

class MyFirstModel(DynamicModel):
    def __init__(self, meltRateParameter, temperatureLapseRate, seepageProportion, atmosphericLoss, infiltrationParameter):
        DynamicModel.__init__(self)
        setclone("clone.map")

        # assign "external" input to the model variable
        self.meltRateParameter = meltRateParameter 
        self.temperatureLapseRate = temperatureLapseRate
        # proportion of subsurface water that seeps out to surface water per day
        self.seepageProportion =  seepageProportion
        # potential loss of water to the atmosphere (m/day)
        self.atmosphericLoss = atmosphericLoss
        # infiltration capacity parameter
        self.infiltrationParameter = infiltrationParameter
        
    def initial(self):
        self.clone = self.readmap("clone")
    
        dem = self.readmap("dem")
    
        # elevation (m) of the observed meteorology, this is taken from the
        # reanalysis input data set
        elevationMeteoStation = 1180.0
        elevationAboveMeteoStation = dem - elevationMeteoStation
 
        self.temperatureCorrection = elevationAboveMeteoStation * self.temperatureLapseRate
        
        # infiltration capacity, m/day
        self.infiltrationCapacity = scalar(self.infiltrationParameter * 24.0)
        
        # amount of water in the subsurface water (m), initial value
        self.subsurfaceWater = 0.0
    
        # amount of upward seepage from the subsurface water (m/day), initial value
        self.upwardSeepage = 0.0
        
        # snow thickness (m), initial value
        self.snow = 0.0
    
        # flow network
        self.ldd = self.readmap("ldd")
    
        # location where streamflow is measured (and reported by this model)
        self.sampleLocation = self.readmap("sample_location")
    
        # initialize streamflow timeseries for directly writing to disk
        self.runoffTss = TimeoutputTimeseries("streamflow_modelled", self, self.sampleLocation, noHeader=True)
        # initialize streamflow timeseries as numpy array for directly writing to disk
        self.simulation = numpy.zeros(self.nrTimeSteps())
    
    
    def dynamic(self):
        precipitation = timeinputscalar("precipitation.txt",self.clone)/1000.0
        temperatureObserved = timeinputscalar("temperature.txt",self.clone)
        temperature = temperatureObserved - self.temperatureCorrection
    
        freezing=temperature < 0.0
        snowFall=ifthenelse(freezing,precipitation,0.0)
        rainFall=ifthenelse(pcrnot(freezing),precipitation,0.0)
    
        self.snow = self.snow+snowFall
        
        potentialMelt = ifthenelse(pcrnot(freezing),temperature * self.meltRateParameter, 0)
        actualMelt = min(self.snow, potentialMelt)
    
        self.snow = self.snow - actualMelt
    
        # sublimate first from atmospheric loss
        self.sublimation = min(self.snow,self.atmosphericLoss)
        self.snow = self.snow - self.sublimation
           
        # potential evapotranspiration from subsurface water (m/day)
        self.potential_evapotranspiration = max(self.atmosphericLoss - self.sublimation,0.0)
    
        # actual evapotranspiration from subsurface water (m/day)
        self.evapotranspiration = min(self.subsurfaceWater, self.potential_evapotranspiration)
                
        # subtract actual evapotranspiration from subsurface water
        self.subsurfaceWater = max(self.subsurfaceWater - self.evapotranspiration, 0)
    
        # available water on surface (m/day) and infiltration
        availableWater = actualMelt + rainFall
        infiltration = min(self.infiltrationCapacity,availableWater)
        self.runoffGenerated = availableWater - infiltration
    
        # streamflow in m water depth per day
        discharge = accuflux(self.ldd,self.runoffGenerated + self.upwardSeepage)
        
        # upward seepage (m/day) from subsurface water
        self.upwardSeepage = self.seepageProportion * self.subsurfaceWater 
    
        # update subsurface water
        self.subsurfaceWater = max(self.subsurfaceWater + infiltration - self.upwardSeepage, 0)
    
        # convert streamflow from m/day to m3 per second
        dischargeMetrePerSecond = (discharge * cellarea()) / (24 * 60 * 60)
        # sample the discharge to be stored as timeseries file
        self.runoffTss.sample(dischargeMetrePerSecond)
    
        # read streamflow at the observation location 
        runoffAtOutflowPoint=getCellValueAtBooleanLocation(self.sampleLocation,dischargeMetrePerSecond)
        # insert it in place in the output numpy array
        self.simulation[self.currentTimeStep() - 1] = runoffAtOutflowPoint
