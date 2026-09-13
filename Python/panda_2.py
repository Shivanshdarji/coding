import pandas as pd

renewable_sources = ["solar","wind","hydropower","geothermal","biomass"]

data ={
    "Project" : ["Solar Farm A","Wind Turbin A","Hydropower Y","Solar Roof 2","geothermal plant P"],
    "Technology":["solar","wind","hydropower","solar","geothermal"],
    "capacity(mw)":[150,300,200,50,100],
    "cost(million $)":[200,400,350,100,250],
    "location": ["california","taxas","washington","nevada","idaho"],
    "comletion year":[2023,2024,2022,2025,2023]
}
#part1
import pandas as pd

renewable_sources = ["solar","wind","hydropower","geothermal","biomass"]

data ={
    "Project" : ["Solar Farm A","Wind Turbin A","Hydropower Y","Solar Roof 2","geothermal plant P"],
    "Technology":["solar","wind","hydropower","solar","geothermal"],
    "capacity(mw)":[150,300,200,50,100],
    "cost(million $)":[200,400,350,100,250],
    "location": ["california","taxas","washington","nevada","idaho"],
    "comletion year":[2023,2024,2022,2025,2023]
}

renewable_series = pd.Series(renewable_sources)
project_df = pd.DataFrame(data)
print("renewable sources")
print(renewable_series)

#part 2
import pandas as pd

renewable_sources = ["solar","wind","hydropower","geothermal","biomass"]

data ={
    "Project" : ["Solar Farm A","Wind Turbin A","Hydropower Y","Solar Roof 2","geothermal plant P"],
    "Technology":["solar","wind","hydropower","solar","geothermal"],
    "capacity(mw)":[150,300,200,50,100],
    "cost(million $)":[200,400,350,100,250],
    "location": ["california","taxas","washington","nevada","idaho"],
    "comletion year":[2023,2024,2022,2025,2023]
}

project_df = pd.DataFrame(data)

print("\n Green Technology Projecta DataFrame:")
print(project_df)

#part3
import pandas as pd

renewable_sources = ["solar","wind","hydropower","geothermal","biomass"]

data ={
    "Project" : ["Solar Farm A","Wind Turbin A","Hydropower Y","Solar Roof 2","geothermal plant P"],
    "Technology":["solar","wind","hydropower","solar","geothermal"],
    "capacity(mw)":[150,300,200,50,100],
    "cost(million $)":[200,400,350,100,250],
    "location": ["california","taxas","washington","nevada","idaho"],
    "comletion year":[2023,2024,2022,2025,2023]
}
project_df = pd.DataFrame(data)
print("\n list of project: ")
print(project_df["Project"])

#part5
import pandas as pd

renewable_sources = ["solar","wind","hydropower","geothermal","biomass"]

data ={
    "Project" : ["Solar Farm A","Wind Turbin A","Hydropower Y","Solar Roof 2","geothermal plant P"],
    "Technology":["solar","wind","hydropower","solar","geothermal"],
    "capacity(mw)":[150,300,200,50,100],
    "cost(million $)":[200,400,350,100,250],
    "location": ["california","taxas","washington","nevada","idaho"],
    "comletion year":[2023,2024,2022,2025,2023]
}
project_df = pd.DataFrame(data)
high_capacity_projects = project_df[project_df["capacity(mw)"] > 100]
print(high_capacity_projects)

#part6
import pandas as pd

renewable_sources = ["solar","wind","hydropower","geothermal","biomass"]

data ={
    "Project" : ["Solar Farm A","Wind Turbin A","Hydropower Y","Solar Roof 2","geothermal plant P"],
    "Technology":["solar","wind","hydropower","solar","geothermal"],
    "capacity(mw)":[150,300,200,50,100],
    "cost(million $)":[200,400,350,100,250],
    "location": ["california","taxas","washington","nevada","idaho"],
    "comletion year":[2023,2024,2022,2025,2023]
}
project_df = pd.DataFrame(data)
project_df["cost per mw"]= project_df["cost(million $)"]/ project_df["capacity(mw)"]

print("\n DataFrame with cost per mw :")
print(project_df)

#part7
import pandas as pd

renewable_sources = ["solar","wind","hydropower","geothermal","biomass"]

data ={
    "Project" : ["Solar Farm A","Wind Turbin A","Hydropower Y","Solar Roof 2","geothermal plant P"],
    "Technology":["solar","wind","hydropower","solar","geothermal"],
    "capacity(mw)":[150,300,200,50,100],
    "cost(million $)":[200,400,350,100,250],
    "location": ["california","taxas","washington","nevada","idaho"],
    "comletion year":[2023,2024,2022,2025,2023]
}
project_df = pd.DataFrame(data)
total_capacity = project_df["capacity(mw)"].sum()
total_cost = project_df["cost(million $)"].sum()

print(f"\n Total capacity of all projects: {total_capacity} mw ")
print(f"\n Total cost of all projects: ${total_cost} million ")