from lps25h import *

if __name__ == "__main__":
    lps25h = LPS25H()

    if lps25h.check_sensor():
        lps25h.set_power_mode(True)

        lps25h.enable_hardware_filter()
        
        lps25h.calibrate_altitude(100) ## The amount of cycles the program will use to calibrate the altitude(pressure).
        
        print("Continuously monitoring altitude with calibrated sea level pressure...")
        while True:
            pressure = lps25h.read_pressure()
            altitude = lps25h.calculate_altitude(pressure)
            print(f"Relative Altitude: {altitude:.2f} meters")
            time.sleep(0.1)

    else:
        print("Sensor not detected. Check wiring and I2C address.")