#!/bin/bash
## Command to know the connected USBs to the device 


## Command to run the IMU

./cltool -c /dev/ttyACM0 -did DID_INS_1 DID_GPS1_POS DID_PIMU  presetPPD DID_IMU  -lon -lt=csv



# Trap termination signal and perform cleanup
trap "cleanup_function" EXIT

cleanup_function() {
    echo "Cleanup function executed"
    # Additional cleanup logic if needed
}
