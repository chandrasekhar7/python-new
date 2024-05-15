"""
helium.py

This module provides functionality to read and process data from the Helium Analyzer.
It likely interacts with the Helium Analyzer device through serial communication or
other appropriate interfaces.

Key Functions:
- read_data_from_helium(repository, root): Function to read and process data from the
Helium Analyzer.

Dependencies:
- The specific dependencies for this module are not provided, but it may rely on libraries
  for serial communication, data processing, and potentially tkinter for GUI-related functionality.

Usage:
This module is typically imported, and the `read_data_from_helium` function is called
when the application needs to read and process data from the Helium Analyzer.
The function likely takes the Repository object and the root Tkinter window as arguments
for database interaction and potential GUI updates.
"""
from tkinter import messagebox
import re
import logging
import serial.tools.list_ports
import serial

def read_from_serial(ser, root):
    """
    Read data from the serial port.

    Args:
        ser: The serial port object.
        root: The root window.

    Returns:
        The parsed data if available, or 0 if there's an error.
    """
    try:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            return parse_data(data)
        read_from_serial(ser, root)
    except serial.SerialException as e:
        logging.info("Serial Exception Occurred: %s, while reading Helium Analyzer", str(e))
        print(f"Serial Exception Occurred: {str(e)}, while reading Helium Analyzer")
        messagebox.showerror("Error", "Helium Analyzer Port disconnected.", parent=root)
        return 0

def parse_data(data):
    """
    Parses the input data string and extracts the helium percentage value.

    Args:
        data (str): The input data string containing information about helium percentage,
        oxygen percentage, temperature, pressure, and timestamp.

    Returns:
        str: The extracted helium percentage value.

    Example:
        >>> parse_data("He 23.5% O2 21.2% Ti 25.0~C 1012.3 hPa 2024/05/14 15:30:00")
        '23.5'
    """
    # Define regular expression pattern to match required values
    pattern = (
        r"He\s+(\d+\.\d+)\s*%\s*O2\s+(\d+\.\d+)\s*%\s*Ti\s+(\d+\.\d+)\s*~C\s+(\d+\.\d+)\s*"
        r"hPa\s+(\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2})"
        )

    # Match the pattern in the data string
    match = re.search(pattern, data)
    if match:
        # Extract values from the matched groups
        he_value = match.group(1)
        #O2_value = match.group(2)
        #Ti_value = match.group(3)
        #hPa_value = match.group(4)
        #timestamp = match.group(5)
        logging.info("Received: %s\n", data)
        return he_value

def read_data_from_helium(repository, root):
    """
    Reads data from a Helium Analyzer device via serial communication.

    Args:
        repository: The repository object containing device configuration information.
        root: The root Tkinter window or frame to which messagebox will be parented.

    Returns:
        None

    """
    logging.info("Enter into read data from helium")

    helium_analyzer_config = repository.get_device_info_by('Helium Analyzer')
    port = helium_analyzer_config.port
    if port:
        try:
            baud_rate = helium_analyzer_config.baudrate
            ser = serial.Serial(port, baud_rate)
            return read_from_serial(ser, root)
        except serial.SerialException as e:
            logging.info("Serial Exception Occurred: %s, while reading Helium Analyzer", str(e))
            print(f"Serial Exception Occurred: {str(e)}, while reading Helium Analyzer")
            messagebox.showerror("Error", "Failed to open Helium Analyzer.", parent=root)
    else:
        messagebox.showwarning("Warning", "Please specify a COM Port for Helium Analyzer.",
                               parent=root)
