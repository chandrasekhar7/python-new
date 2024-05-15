"""
denkovi_relay.py

This module defines the RelaySwitch class, which interacts with the Denkovi Relay Switch.
It provides methods to connect to the relay switch, set the state of individual relay channels
(turning devices on or off), and manage the power state of connected devices.

Key Class:
- RelaySwitch:
  - __init__(self, repository): Initializes the RelaySwitch instance with a Repository object.
  - connect(self, port=None): Connects to the Denkovi relay switch.
  - set_relay_state(self, device, state): Sets the state of a specific relay channel.
  - turn_on_devices(self): Turns on devices in the specified sequence.
  - turn_off_devices(self): Turns off devices in the specified sequence.
  - close(self): Closes the serial connection.

Dependencies:
- serial
- time
- logging

Usage:
This module is typically imported and an instance of the RelaySwitch class is created,
passing in the Repository object. The RelaySwitch instance can then be used to control
the power state of connected devices through the relay switch.
"""
import time
import logging
import serial

# Dictionary mapping device names to their corresponding relay channels
DEVICES = {
    "Inficon": 1,
    "Helium Solenoid Valve": 2,
    "Helium Analyzer": 3,
    "Mass Flow Controller": 4
}


class RelaySwitch:
    """
    Represents a Denkovi Relay Switch instance.

    This class provides methods to initialize the relay switch, connect to it, set relay states,
    and control devices connected to it.

    Args:
        repository (object): Repository object containing relay configuration.

    Attributes:
        config: Configuration information for the relay switch.
        relay: Serial connection to the relay switch.

    """
    def __init__(self, repository):
        """
        Initialize the Denkovi Relay Switch instance.

        :param repository: Repository object containing relay configuration
        """
        self.config = repository.get_device_info_by("Relay Switch")
        self.relay = None

    def connect(self, port=None):
        """
        Connect to the Denkovi relay Switch.

        :param port: Serial port to connect to the relay switch (optional)
        :return: True if connected successfully, False otherwise
        """
        try:
            self.relay = serial.Serial(port, self.config.baudrate)
            self.relay.write(b'\x5B\x01\x5D')  # Command: [01]
            time.sleep(0.1)
            response = self.relay.read(5)
            relay_states = response[1:5]  # Byte 1-4 indicate relay states

            # Print the status of each relay channel
            switch_status = []
            for i in range(4):
                state = 'ON' if relay_states[i] == 0x01 else 'OFF'
                switch_status.append(True if state == 'ON' else False )
                logging.info("Relay Channel %d: %s", i + 1, state)
                print(f"Relay Channel {i + 1}: {state}")

            return True, switch_status
        except serial.SerialException:
            logging.error("Failed to read relay status. Check serial connection.")
            print("Failed to read relay status. Check serial connection.")
            return False, []

    def set_relay_state(self, device, state):
        """
        Set the state of a specific relay channel.

        :param self: The RelaySwitch instance
        :param device: Name of the device
        :param state: State to set (0 for OFF, 1 for ON)
        :return: True if the relay state is set successfully, False otherwise
        """
        if device not in DEVICES:
            logging.error("Invalid device: %s", device)
            return False

        if state not in [0, 1]:
            logging.error("Invalid state value: %s. Must be 0 (OFF) or 1 (ON).", state)
            return False

        channel = DEVICES[device]
        command = f"\x5B\x11{channel:02d}{state:d}\x5D".encode()
        # Command: [11XX] where XX is channel and state
        try:
            self.relay.write(command)
            time.sleep(0.1)  # Wait for command to be processed

            # Read the response from the relay to check the status
            response = self.relay.read(5)
            if len(response) == 5 and response[0] == 0x5B and response[-1] == 0x5D:
                logging.info("%s set to %s", device, 'ON' if state == 1 else 'OFF')
                return True
        except serial.SerialException as e:
            logging.error("Serial communication error: %s", str(e))
            return False
        except Exception as e:
            logging.error("Unexpected error: %s", str(e))
            return False

    def turn_on_devices(self):
        """Turn on devices in the specified sequence."""
        logging.info("Turning on devices...")
        self.set_relay_state("Inficon", 1)
        self.set_relay_state("Helium Solenoid Valve", 1)
        self.set_relay_state("Helium Analyzer", 1)
        self.set_relay_state("Mass Flow Controller", 1)

    def turn_off_devices(self):
        """Turn off devices in the specified sequence."""
        logging.info("Turning off devices...")
        self.set_relay_state("Mass Flow Controller", 0)
        self.set_relay_state("Helium Analyzer", 0)
        self.set_relay_state("Helium Solenoid Valve", 0)
        self.set_relay_state("Inficon", 0)

    def close(self):
        """Close the serial connection."""
        if self.relay is not None:
            self.relay.close()
