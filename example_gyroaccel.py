from lsm6ds33 import *

if __name__ == "__main__":
    lsm6ds33 = LSM6DS33()
    lsm6ds33.initialize()
    
    while True:
        gx, gy, gz = lsm6ds33.read_gyroscope()
        print(f"Gyroscope: X={gx}, Y={gy}, Z={gz}")
        
        ax, ay, az = lsm6ds33.read_accelerometer()
        print(f"Accelerometer: X={ax}, Y={ay}, Z={az}")