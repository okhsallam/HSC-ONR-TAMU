import sys
import pyzed.sl as sl
from sys import exit
import time 
import numpy as np
from datetime import datetime
pi = np.pi
import Jetson.GPIO as GPIO
#%%
GPIO.setmode(GPIO.BOARD)

Toggle_switch = 15
GPIO.setup(Toggle_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#%%
init_params = sl.InitParameters(camera_resolution=sl.RESOLUTION.HD720,
                             coordinate_units=sl.UNIT.METER,
                             coordinate_system=sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP)
                             
zed = sl.Camera()
status = zed.open(init_params)
if status != sl.ERROR_CODE.SUCCESS:
    print(repr(status))
    exit()
tracking_params = sl.PositionalTrackingParameters()
zed.enable_positional_tracking(tracking_params)
runtime = sl.RuntimeParameters()
camera_pose = sl.Pose()
camera_info = zed.get_camera_information()
py_translation = sl.Translation()
pose_data = sl.Transform()
#%%
now=datetime.now()
current_time = now.strftime("%H_%M_%S")

#%% Create a results file  
import os
Results_Folder = 'Results_ZED'
os.makedirs(Results_Folder, exist_ok=True)
file_name= Results_Folder + '/'+current_time +".txt"
File_6_DOF = open(file_name, 'a')
print("File generated to save data stream ...")
#%%

Time_0 =  time.time()
try:
    print('ZED Camera Started')
    while True:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            tracking_state = zed.get_position(camera_pose, sl.REFERENCE_FRAME.WORLD)
            if tracking_state == sl.POSITIONAL_TRACKING_STATE.OK:
                rotation = camera_pose.get_rotation_vector()*180/pi
                translation = camera_pose.get_translation(py_translation)    
                # pose_data = camera_pose.pose_data(sl.Transform())
                DOF_6 =  np.concatenate((translation.get(),rotation))       
                DOF_6_text = str([time.time()-Time_0,   round(DOF_6[0],4),  round(DOF_6[1],4)  ,round(DOF_6[2],4),round(DOF_6[3],4),  round(DOF_6[4],4)  ,round(DOF_6[5],4)] )
                # print(DOF_6_text)
                File_6_DOF.write(DOF_6_text+"\n")
                # print(DOF_6_text)
                
                
                
                
                
        if GPIO.input(Toggle_switch) == GPIO.LOW:
            
            zed.close()
            print('ZED Camera is Terminated')
            break
       
 
except KeyboardInterrupt:
     zed.close()
     sys.exit(1)  
    
