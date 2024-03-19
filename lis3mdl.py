from i2c_interface import I2CInterface

class LIS3MDL:
    """
    The base address is 0x1E, if the SA0 is connected to the VDD_IO, the
    address becomes 0x1F.
    """
    def __init__(self, i2c_bus=1, i2c_address=0x1E): 
        self.WHO_AM_I = 0x0F
        self.CTRL_REG1 = 0x20
        self.CTRL_REG2 = 0x21
        self.CTRL_REG3 = 0x22
        self.CTRL_REG4 = 0x23
        self.OUT_X_L = 0x28
        self.OUT_X_H = 0x29
        self.OUT_Y_L = 0x2A
        self.OUT_Y_H = 0x2B
        self.OUT_Z_L = 0x2C
        self.OUT_Z_H = 0x2D

        self.i2c = I2CInterface(i2c_bus, i2c_address)
        self.initialize_sensor()
    
    def initialize_sensor(self):
        self.i2c.write_byte_data(self.CTRL_REG1, 0x70)  # 80 Hz, high performance
        self.i2c.write_byte_data(self.CTRL_REG2, 0x00)  # ±4 gauss
        self.i2c.write_byte_data(self.CTRL_REG3, 0x00)  # Continuous-conversion mode
        self.i2c.write_byte_data(self.CTRL_REG4, 0x0C)  # Z-axis ultra high performance

    def read_magnetic_field(self):
        x = self.read_axis(self.OUT_X_L, self.OUT_X_H)
        y = self.read_axis(self.OUT_Y_L, self.OUT_Y_H)
        z = self.read_axis(self.OUT_Z_L, self.OUT_Z_H)
        return x, y, z

    def read_axis(self, low_addr, high_addr):
        low_byte = self.i2c.read_byte_data(low_addr)
        high_byte = self.i2c.read_byte_data(high_addr)
        value = (high_byte << 8) | low_byte
        if value > 32767:
            value -= 65536
        return value