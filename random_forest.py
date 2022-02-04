import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import matplotlib.pyplot as plt

'''
Trains a random forest to predict streamflow and plots results

Inputs
------
simulation model: MyFirstModel object
    dynamic model
streamflow : txt
    the observed streamflow

Parameters
----------
max_depth: int 
    maximum depth of tree
n_estimators: int
    numbers of trees in forest
nrOfTimeSteps: int
    number of timesteps for model to run
    
Output
------
plot of observed & predicted streamflow
'''

# read the data from txt files
sf = pd.read_csv('streamflow.txt', header = None, delimiter = " ", names=["Day", "Streamflow"]).drop(columns=['Day'])
pt = pd.read_csv('precipitation.txt', header = None, delimiter = " ", names=["Day", "Precipitation"]).drop(columns=['Day'])
tm = pd.read_csv('temperature.txt', header = None, delimiter = " ", names=["Day", "Temperature"]).drop(columns=['Day'])
data = pd.concat([sf,pt,tm], axis = 1)

#split the dataset
train_X = data.iloc[365:1094,1:3]
train_y = data.iloc[365:1094,0]
test_X = data.iloc[1095:1460,1:3].reset_index(drop = True)
test_y = data.iloc[1095:1460,0].reset_index(drop = True)

#train a randomforest
model = RandomForestRegressor(max_depth = 6,n_estimators= 800, random_state=42)
model.fit(train_X, train_y)

predictions = model.predict(test_X)
errors = (predictions - test_y)**2
print('Mean Absolute Error:', np.mean(errors), 'degrees.')

# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors / test_y)
# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')

# plot results
plt.plot(predictions[0:365], color = "b")
plt.plot(test_y[0:365], color = 'r')
plt.show()