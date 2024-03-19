from i2c_interface import I2CInterface
import struct
import time

class LPS25H:
    def __init__(self, i2c_bus=1, i2c_address=0x5D):
        self.i2c = I2CInterface(i2c_bus, i2c_address)
        self.WHO_AM_I_REG_ADDR = 0x0F
        self.CTRL_REG1_ADDR = 0x20
        self.CTRL_REG2_ADDR = 0x21
        self.RES_CONF_ADDR = 0x10
        self.FIFO_CTRL_ADDR = 0x2E
        self.CTRL_REG2_ADDR = 0x21
        self.PRESS_OUT_XL = 0x28
        self.PRESS_OUT_L = 0x29
        self.PRESS_OUT_H = 0x2A
        self.TEMP_OUT_L = 0x2B
        self.TEMP_OUT_H = 0x2C
        self.initial_sea_level_pressure_hpa = None
        self.pressure_readings = []

    def check_sensor(self):
        return self.i2c.read_byte_data(self.WHO_AM_I_REG_ADDR) == 0xBD

    def set_power_mode(self, power_on):
        mode = 0x90 if power_on else 0x00
        self.i2c.write_byte_data(self.CTRL_REG1_ADDR, mode)

    def read_pressure(self):
        data = [self.i2c.read_byte_data(reg) for reg in [self.PRESS_OUT_XL, self.PRESS_OUT_L, self.PRESS_OUT_H]]
        pressure_raw = data[2] << 16 | data[1] << 8 | data[0]
        if pressure_raw & 0x800000:
            pressure_raw -= 0x1000000
        return pressure_raw / 4096.0

    def read_temperature(self):
        l, h = self.i2c.read_byte_data(self.TEMP_OUT_L), self.i2c.read_byte_data(self.TEMP_OUT_H)
        temp_raw = struct.unpack('<h', bytes([l, h]))[0]
        return 42.5 + temp_raw / 480.0

    def moving_average_pressure(self, new_pressure, window_size=10):
        self.pressure_readings.append(new_pressure)
        if len(self.pressure_readings) > window_size:
            self.pressure_readings.pop(0)
        return sum(self.pressure_readings) / len(self.pressure_readings)
    
    def enable_hardware_filter(self):
        """
        Enable and configure the hardware filter.
        Adjust the filter settings based on your specific needs and what the datasheet allows.
        """
        filter_config = 0x00  # Example filter configuration. Adjust based on datasheet.
        self.i2c.write_byte_data(self.CTRL_REG2_ADDR, filter_config)
        print("Hardware filter enabled with configuration:", bin(filter_config))
    
    """
    Assuming that the sensor is at resting point, it will calibrate it. Best to not move the
    sensor during this time.
    """
    def calibrate_altitude(self, cycles=100):
        print("Starting initial pressure calibration...")
        for _ in range(cycles):
            pressure = self.read_pressure()
            self.moving_average_pressure(pressure)
            time.sleep(0.1)
        self.initial_sea_level_pressure_hpa = sum(self.pressure_readings) / len(self.pressure_readings)
        print(f"Calibration complete. Calibrated sea level pressure: {self.initial_sea_level_pressure_hpa:.2f} hPa")

    def calculate_altitude(self, pressure_hpa):
        if self.initial_sea_level_pressure_hpa is None:
            return 0
        return 44330 * (1 - (pressure_hpa / self.initial_sea_level_pressure_hpa) ** (1 / 5.255))

if __name__ == "__main__":
    lps25h = LPS25H()
    if lps25h.check_sensor():
        ## Turns on the sensor.
        lps25h.set_power_mode(True)

        ## Enables some filters.
        lps25h.enable_hardware_filter()
        lps25h.calibrate_altitude(10)
        
        print("Continuously monitoring altitude with calibrated sea level pressure...")
        while True:
            pressure = lps25h.read_pressure()
            altitude = lps25h.calculate_altitude(pressure)
            print(f"Relative Altitude: {altitude:.2f} meters")
            time.sleep(0.1)
    else:
        print("Sensor not detected. Check wiring and I2C address.")
