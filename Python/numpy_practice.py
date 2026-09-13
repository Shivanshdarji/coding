import numpy as np

energy_consumption=np.array([1200,3400,2900,1800,2500])

print("Energy Consumption (in Mwh) for diffrent Renewable Sources:")
print(energy_consumption)

#part2
import numpy as np
energy_consumption=np.array([1200,3400,2900,1800,2500])
total_consumption= np.sum(energy_consumption)
print(f"\nTotal Energy Consumption: {total_consumption:.2f}Mwh")

#part3
import numpy as np
energy_consumption=np.array([1200,3400,2900,1800,2500])
std_deviation=np.std(energy_consumption)
print(f"\nTotal Energy Consumption: {std_deviation:.2f}Mwh")

#part4
import numpy as np
energy_consumption=np.array([1200,3400,2900,1800,2500])
reshaped_array=energy_consumption.reshape((5,1))
print("5*1 array:")
print(reshaped_array)