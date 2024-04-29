import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
import os

#%% Plotting parmeters 
plt.rcParams["font.family"] = "Times New Roman"
font = {
        #'weight' : 'bold',
        'size'   : 16}
plt.rc('font', **font)
DPI= 200

#%%  Number of the file to plot, start with 1
num_file = 2
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
    return Data

def read_GPS(file_name):
    data = read_csv(file_name)
    Lat = np.array(data['lla[0]'].tolist())
    Long = np.array(data['lla[1]'].tolist())
    Alt = np.array(data['lla[2]'].tolist())
    
    u = np.array(data['uvw[0]'].tolist())
    v = np.array(data['uvw[1]'].tolist())
    w = np.array(data['uvw[2]'].tolist())
    
        
    Time_IMU =  np.linspace(0,len(Lat)/fs,len(Lat))
    
    Data = np.transpose(np.array([Time_IMU,Lat,Long,Alt , u,v,w]))
    return Data
#%%
 
Results_Folder = 'IS_logs/'
#%%




def find_last_file_by_name(Path,data_file_end):
    
    Path  =  'IS_logs'
    # Get the last directory
    directories = [d for d in os.listdir(Path) if os.path.isdir(os.path.join(Path, d))]
    directories = sorted(directories)

    all_files = os.listdir(Path + '/' + directories[num_file-1])
    
    # Filter files with the specified ending
    target_files = [file for file in all_files if file.endswith(data_file_end)]
    target_file_path = os.path.join(target_files[0])
    File =  directories[num_file-1] + '/'  + target_file_path
#    print(File)

    return File


#%%
File_Name_IMU = find_last_file_by_name(Results_Folder,'_IMU.csv')
IMU_DATA= read_IMU(Results_Folder+File_Name_IMU)


File_Name_GPS = find_last_file_by_name(Results_Folder,'_INS_1.csv')
GPS_DATA= read_GPS(Results_Folder+File_Name_GPS)

#%%
Title_IMU = ['acc x' , 'acc y' ,'acc z' , 'Gyr x' , 'Gyr y' ,'Gyr z'  ]
Title_GPS = ['Lat' , 'Long' ,'Alt' , 'u' , 'v' ,'w'  ]

#%% Plotting 
plt.figure(figsize=(16,7))
for i in range(0,6):
    plt.subplot(2,3,i+1)
    plt.plot(IMU_DATA[:,0],IMU_DATA[:,i+1],'k')
    plt.title(Title_IMU[i])
    plt.xlabel('Time [sec]')

plt.tight_layout()


plt.figure(figsize=(16,7))
for i in range(0,6):
    plt.subplot(2,3,i+1)
    plt.plot(GPS_DATA[:,0],GPS_DATA[:,i+1],'k')
    plt.title(Title_GPS[i])
    plt.xlabel('Time [sec]')

plt.tight_layout()

#%%
U_Mag = (GPS_DATA[:,4]**2 + GPS_DATA[:,5]**2)**0.5
plt.figure()
plt.plot(GPS_DATA[:,0],U_Mag,'k')
plt.title('U Mag [m/sec]')
plt.xlabel('Time [sec]')
