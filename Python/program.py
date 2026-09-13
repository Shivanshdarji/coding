# Sample climate dataset
climate_data=[{"city": "city A", "temperature": 25, "carbon_footprint": 500},
{"city": "city B", "temperature": 10,  "carbon_footprint": 200},
{"city": "city C", "temperature": 50,  "carbon_footprint": 300},
{"city": "city D", "temperature": 30,  "carbon_footprint":400}]

#high temperature threshold (cities above this temperature will be selected)
high_temp_threshold=26

#uses a list comprehension to filter cities with temperatures after than the threshold .
high_temp_cities= [city for city in climate_data if city["temperature"]> high_temp_threshold]

#print the result
print("cities with high temperatures (>26):")
for city in high_temp_cities:
    print(f"{city['city']} - {city['temperature']}") 

total_carbon=0 # carbon_footprint variable
for city in climate_data:
    total_carbon += city[ "carbon_footprint"]

average_carbon_footprint = total_carbon / len(climate_data) # calculating average
print(f"\nAverage Carbon Footprint: {average_carbon_footprint:.2f} kg CO2")

#set a sustainable threshold
sustainability_threshold =400

sustainable_cities = list(filter(lambda city: city["carbon_footprint"]< sustainability_threshold, climate_data))

print("\nSustainable cities (carbon footprint < 400):")
for city in sustainable_cities:
    print(f"{city['city']}- {city['carbon_footprint']}")

def calculate_carbon_footprint(energy_comsumption, emission_factor):
    return energy_comsumption * emission_factor

energy_consumption = 1000
emission_factor = 0.475

carbon_footprint = calculate_carbon_footprint(energy_consumption, emission_factor)
print(f"carbon foorprint: {carbon_footprint}")