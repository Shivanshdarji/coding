import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
import seaborn as sns
import matplotlib.pyplot as plt

#Load the dataset
data = pd.read_csv('C:/Users/SHIVANSH/Downloads/green_tech_data.csv')
data.head()
print(data.head())
print(data.isnull().sum())

# #failure selection 
# x= data[['carbon_emissions','energy_output','renewability_index','cost_efficiency']]
# y= data['sustainablity']
x=data[['carbon_emissions','energy_output','renewability_index','cost_efficiency']]
y=data['sustainability']

x_train, x_test, y_train, y_test= train_test_split(x,y,test_size=0.2,random_state=42)

model= LogisticRegression()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
y_pred

#accuracy_score
accuracy=accuracy_score(y_test,y_pred)
print("accuracy:",accuracy)

#confusion matrix
conf_matrix = confusion_matrix(y_test,y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['Not sustainable','Sustainable'],yticklabels=['Not sustainable','Sustainable'])

plt.xlabel('Pridicted')
plt.ylabel('Actual')
plt.title('Confusion matrix')
plt.show()

print(classification_report(y_test, y_pred, target_names=['Not_Sustainable','Sustainable']))

