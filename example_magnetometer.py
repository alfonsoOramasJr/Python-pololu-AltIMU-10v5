from lis3mdl import *

if __name__ == "__main__":
    magnetometer = LIS3MDL()
    try:
        while True:
            x, y, z = magnetometer.read_magnetic_field()
            print(f"Magnetic field [X, Y, Z]: [{x}, {y}, {z}]")
    except KeyboardInterrupt:
        print("Program terminated by the user.")