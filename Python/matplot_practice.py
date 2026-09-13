import matplotlib.pyplot as plt
months =['Jan','feb','mar','apr','may','jun']
energy_consumption =[1200,1300,1100,1500,1400,1600]
#create line plot
plt.plot(months,energy_consumption,marker='o',color='b',linestyle='--')#scatter for dot graph
#add titles and lables
plt.title("Energy Consumption over 6 months")
plt.xlabel("month")
plt.ylabel("Energy Consumption(Mwh)")
plt.show()


