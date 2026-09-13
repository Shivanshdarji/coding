# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import silhouette_score

# data= pd.read_csv("C:/Users/SHIVANSH/Downloads/environmental factors.csv")
# data.head()

# print(data.head())

# scaler = StandardScaler()
# data_scaled=scaler.fit_transform(data)

# print("\n")

# #display scaled data
# print(pd.DataFrame(data_scaled, columns=data.columns).head())
# inertia=[]
# k_range=range(1,11)
# for k in k_range:
#     kmeans=KMeans(n_clusters=k,random_state=42)
#     kmeans.fit(data_scaled)
#     inertia.append(kmeans.inertia_)

# plt.plot(k_range,inertia,marker='o')
# plt.title("elbow method")
# plt.xlabel("numbers of cluster")
# plt.ylabel("inertia")
# plt.show()

# sil_score=silhouette_score(data_scaled,['cluster'])
# print(f'Silhouette Score:{sil_score}')
# print(f"silhouette Score: {sil_score}")

# plt.figure(figsize=(8,6))
# sns.scatterplot(x='tempreture',y="humidity", hue="cluster",
#                 data=data, palette='viridis', s=100, alpha=0.7, edgecolor='k')

# plt.title('K-means clustering of environmental factors')
# plt.xlabel('tempreture')
# plt.ylabel("humidity")
# plt.legend(title='cluster', bbox_to_anchor=(1.05,1), loc='upper left')
# plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

data= pd.read_csv("C:/Users/SHIVANSH/Downloads/farmer_advisor_dataset.csv")
data.head()

print(data.head())

scaler = StandardScaler()
data_scaled=scaler.fit_transform(data)


print("\n")

#display scaled data
print(pd.DataFrame(data_scaled, columns=data.columns).head())
inertia=[]
k_range=range(1,11)
for k in k_range:
    kmeans=KMeans(n_clusters=k,random_state=42)
    kmeans.fit(data_scaled)
    inertia.append(kmeans.inertia_)

plt.plot(k_range,inertia,marker='o')
plt.title("elbow method")
plt.xlabel("numbers of cluster")
plt.ylabel("inertia")
plt.show()

k=7
kmeans=KMeans(n_clusters=k, random_state=42)
data['cluster']=kmeans.fit_predict(data_scaled)

#priting first few rows with cluster labels
print(data.head())

sil_score= silhouette_score(data_scaled, data['cluster'])
print(f"silhouette Score: {sil_score}")

plt.figure(figsize=(8,6))
sns.scatterplot(x='carbon_emissions',y="pollution_level", hue="cluster",
                data=data, palette='viridis', s=100, alpha=0.7, edgecolor='k')

plt.title('K-means clustering of environmental factors')
plt.xlabel('carbon emission')
plt.ylabel("pollution level")
plt.legend(title='cluster', bbox_to_anchor=(1.05,1), loc='upper left')
plt.show()