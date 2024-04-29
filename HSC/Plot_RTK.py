import matplotlib.pyplot as plt
import numpy as np 
#%%
num_file = 2

#%%
# Open the text file
with open("RTK_GNSS/RTK_GNSS_" + str(num_file)+ ".txt", "r") as file:
    # Read the lines
    lines = file.readlines()

Lat = []
Lon =[]
Speed = []
fs =4
# Iterate through the lines
for line in lines:
    # Check if the line starts with "$GNMRC"
    if line.startswith("$GNRMC"):
        # Split the line by comma
        values = line.strip().split(",")
        # print(values)
        Lat.append(eval(values[3])) 
        Lon.append(eval(values[5])) 
        Speed.append(eval(values[7])) 

Time =  np.linspace(0,len(Speed)/fs,len(Speed))
#%%
plt.figure(figsize=(16,3))
plt.subplot(1,3,1)
plt.plot(Time,Lat,'k')
plt.title('Lat')
plt.subplot(1,3,2)
plt.plot(Time,Lon,'k')
plt.title('Long')
plt.subplot(1,3,3)
plt.plot(Time,Speed,'k')
plt.title('U Mag [m/sec]')

plt.tight_layout()