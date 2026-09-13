import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

#load datset
df=pd.read_csv("C:/Users/SHIVANSH/Downloads/appliance_energy.csv")

#display some rows
print(df.head())

#check for missing values
print(df.isnull().sum())
df=df.dropna()

#features (independent variables) and target (dependent variables)
#independent variable (Temperature)
x= df[['Temperature (°C)']]
#Dependent variable (Energy Consumption)
y= df['Energy Consumption (kWh)']

#Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

#Create a Linear Regresion model
model = LinearRegression()

#Traain the model
model.fit(x_train, y_train)

#Make predictions on the test set
y_pred = model.predict(x_test)

# Assuming df is your DataFrame and necessary libraries are imported

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Features (Independent variable)
x = df['Temperature (°C)'].values.reshape(-1, 1)  # Reshaping x to 2D array

# Target (Dependent variable)
y = df['Energy Consumption (kWh)']

# Split data into training and testing set (80% train, 20% test)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Create a linear regression model
model = LinearRegression()

# Train the model using both x_train and y_train
model.fit(x_train, y_train)

# Make predictions on the test set
y_pred = model.predict(x_test)

# Optional: Evaluate the model performance (e.g., R-squared)
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_pred)
print(f"R-squared: {r2}")

#chart
plt.scatter(x_test,y_test,color='blue',label='Test_data')
plt.plot(x_test,y_pred,color='red',label='Regression_line')
plt.xlabel('Temperature (°C)')
plt.ylabel('Energy Consumption (kWh)')
plt.legend()
plt.title('Energy Consumption Prediction using Simle linear Regression')
plt.show()

import joblib
#save a model to a file
joblib.dump(model,'appliance_energy_model.pk1')

