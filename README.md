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
