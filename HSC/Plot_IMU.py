import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv


#%% Plotting parmeters 
plt.rcParams["font.family"] = "Times New Roman"
font = {
        #'weight' : 'bold',
        'size'   : 16}
plt.rc('font', **font)
DPI= 200

#%%
fs= 1/0.004
#%% Functions  
def read_IMU(file_name):
    data = read_csv(file_name)
    acc_x = np.array(data['acc[0]'].tolist())
    acc_z = np.array(data['acc[1]'].tolist())
    acc_y = np.array(data['acc[2]'].tolist())
    
    Gyr_x = np.array(data['pqr[0]'].tolist())
    Gyr_z = np.array(data['pqr[1]'].tolist())
    Gyr_y = np.array(data['pqr[2]'].tolist())
        
    Time_IMU =  np.linspace(0,len(acc_z)/fs,len(acc_z))
    
    Data = np.transpose(np.array([Time_IMU,acc_x,acc_y,acc_z , Gyr_x,Gyr_y,Gyr_z]))
    # print(Data)
    # return Time_IMU,acc_x,acc_y,acc_z , Gyr_x,Gyr_y,Gyr_z
    return Data

#%%
 
Results_Folder = 'IS_logs/'
#%%
import os

def find_last_file_by_name(Path):
    Path  =  'IS_logs'
    # Get the last directory
    directories = [d for d in os.listdir(Path) if os.path.isdir(os.path.join(Path, d))]
    directories = sorted(directories)

    all_files = os.listdir(Path + '/' + directories[-1])
    
    # Filter files with the specified ending
    target_files = [file for file in all_files if file.endswith('_IMU.csv')]
    target_file_path = os.path.join(target_files[0])
    File =  directories[-1] + '/'  + target_file_path
#    print(File)

    return File

File_Name = find_last_file_by_name(Results_Folder)

IMU_DATA= read_IMU(Results_Folder+File_Name)

#%%
Title = ['acc x' , 'acc y' ,'acc z' , 'Gyr x' , 'Gyr y' ,'Gyr z'  ]
#%% Plotting 
plt.figure(figsize=(16,5))
for i in range(0,6):
    plt.subplot(2,3,i+1)
    plt.plot(IMU_DATA[:,0],IMU_DATA[:,i+1],'k')
    plt.title(Title[i])
    plt.xlabel('Time [sec]')

plt.tight_layout()
