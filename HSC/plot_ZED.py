import numpy as np
import matplotlib.pyplot as plt


#%% Plotting parmeters 
plt.rcParams["font.family"] = "Times New Roman"
font = {
        #'weight' : 'bold',
        'size'   : 16}
plt.rc('font', **font)
DPI= 300

#%%
fs = 1/0.023
#%% Functions  
# file_ZED ='Heave__Lake_2_new7' 

def read_dof(file_name):
    DOF_6=np.zeros((1,7))

    with open(file_name) as f:
        for line in f:
            line_split = line.strip().replace("["," ").replace("]"," ").split(",")
            DOF_6_frame = np.array(line_split,dtype=float).reshape((1, 7))
            DOF_6=np.append(DOF_6,DOF_6_frame,axis=0)
    
    # X_T = DOF_6[:,1]
    # Y_T = DOF_6[:,2]
    # Z_T = DOF_6[:,3]
    
    # X_R = DOF_6[:,4]
    # Y_R = DOF_6[:,5]
    # Z_R = DOF_6[:,6]
    
    
    DOF_6 = np.delete(DOF_6,0,axis=0)
    # Time=DOF_6[:,0]
    return DOF_6

#%%  
Results_Folder = 'Results_ZED/'
#%%
import os

def find_last_file_by_name(directory):
    # Get a list of all files in the directory
    all_files = os.listdir(directory)

    # Filter out directories and get only files
    files = [file for file in all_files if os.path.isfile(os.path.join(directory, file))]

    # Sort the files by name and get the last one
    last_file = max(files)

    return last_file



File_Name = find_last_file_by_name(Results_Folder)
DOF_6 = read_dof(Results_Folder+File_Name)


#%%

Title = ['Forward', 'Heave','Sway','Roll', 'Yaw','Pitch']   #  X_T , Y_T , Z_T , X_R , Y_R , Z_R

#%% Plotting 
plt.figure(figsize=(16,6))

for i in range(0,6):
    plt.subplot(2,3,i+1)
    plt.plot(DOF_6[:,0], DOF_6[:,i+1],'k')
    plt.title(Title[i])
    plt.xlabel('Time [sec]')
    plt.ylabel('[m]')
    

plt.tight_layout()







