import smbus2

class I2CInterface:
    def __init__(self, i2c_bus=1, i2c_address=0x6B):
        self.bus = smbus2.SMBus(i2c_bus)
        self.i2c_address = i2c_address

    def read_byte_data(self, register):
        return self.bus.read_byte_data(self.i2c_address, register)

    def write_byte_data(self, register, value):
        self.bus.write_byte_data(self.i2c_address, register, value)

    def read_i2c_block_data(self, register, length):
        return self.bus.read_i2c_block_data(self.i2c_address, register, length)