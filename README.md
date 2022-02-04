# StreamflowPrediction
This code was developed for the course of Spatial Data Analysis and Simulation Models at Utrecht University. 

Frist in order to simulate efficiently the streamflow we calibrated a simulation model using the Brute Force technique. The experiments for the calibration process included the following parameters:
- **Snow melt rate**
- **Temperature lapse rate**
- **Infiltration capacity**
- **Seepage proportion**
- **Atmoshperic loss**

Then, a Random Forest (RF) was developed in order to predict streamflow, having presipitation and temperature as inputs. The predictions of the two models were compared and the analysis was extended to a new dataset to observe their variance.

# How to Run
build_model.py: builds a dynamic model for simulating the streamflow

brute_force.py: imports the model from build_model.py and performs calibration for a set of values for the parameters mentioned above. Finally, returns the mse for each calibrated model.

simulation_results.py: based on the values obtained by the calibration, runs the calibrated model and plots the observed and the simulated streamflow.

random_forest.py: trains a random forest model (max_depth = 6, n_estimators = 800), predicts the streamflow and compares the observed and the predicted streamflow.

# Data
Observed streamflow data
--------------------------

streamflow.txt
Streamflow from Dorferbach. Downloaded from the Global Runoff Data
Centre, https://www.bafg.de/GRDC/
It represents the time span from 1 jan 1990 up to 31 dec 1993

Meteorological data
---------------------

temperature.txt and precipitation.txt
Meteorological data for the catchment areas, reanalysis data from
the NCEP, downloaded from https://globalweather.tamu.edu
It represents the time span from 1 jan 1990 up to 31 dec 1993

Map data
-----------

dem.map
Resampled from the data source:
DGM_Tirol_10m_epsg31254
Downloaded from https://www.data.gv.at/katalog/dataset/land-tirol_tirolgelnde
It is the gelande model.

ldd.map
derived from dem

sample_location.map
location of measurement for streamflow (see above)
