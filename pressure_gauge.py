"""
pressure_gauge.py

This module provides functionality to interact with the ESI-USB-API library for the
GD4200 USB pressure gauge.
It allows reading pressure and temperature values from the pressure gauge and storing
the data in the database.

Key Functions:
- check_pressure_gauge(repository): Main function to read and process data from the pressure gauge.

Dependencies:
- ctypes (to interface with the ESI-USB-API library)
- time
- platform
- numpy (for random data generation, used for testing/mock purposes)
- logging
- db_model (for interacting with the database models)

Usage:
This module is typically imported, and the `check_pressure_gauge` function is called when the
application needs to read and process data from the pressure gauge. The function takes the
Repository object as an argument for database interaction and returns the pressure and
temperature values read from the gauge.
"""
import ctypes # Import the ctypes module to interface with the ESI-USB-API library
import platform # Import the platform module to identify whether it is 32bit or 64 bit system
import logging
from db_model import PressureGaugeData

# Detect the system architecture
def check_pressure_gauge(repository):
    '''
    This method is used to check the pressure and temperature in pressure gauge device.
    '''
    logging.info("Entered into check pressure gauge")
    is_64bit = platform.architecture()[0] == '64bit'
    # Load the appropriate DLL file based on the system architecture
    if is_64bit:
        esi_api = ctypes.CDLL("./esi_dll/ESI-USB-API.dll")
        # This library provides functions to interact with GD4200 USB pressure gauge
    else:
        esi_api = ctypes.CDLL("./esi_dll/ESI_USB_API_COM.dll")
        # This library provides functions to interact with GD4200 USB pressure gauge
    # Define constants
    # These constants are used as return values from the API functions
    OK = 0
    FAIL = -1
    INVALID_INDEX = -2
    INVALID_PARAMETER = -3
    INVALID_STATE = -4
    # Define enums
    # These enums represent the available pressure and temperature units
    class PressureUnits(ctypes.c_int):
        '''
        This class is using for define the measurment units
        '''
        bar = 0
        mbar = 1
        psi = 2
        MPa = 3
        Pa = 4
        mmH2O = 5
        mmHg = 6
        atm = 7
        kgcm2 = 8
        kPa = 9

    class TemperatureUnits(ctypes.c_int):
        '''
        This is used to have the units for temperature.
        '''
        C = 0
        K = 1
        F = 2
    # Define function prototypes
    # These declarations specify the argument types and return types of the API functions
    esi_api.FindSensors.argtypes = [ctypes.POINTER(ctypes.c_int)]
    esi_api.FindSensors.restype = ctypes.c_int
    esi_api.GetSensorInfo.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int),
                                      ctypes.c_char_p, ctypes.c_int]
    esi_api.GetSensorInfo.restype = ctypes.c_int
    esi_api.UseSensor.argtypes = [ctypes.c_int]
    esi_api.UseSensor.restype = ctypes.c_int
    esi_api.Read.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int,
                             ctypes.c_float, ctypes.POINTER(ctypes.c_float)]
    esi_api.Read.restype = ctypes.c_int
    esi_api.ReadTemperature.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float)]
    esi_api.ReadTemperature.restype = ctypes.c_int
    esi_api.ReleaseSensor.argtypes = [ctypes.c_int]
    esi_api.ReleaseSensor.restype = ctypes.c_int
    esi_api.CleanUp.argtypes = []
    esi_api.CleanUp.restype = ctypes.c_int
    # Function to find connected sensors
    def find_sensors():
        sensor_count = ctypes.c_int()
        result = esi_api.FindSensors(ctypes.byref(sensor_count))
        if result != OK:
            raise Exception("Failed to find sensors")
        return sensor_count.value

    # Function to get sensor information
    def get_sensor_info(sensor_index):
        port_number = ctypes.c_int()
        serial_number = ctypes.create_string_buffer(100)
        result = esi_api.GetSensorInfo(sensor_index, ctypes.byref(port_number), serial_number, 100)
        if result != OK:
            raise Exception("Failed to get sensor info")
        return port_number.value, serial_number.value.decode()

    # Function to use a sensor
    def use_sensor(sensor_index):
        result = esi_api.UseSensor(sensor_index)
        if result != OK:
            print("Failed to use sensor")

    # Function to read pressure
    def read_pressure(sensor_index, units, absolute, temperature):
        pressure = ctypes.c_float()
        result = esi_api.Read(sensor_index, units, absolute, temperature, ctypes.byref(pressure))
        if result != OK:
            print("Failed to read pressure")
        return pressure.value

    # Function to read temperature
    def read_temperature(sensor_index, units):
        temperature = ctypes.c_float()
        result = esi_api.ReadTemperature(sensor_index, units, ctypes.byref(temperature))
        if result != OK:
            print("Failed to read temperature")
        return temperature.value

    # Function to release a sensor
    def release_sensor(sensor_index):
        result = esi_api.ReleaseSensor(sensor_index)
        if result != OK:
            print("Failed to release sensor")

    # Function to clean up resources
    def clean_up():
        result = esi_api.CleanUp()
        if result != OK:
            print("Failed to clean up")

    print("Usage area")
    try:
        # Find connected sensors
        sensor_count = find_sensors()
        print(f"Found {sensor_count} sensor(s)")
        # Get sensor information
        for i in range(sensor_count):
            port, serial = get_sensor_info(i)
            print(f"Sensor {i}: Port={port}, Serial={serial}")
        # Use the first sensor
        sensor_index = 0
        use_sensor(sensor_index)

        # Read pressure in bar and temperature in Celsius
        pressure = read_pressure(sensor_index, PressureUnits.bar, 0, 20.0)
        temperature = read_temperature(sensor_index, TemperatureUnits.C)

        print(f"Pressure: {pressure:.2f} bar, Temperature: {temperature:.2f} °C")

        pressure_gauge_data = PressureGaugeData(pressure=pressure, temperature=temperature)
        repository.create_pressure_gauge_data(pressure_gauge_data)

        print(f"Pressure: {pressure:.2f} bar, Temperature: {temperature:.2f} °C")
        logging.info("Pressure: %.2f bar, Temperature: %.2f °C", pressure, temperature)

        return [pressure, temperature]

    except Exception as e:
        print(f"Error: {str(e)}")
        logging.error("Error occurred in check_pressure_gauge: %s", str(e))
        return None, None  # Return None for both pressure and temperature
    finally:
        # Release the sensor and clean up
        release_sensor(sensor_index)
        clean_up()
