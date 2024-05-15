"""
main_page.py

This module contains the main user interface and core functionality for the Leakware application.
It handles tasks such as creating the main window, establishing serial connections, controlling
measurements, managing data, and interacting with the database.

Key Functions:
- main_page(tk, root, mode_of_measurement, leakware_id, leak_detector_available,
            is_mass_flow_controller_available, repository, measurement_type):
  Main function to create the primary user interface and handle various functionalities.

- display_label(value_label): Function to update the leak rate display and plot in real-time.
- read(): Function to read the leak rate measurement from the leak detector.
- start(): Function to start a new leak test measurement.
- stop(): Function to stop the current leak test measurement.
- reconnect(): Function to reconnect to the leak detector and mass flow controller.
- calibration(): Function to perform internal calibration of the leak detector.
- delete_last(): Function to delete the last measurement entry.
- load_data_from_database(): Function to load measurement data from the database.
- create_table(): Function to create a table with measurement data.
- load_tree_view(): Function to load and display measurement data in a tree view.
- edit_cell(event, measurements_list): Function to handle editing of measurement data cells.
- update_cell(entry, item, col_index, measurements_list): Function to update a measurement
data cell.
- get_measurement_id(selected_item, measurements_list): Function to get the measurement ID
from a selected item.
- highest_value(): Function to display the highest leak rate value.
- get_mass_flow_data(): Function to get data from the mass flow controller.
- adjust_flow_rate(sccm_increment): Function to adjust the flow rate of the mass flow controller.
- update_sensor_data(): Function to continuously update sensor data.
- clear_highest(): Function to clear the highest leak rate value.
- graph_clear(): Function to clear the measurement graph.
- clear_both(): Function to clear both the measurement graph and highest value.
- auto_stop(): Function to handle automatic stopping of measurements based on conditions.
- auto_button(): Function to start the auto-stop process.
- close(): Function to close the application and handle cleanup tasks.
- animate(i): Function to animate the measurement graph.

Dependencies:
- tkinter
- matplotlib
- numpy
- pandas
- threading
- time
- datetime
- json
- logging
- serial
- db_model
- Pem_mode
- profil_specification
- Settings
- create_report
- helium
- pressure_gauge
- denkovi_relay

Usage:
This module is typically imported and used as the main application logic for the Leakware software.
The `main_page` function is called with the necessary arguments to create and manage the primary
user interface,
handle device connections, control measurements, and interact with the database.
"""
import json
import logging
from tkinter import messagebox
import threading
import time
from datetime import datetime
import random
import serial
import serial.tools.list_ports
import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FormatStrFormatter
from Pem_mode import pem_mode_config
from profil_specification import profil_specification
from db_model import Measurements, Specimens
from compare_graph import compare
from Settings import settings
from create_report import create_report
from helium import read_data_from_helium
from pressure_gauge import check_pressure_gauge
from denkovi_relay import RelaySwitch


def set_stop_flag():
    """
    Set the stop flag to indicate stopping condition.

    This function sets a global flag variable `stop_flag` to True,
    indicating that a stopping condition has been triggered.

    Returns:
        None
    """
    global stop_flag
    stop_flag = True


def main_page(
    tk,
    root,
    mode_of_measurement,
    leakware_id,
    leak_detector_available,
    is_mass_flow_controller_available,
    repository,
    measurement_type,
):
    '''
     this is method we are calling for measurement.
    '''
    global tree

    global stop_flag
    stop_flag = False

    global show_popup
    show_popup = 1

    def call_pem_mode():
        main_root = tk.Toplevel(root)
        pem_mode_config(
            tk, main_root, mode_of_measurement, leakware_id, repository
        )

    def profil_spec():
        main_root = tk.Toplevel(root)
        profil_specification(
            tk, main_root, mode_of_measurement, leakware_id, repository
        )

    def call_settings():
        main_root = tk.Toplevel(root)
        settings(
            tk,
            main_root,
            leak_detector_available,
            is_mass_flow_controller_available,
            mode_of_measurement,
            repository,
        )

    def create_report_pem():
        report_root = tk.Toplevel(root)
        create_report(tk, report_root, repository, leakware_id, mode_of_measurement)

    def custom_command():
        if mode_of_measurement == "PEM":
            call_pem_mode()
        else:
            profil_spec()

    def load_cfg(ports=None):
        global leakware_config
        global mass_flow_config
        global helium_analyzer_config
        nonlocal leak_detector_available
        nonlocal is_mass_flow_controller_available

        leakware_config = repository.get_device_info_by("Leak Detector")
        mass_flow_config = repository.get_device_info_by("Mass Flow Controller")
        if ports:
            for port in ports:
                if port == leakware_config.port:
                    leakware_config.is_available = True
                elif port == mass_flow_config.port:
                    mass_flow_config.is_available = True
        leak_detector_available = leakware_config.is_available
        is_mass_flow_controller_available = mass_flow_config.is_available
        try:
            repository.update_device_info()
        except Exception as e:
            print("An error occurred while updating device info:", e)
            logging.error("An error occured while updating device info in load_cfg method in main_page.py: %s", str(e))

    load_cfg()

    def display_label(value_label):
        def display_refresh():
            global measurement
            global start_time
            global seconds_elapsed
            global auto_onoff
            global xs, ys, ys2

            end_time = time.time()
            seconds_elapsed = end_time - start_time

            if on_off != 0:
                measurement = read()
                if measurement >= 0.005:
                    value_label.config(
                        text=f"{measurement:10.4e}",
                        fg="red",
                        font=("arial", 14, "bold"),
                    )
                else:
                    value_label.config(
                        text=f"{measurement:10.4e}",
                        fg="green",
                        font=("arial", 14, "bold"),
                    )

                if len(xs) > 0:
                    if seconds_elapsed != 0:
                        xs.append(seconds_elapsed)
                        ys.append(measurement)
                else:
                    xs.append(seconds_elapsed)
                    ys.append(measurement)

                if auto_onoff == 1:
                    auto_stop()
                if 3 <= seconds_elapsed <= 5:
                    clear_both()
                if 6 <= seconds_elapsed:
                    highest_value()
                ys2.append(measurement)

                time.sleep(0.01)
                tr = threading.Thread(target=display_refresh)
                tr.start()

            else:
                print("Process finished.\n")

        display_refresh()

    def read():
        measure_val = 0

        try:
            serialPort_leakDetector.flushInput()
            serialPort_leakDetector.write(
               "*read?\r".encode()
            )  # Send the command to retrieve the leak rate
            time.sleep(0.1)  # Wait for a short delay to ensure the command is processed
            measure_val = float(serialPort_leakDetector.readline())
            #measure_val = float(random.choice([random.random() for _ in range(10)]))
            if measure_val > 0 and isinstance(measure_val, float):
                return measure_val
            else:
                return read()  # Retry reading if the value is not valid

        except serial.SerialException as e:
            print(
                f"Serial communication error occurred: {str(e)}, while reading leak rate. Retrying..."
            )
            logging.info(
                "Serial communication error occurred: %s, while reading leak rate. Retrying...", str(e)
            )
            read()  # Retry reading if a serial communication error occurs
        except ValueError as v:
            print(
                f"Invalid response received: {str(v)}, while reading leak rate. Retrying..."
            )
            logging.info(
                "Invalid response received: %s, while reading leak rate. Retrying...", str(v)
            )
            read()  # Retry reading if an invalid response is received

    def start():
        global on_off
        global start_time
        global element_no
        global serialPort_leakDetector
        global serial_port_mass_flow_controller
        global directory_path
        global temperature_array
        nonlocal leak_detector_available
        global settings_onoff

        temperature_array = []

        reconnect()

        if leak_detector_available:
            try:
                serialPort_leakDetector.flushInput()
                # Flush the input buffer of the serial port for the leak detector
                # Send the '*start\r' command to the leak detector to start the measurement
                serialPort_leakDetector.write("*start\r".encode())

                time.sleep(0.05)

                # Flush the output buffer of the serial port for the leak detector
                serialPort_leakDetector.flushOutput()
            except serial.SerialException as e:
                print(
                    f"Serial Exception occurred: {str(e)}, while starting the measurement. Retrying..."
                )
                logging.info(
                    "Serial Exception occurred: {str(e)}, while starting the measurement. Retrying..."
                )
                settings_onoff = False
                start()  # Recursively call the start() function to retry starting the measurement

            on_off = 1
            auto_onoff = 0
            start_time = 0
            start_time = time.time()
            display_label(value_label)
            clear_both()
            return on_off

    def stop():
        global on_off
        global auto_onoff
        global element_no
        global xs
        global ys
        global element_listx
        global element_listy
        global temperature_array
        global serialPort_leakDetector
        nonlocal leak_detector_available

        on_off = 0
        element_listx.append(xs)
        element_listy.append(ys)

        print(temperature_array)

        if leak_detector_available:
            try:
                serialPort_leakDetector.write("*stop\r".encode())
                time.sleep(0.75)

                serialPort_leakDetector.write("*vent\r".encode())
                time.sleep(0.05)

                serialPort_leakDetector.flushOutput()
                time.sleep(0.5)

                serialPort_leakDetector.write("*vent\r".encode())
                time.sleep(0.05)

                serialPort_leakDetector.flushOutput()
            except serial.SerialException as e:
                print(
                    f"Serial communication error occurred during the stop sequence: {str(e)}"
                )
                logging.info(f"Serial communication error occurred during the stop sequence: {str(e)}")

        element_no += 1

        if auto_onoff == 1:
            button_autostop.config(bg=color1)
            print("Autostop cancelled.")
            auto_onoff = 0

        create_table()
        time.sleep(1)
        load_data_from_database()

    def reconnect():
        global serialPort_leakDetector
        global serial_port_mass_flow_controller
        global settingsdict_leakDetector
        global settingsdict_massFlowController
        global port_leakDetector
        global port_massFlow
        global element_no
        global leakware_config
        global mass_flow_config
        nonlocal leak_detector_available
        nonlocal is_mass_flow_controller_available
        global settings_onoff
        global settings_onoff2

        ports = serial.tools.list_ports.comports()
        load_cfg(ports)

        if ports != []:

            if leak_detector_available:
                try:
                    settingsdict_leakDetector = {
                        "baudrate": leakware_config.baudrate,
                        "bytesize": int(leakware_config.bytesize),
                        "parity": leakware_config.parity,
                        "stopbits": int(leakware_config.stopbits),
                        "xonxoff": False,
                        "dsrdtr": False,
                        "rtscts": False,
                        "timeout": 1,
                        "write_timeout": None,
                        "inter_byte_timeout": None,
                    }
                    if not settings_onoff:
                        serialPort_leakDetector = serial.Serial(
                            port=leakware_config.port
                        )
                        serialPort_leakDetector.apply_settings(
                            settingsdict_leakDetector
                        )
                        settings_onoff = True
                    else:
                        serialPort_leakDetector = serial.Serial(
                            port=leakware_config.port
                        )
                        serialPort_leakDetector.apply_settings(
                            settingsdict_leakDetector
                        )
                except serial.SerialException as e:
                    logging.error("reconnect serial exception: %s", str(e))
                    print("reconnect serial exception:" + str(e))
                    if element_no == 0:
                        if not settings_onoff:
                            print("No Leak Detector connected.")
                try:
                    settingsdict_massFlowController = {
                        "baudrate": mass_flow_config.baudrate,
                        "bytesize": int(mass_flow_config.bytesize),
                        "parity": mass_flow_config.parity,
                        "stopbits": int(mass_flow_config.stopbits),
                        "xonxoff": False,
                        "dsrdtr": False,
                        "rtscts": False,
                        "timeout": 1,
                        "write_timeout": None,
                        "inter_byte_timeout": None,
                    }
                    if not settings_onoff2:
                        serial_port_mass_flow_controller = serial.Serial(
                            port=mass_flow_config.port
                        )
                        serial_port_mass_flow_controller.apply_settings(
                            settingsdict_massFlowController
                        )
                        settings_onoff2 = True
                    else:
                        serial_port_mass_flow_controller = serial.Serial(
                            port=mass_flow_config.port
                        )
                        serial_port_mass_flow_controller.apply_settings(
                            settingsdict_massFlowController
                        )
                except:
                    if element_no == 0:
                        if not settings_onoff2:
                            print("No Mass_Flow_Controller connected.")

            else:
                print("No default COM port found. Check connection or port settings.")
                messagebox.showerror(
                    title="COM Check",
                    message="No default COM port found. Check connection or port settings.",
                    parent=root,
                )

        else:
            print("Check COM port and ensure devices are powered on - none detected")
            messagebox.showerror(
                title="COM Port Check",
                message="Check COM port and ensure devices are powered on - none detected",
                parent=root,
            )

    def calibration():
        global serialPort_leakDetector
        nonlocal leak_detector_available

        reconnect()

        if leak_detector_available:
            serialPort_leakDetector.flushInput()
            serialPort_leakDetector.write("*hour:pow?\r".encode())
            time.sleep(0.05)
            time_pwon = int(serialPort_leakDetector.readline().decode())
            time.sleep(0.05)
            serialPort_leakDetector.flushOutput()
            time.sleep(1)
            print(time_pwon)

            if time_pwon >= 21:
                print("Calibrating.")

                def lbl3():
                    value_label.config(text="-", fg="black")

                def lbl2():
                    serialPort_leakDetector.flushInput()
                    serialPort_leakDetector.write("*stat:calh 1?\r".encode())
                    time.sleep(0.05)
                    serialPort_leakDetector.flushOutput()
                    time.sleep(1)
                    cal = serialPort_leakDetector.readline().decode()
                    cal = cal.split()[-1]
                    print(f"Calibration factor: {cal}")
                    value_label.config(
                        text=(f"Calibration factor:\n {cal}"), fg="blue"
                    )  # 11
                    value_label.after(15000, lbl3)

                def lbl1():
                    value_label.config(text="Calibrating...", fg="blue")  # 16
                    serialPort_leakDetector.write("*cal\r".encode())
                    time.sleep(0.05)
                    serialPort_leakDetector.flushOutput()
                    value_label.after(40000, lbl2)

                lbl1()

            else:

                def lbl5():
                    value_label.config(text="-", fg="black")

                def lbl4():
                    print(
                        "After power on, wait about 20 minutes to start the calibration."
                    )
                    value_label.config(
                        text="Power on: "
                        + str(time_pwon)
                        + "min"
                        + "\n Wait at least "
                        + str(20 - time_pwon)
                        + " min.",
                        fg="blue",
                        font=("arial", 14),
                    )
                    value_label.after(10000, lbl5)

                lbl4()

    def delete_last():
        global tree
        repository.delete_last_measurement(leakware_id)
        load_tree_view()
        print("last measurement deleted")

    def load_data_from_database():
        global element_listx
        global element_listy

        element_listx = []
        element_listy = []

        try:

            specimens = repository.get_all_specimens(leakware_id)
            for specimen in specimens:
                element_listx.append(json.loads(specimen.x_value))
                element_listy.append(json.loads(specimen.y_value))
        except Exception as e:
            # Log the error for debugging purposes
            logging.error("Error occurred while loading data from database: %s", str(e))
            messagebox.showerror(
                "Error", "Failed to load data from database. Please try again."
            )

    def create_table():
        global element_no
        global measurement
        global xs
        global ys
        global ys2
        global seconds_elapsed
        global row_elemno
        global row_time
        global row_measurement
        global row_highest
        global tree
        global df
        global data_information_id
        global auto_onoff
        global temperature_array

        row_elemno.append(element_no)
        row_time.append(round(seconds_elapsed, 1))
        row_measurement.append(f"{measurement:10.2e}")
        row_highest.append(f"{max(ys2, default=0):10.2e}")

        data = {
            "no.": row_elemno,
            "time [s]": row_time,
            "value [mbarˑl/s]": row_measurement,
            "max [mbarˑl/s]": row_highest,
        }
        df = pd.DataFrame(data)
        pd.set_option("display.max_rows", None)
        print(df)

        if "data_information_id" not in globals():
            data_information_id = None

        average_temperature = 0

        try:
            average_temperature = sum(temperature_array) / len(temperature_array)
        except ZeroDivisionError:
            logging.error("Room Temperature List is empty")

        # Insert data into measurements table
        panel_no, location_no = repository.get_panel_and_location_number(leakware_id)
        if measurement > 0:
            logging.info("Measurement Creation")

            try:
                if ys2:
                    max_value = f"{max(ys2):10.2e}"
                else:
                    max_value = "0.00e+00"  # Set a default value when ys2 is empty

                measurement_db = Measurements(
                    leakware_id=leakware_id,
                    data_information_id=data_information_id,
                    serial_number=element_no,
                    time_in_seconds=round(seconds_elapsed, 1),
                    value_mbarl_second=f"{measurement:10.2e}",
                    max_value=f"{max(ys2, default=0):10.2e}",
                    autostop=auto_onoff,
                    panel_no=panel_no,
                    location_no=location_no,
                    average_temperature=average_temperature,
                    he_pressure="Testing",
                    he_percentage="Testing",
                    he_massflow_value="Testing",
                    active=True,
                )
                measurement_db.average_temperature = average_temperature
                measurement_id = repository.insert_measurement(
                    measurement_db
                ).measerment_Id
                measurement = 0
                logging.info("Measurement Id is : %s", measurement_id)

                if len(xs) > 0 and len(ys) > 0:
                    specimen = Specimens(
                        measerment_Id=measurement_id,
                        x_value=json.dumps(xs),
                        y_value=json.dumps(ys),
                        leakware_id=leakware_id,
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                    )
                    repository.insert_specimens(specimen)

                try:
                    repository.commit()  # Commit the session changes
                except Exception as e:
                    logging.error("Error occurred while committing the session: %s", str(e))
                    repository.session.rollback()
                    raise  # Re-raise the exception for proper error handling
                load_tree_view()
            except Exception as e:
                logging.error("Error occurred while creating measurement: %s", str(e))
                repository.session.rollback()  # Rollback the transaction if an error occurs
                raise  # Re-raise the exception for proper error handling

    def load_tree_view():
        tree.delete(*tree.get_children())

        row_lst = []
        measurements_list = repository.get_all_measurements_data(leakware_id)
        for numbr, measurement in enumerate(measurements_list, start=1):
            row_lst.append(
                (
                    measurement.panel_no,
                    measurement.location_no,
                    measurement.time_in_seconds,
                    f"{float(measurement.value_mbarl_second):10.1e}",
                    f"{float(measurement.max_value):10.1e}",
                )
            )
            tree.insert("", "end", values=row_lst[numbr - 1])
        tree.bind("<Double-1>", lambda event: edit_cell(event, measurements_list))
        tree.yview_moveto(1)

    def edit_cell(event, measurements_list):
        item = tree.selection()[0]
        column = tree.identify_column(event.x)
        row = tree.identify_row(event.y)
        col_index = int(column[1:]) - 1

        # Check if the column index is one of the editable columns
        if col_index in (0, 1):
            # Get the bounding box of the cell
            x, y, width, height = tree.bbox(item, column)

            # Create entry widget
            entry = tk.Entry(tree, bd=0)
            entry.place(x=x, y=y, width=width, height=height)
            entry.insert(0, tree.item(item)["values"][col_index])
            entry.bind(
                "<FocusOut>",
                lambda event: update_cell(entry, item, col_index, measurements_list),
            )
            entry.bind(
                "<Return>",
                lambda event: update_cell(entry, item, col_index, measurements_list),
            )
            entry.bind("<Escape>", lambda event: entry.destroy())

            # Focus and select entry widget
            entry.focus_set()
            entry.selection_range(0, "end")

    def update_cell(entry, item, col_index, measurements_list):
        new_value = entry.get()
        tree.set(item, column=f"#{col_index + 1}", value=new_value)
        measurement_id = get_measurement_id(item, measurements_list)
        column_name = "panel_no" if col_index == 0 else "location_no"
        try:
            repository.update_measurement_by_id(measurement_id, column_name, new_value)
        except Exception as e:
            print("An error occurred while updating measurement:", e)
            logging.error("An error occurred while updating measurement in update cell method in main page: %s", str(e))
        entry.destroy()

    def get_measurement_id(selected_item, measurements_list):
        # Get the index of the selected item in the Treeview
        index = tree.index(selected_item)
        # Get the measurement ID from the measurements_list using the index
        return measurements_list[index].measerment_Id

    def highest_value():
        global measurement
        global ys2
        value = measurement

        if max(ys2, default=0) >= 0.005:
            highest_label.config(
                text=f"{max(ys2, default=0):10.4e}",
                fg="red",
                font=("arial", 14, "bold"),
            )
        else:
            highest_label.config(
                text=f"{max(ys2, default=0):10.4e}",
                fg="green",
                font=("arial", 14, "bold"),
            )

        if value > max(ys2, default=0):
            value = measurement
            if measurement >= 0.005:
                highest_label.config(text=f"{value:10.4e}", fg="red")
            else:
                highest_label.config(text=f"{value:10.4e}", fg="green")

    def get_mass_flow_data():
        global serial_port_mass_flow_controller
        sccm_val = 0.0
        temp_v = 0.0

        try:
            if is_mass_flow_controller_available:
                for i in range(0, 2):
                    i += 1
                    serial_port_mass_flow_controller.flushInput()
                    serial_port_mass_flow_controller.write("*@=A\r".encode())
                    serial_port_mass_flow_controller.flushInput()
                    value_sens = serial_port_mass_flow_controller.read_until(
                        "\r"
                    ).decode()
                    value_sens_list = value_sens.split(" ")
                    temp_v = value_sens_list[2]
                    sccm_val = value_sens_list[4]
        except serial.SerialException as e:
            print(
                f"Serial communication error occurred: {str(e)}, in get_mass_flow_data"
            )
            logging.info("Serial communication error occurred: %s, in get_mass_flow_data", str(e))
        except Exception as e:
            print("An error occurred while getting mass flow data:", e)
            logging.info("An error occurred while getting mass flow data:%s", str(e))
            # You might want to handle the error in a specific way or log it.
            return [sccm_val, temp_v]

        return [sccm_val, temp_v]

    def adjust_flow_rate(sccm_increment):
        logging.info("set_value_to_mass_flow_controller")
        global serial_port_mass_flow_controller

        if is_mass_flow_controller_available:
            mass_flow_config = repository.get_device_info_by("Mass Flow Controller")
            flowrate = str((mass_flow_config.sccm_value + sccm_increment) * 64000 / 500)
            logging.info("Revised Flow Rate in SCCM is: %s", flowrate)

            # Send the revised flow rate to Mass flow controller
            try:
                serial_port_mass_flow_controller.flushInput()
                serial_port_mass_flow_controller.write("*@=A\r".encode())
                time.sleep(0.2)
                serial_port_mass_flow_controller.flushInput()
                serial_port_mass_flow_controller.write(("*" + flowrate + "\r").encode())
                serial_port_mass_flow_controller.flushOutput()

                # Update the revised flow rate to the Mass Flow Controller Table
                mass_flow_config.sccm_value = flowrate
                repository.update_device_info()  # This will update the values in the DB object mass_flow_config
            except serial.SerialException as e:
                print(
                    f"Serial Exception occurred: {str(e)}. Revised Flow Rate {flowrate} not applied"
                )
                logging.info("Serial Exception occurred: %s. Revised Flow Rate %s not applied", str(e), flowrate)

    def update_sensor_data():
        global on_off
        global temperature_array
        global show_popup
        global stop_flag
        relay_switch = RelaySwitch(repository)
        while not stop_flag:
            logging.info(
                "=============================mass flow temperature============================="
            )
            if is_mass_flow_controller_available:
                sccm_val, mass_flow_temperature = get_mass_flow_data()
                if mass_flow_temperature > 45:
                    button_start.config(state="disabled")

                    if repository.get_device_serial_info_by(
                        "Relay Switch"
                    ).is_available:

                        # Turn off Mass Flow Controller
                        mass_flow_relay_channel = relay_switch.set_relay_state(
                            "Mass Flow Controller", 0
                        )
                        if mass_flow_relay_channel:
                            logging.info("Turning OFF Mass Flow Controller, as it is nearing it's max operating temperature: %s", mass_flow_temperature)
                            print(
                                f"Turning OFF Mass Flow Controller, as it is nearing it's max operating temperature: {mass_flow_temperature}"
                            )

                        # Turn off Helium Solenoid Valve
                        solenoid_valve_relay_channel = relay_switch.set_relay_state(
                            "Helium Solenoid Valve", 0
                        )
                        if solenoid_valve_relay_channel:
                            logging.info("Turning OFF Solenoid Valve as Mass Flow Controller is nearing it's max operating temperature: %s", mass_flow_temperature)
                            print(
                                f"Turning OFF Solenoid Valve as Mass Flow Controller is nearing it's max operating temperature: {mass_flow_temperature}"
                            )
                else:
                    button_start.config(state="normal")
                helium_massflow_value.config(text=sccm_val)
                print(f"SCCM Value is: {sccm_val}")

            pressure, temperature = check_pressure_gauge(repository)
            if pressure is not None and temperature is not None:
                if on_off == 1:
                    temperature_array.append(temperature)
                if root.winfo_exists():  # check if the root window exists
                    if room_temp_value.winfo_exists():
                        room_temp_value.config(text=f"{temperature:.2f}")
                    # check if the pressure is 30 bar or below and change the color to red
                    if helium_pressure_value.winfo_exists():
                        if pressure <= 30:
                            helium_pressure_value.config(
                                text=f"{pressure:.2f}", fg="red"
                            )
                        else:
                            helium_pressure_value.config(
                                text=f"{pressure:.2f}", fg="green"
                            )

            helium_analyser_config = repository.get_device_info_by("Helium Analyzer")
            if helium_analyser_config.is_available:
                helium_value = read_data_from_helium(repository, root)
                logging.info(f"helium value is : {helium_value}")

                if helium_value is not None:
                    if helium_value < 95.0:
                        if show_popup == 1:
                            messagebox.showerror(
                                "Error", "Helium Value is below threshold", parent=root
                            )
                            messagebox.showwarning(
                                "Warning",
                                "Increasing the sccm value by 1, Please wait for a moment",
                                parent=root,
                            )
                            adjust_flow_rate(1)  # Increase the SCCM by 1
                            time.sleep(60)  # To allow the increased SCCM take effect
                            show_popup = 0
                    else:
                        show_popup = 1
                    helium_concentration_value.config(text=helium_value)
            print("updated sensor data")
            time.sleep(1)

    def clear_highest():
        global ys2
        ys2 = []
        highest_label.config(text="-")

    def graph_clear():
        global xs
        global ys
        global ys2

        xs, ys, ys2 = [], [], []

    def clear_both():
        graph_clear()
        clear_highest()

    def auto_stop():
        global measurement
        global seconds_elapsed
        global seconds_autostop
        global auto_onoff
        global auto_value
        autotime = textbox_autotime.get(1.0, "end-1c")
        # print(round((seconds_elapsed - seconds_autostop), 2))
        if not (measurement * 5 > auto_value > measurement / 5):
            button_autostop.config(bg="red")
            print("Autostop measurement out of range.")
            auto_button()
        elif (measurement * 5 > auto_value > measurement / 5) and (
            seconds_elapsed - seconds_autostop >= int(autotime)
        ):
            button_autostop.config(bg=color1)
            print("Autostop measurement finished.")
            auto_onoff = 0
            stop()
        else:
            button_autostop.config(bg="green")

    def auto_button():
        print("Autostop started.")
        global auto_onoff
        global seconds_autostop
        global auto_value
        auto_value = measurement
        print(auto_value)
        seconds_autostop = seconds_elapsed
        auto_onoff = 1

    def close():
        global on_off
        global stop_flag
        stop_flag = True

        if on_off == 1:
            stop()
        try:
            if serialPort_leakDetector is not None:
                serialPort_leakDetector.close()
        except serial.SerialException as e:
            print(
                f"Serial Exception Occurred: {str(e)}. Unable to close Serial Connection"
            )

        try:
            if (
                serial_port_mass_flow_controller in globals()
                and serial_port_mass_flow_controller is not None
            ):
                serial_port_mass_flow_controller.close()
            print("serial closed.")
        except NameError:
            pass  # Variable not defined, ignore the exception
        except serial.SerialException as e:
            print(
                f"Serial Exception Occurred: {str(e)}. Unable to close Serial Connection"
            )

        thread1.join()  # wait for the update_sensor_data thread to complete

        repository.close_session()

        try:
            root.quit()
            root.destroy()
        except Exception as e:
            print(f"Error occurred while closing the window: {str(e)}")

        # Turning Off all devices
        time.sleep(2)  # To allow any previous commands to complete.
        relay_switch = RelaySwitch(repository)
        relay_switch.turn_off_devices()

        exit()

    def animate(i):
        global measurement
        global xs
        global ys
        global ys2
        global toggle_value

        if toggle_value == 0:
            ax1.clear()
            ax1.grid()
            ax1.set_yscale("symlog")
            ax1.set_xlabel("Time [s]")
            ax1.set_ylabel("Leakrate [mbarl/s]")
            ax1.yaxis.set_major_formatter(FormatStrFormatter("%2.1e"))
            if len(ys) > 0:
                ax1.plot(xs[:-1], ys[:-1])
            else:
                ax1.plot(xs, ys)
        else:
            ax1.clear()
            ax1.grid()
            ax1.set_xlabel("Specimen/Location")
            ax1.set_ylabel("Highest Leakrate [mbarˑl/s]")
            ax1.set_title("Trend of Highest Leak rates")

            highest_values = []
            for element_no_in_listy in element_listy:
                highest_values.append(max(element_no_in_listy))
            highest_values.append(max(ys2, default=0))
            x_values = list(range(1, len(highest_values) + 1))
            ax1.plot(
                x_values, highest_values, marker="o", color="blue", label="specimen"
            )
            plt.xticks(range(len(x_values)), x_values)

    def set_toggle():
        global toggle_value

        toggle_value = toggle_value + 1 if toggle_value == 0 else 0

    graph_clear()
    # root = tk.Tk()

    # color1 = "#c4e4ff"
    # color1 = "#c4cfff"
    color2 = "#0533ff"  # full blue
    color3 = "#e6efff"  # light color1
    color4 = "#c4cfff"  # light blue
    color1 = "#2049b0"  # profilblau?
    colorf = "#ffffff"  # font #white

    root.title(mode_of_measurement + " Leakware")
    if mode_of_measurement == "PEM":
        root.iconbitmap("favicon.ico")
    root.configure(background="white")
    root.geometry("1000x600")

    # try:
    #     os.mkdir("./Data/")
    #     print("Directory /Data created.")
    # except:
    #     print("Directory already created.")

    # Graph
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.yaxis.set_major_formatter(FormatStrFormatter("%2.1e"))

    graph_frame = tk.Frame(root, bg="black")
    graph_frame.place(relx=0.35, rely=0.275, relwidth=0.7, relheight=0.65, anchor="nw")
    graph = FigureCanvasTkAgg(fig, master=graph_frame)
    graph.get_tk_widget().pack(fill="both", expand=True)
    ani = animation.FuncAnimation(fig, animate, interval=0.01, cache_frame_data=False)
    graph.draw()

    frame_logo = tk.Frame(root, bg="white")
    if mode_of_measurement == "PEM":
        image_path = "./Images/PEM.png"
        frame_logo.place(relx=0.07, rely=0, relheight=0.3, relwidth=0.2, anchor="n")
    else:
        image_path = "./Images/PROFIL.png"
        frame_logo.place(relx=0.12, rely=0, relheight=0.3, relwidth=0.3, anchor="n")

    ### PROFIL Logo
    logo = tk.PhotoImage(file=image_path)
    logo_label = tk.Label(frame_logo, image=logo)
    logo_label.place(relx=0, rely=0, relheight=0.9, relwidth=1, anchor="nw")

    ### START
    button_start = tk.Button(
        root,
        text="Start Measurement",
        font=("arial", 12, "bold"),
        bg=color1,
        fg=colorf,
        command=start,
    )
    button_start.place(
        relx=0.01, rely=0.28, relheight=0.125, relwidth=0.225, anchor="nw"
    )

    ### STOP
    button_stop = tk.Button(
        root,
        text="Stop \nMeasurement",
        font=("arial", 12, "bold"),
        bg=color1,
        fg=colorf,
        command=stop,
    )
    button_stop.place(relx=0.01, rely=0.415, relheight=0.11, relwidth=0.15, anchor="nw")

    ### Auto STOP
    button_autostop = tk.Button(
        root,
        text="Auto Stop",
        font=("arial", 10, "bold"),
        bg="green",
        command=auto_button,
        fg=colorf,
    )
    button_autostop.place(
        relx=0.165, rely=0.415, relheight=0.05, relwidth=0.07, anchor="nw"
    )
    auto_save_border = tk.Frame(
        root, bg=colorf, bd=1, highlightbackground=color1, highlightthickness=1
    )
    auto_save_border.place(
        relx=0.165, rely=0.48, relheight=0.043, relwidth=0.042, anchor="nw"
    )
    textbox_autotime = tk.Text(root, font=("arial"), bg="white")  # 12
    textbox_autotime.place(
        relx=0.166, rely=0.482, relheight=0.04, relwidth=0.04, anchor="nw"
    )
    textbox_autotime.insert(1.0, "90")
    textbox_autotime.tag_configure("center", justify="center")
    textbox_autotime.tag_add("center", "1.0", "end")
    auto_save_unit = tk.Label(root, text="Sec", bg=colorf, font=("Arial", 10))
    auto_save_unit.place(relx=0.210, rely=0.485, anchor="nw")

    # Element Spec
    if measurement_type != "Quick Test":
        button_element_spec = tk.Button(
            root,
            text="Element Spec",
            font=("arial", 12, "bold"),
            bg=color1,
            fg=colorf,
            command=custom_command,
        )
        button_element_spec.place(
            relx=0.01, rely=0.535, relheight=0.057, relwidth=0.13, anchor="nw"
        )

    ### Clear Graph
    button_clear_graph = tk.Button(
        root,
        text="Clear Graph",
        font=("arial", 11),
        bg=color1,
        fg=colorf,
        command=graph_clear,
    )
    button_clear_graph.place(
        relx=0.149, rely=0.535, relheight=0.057, relwidth=0.085, anchor="nw"
    )

    from tkinter import ttk

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", fieldbackground=color3)
    style.configure(
        "Treeview.Heading",
        background=color1,
        foreground=colorf,
        font=("Arial", 7, "bold"),
        padding=(0, 5),
    )
    tree = ttk.Treeview(
        root,
        columns=("panel", "location", "time", "leakRate", "MaxLeakRate"),
        show="headings",
        height=30,
    )
    tree.pack(fill="both", expand=True)

    tree.heading("#0", text="\n\n\n")
    tree.heading("panel", text="Panel No")
    tree.heading("location", text="Location \nNo")
    tree.heading("time", text="Time (sec)")
    tree.heading("leakRate", text="Leak rate \n[mbar.L\n/sec]")
    tree.heading("MaxLeakRate", text="Max Leak \nrate \n[mbar.L\n/sec]")
    tree.column("panel", width=20)
    tree.column("location", width=20)
    tree.column("time", width=20)
    tree.column("leakRate", width=20)
    tree.column("MaxLeakRate", width=20)

    tree.tag_configure("even", background="#c4cfff")
    tree.tag_configure("odd", background=color3)
    relx = 0.0115
    rely = 0.6
    relwidth = 0.225
    relheight = 0.3
    tree.place(relx=0.122, rely=0.6, relheight=0.3, relwidth=0.225, anchor="n")
    for col in range(0, 6):
        separator = ttk.Separator(root, orient="vertical")
        separator.place(
            relx=relx + (col * relwidth / 5),
            rely=rely,
            relheight=relheight,
            width=2,
            anchor="ne",
        )
    separator = ttk.Separator(root, orient="horizontal")
    separator.place(relx=0.236, rely=0.9, relwidth=0.225, width=2, anchor="ne")
    style.configure(
        "Separator.TSeparator",
        background="white",
        foreground=colorf,
        fieldbackground=colorf,
    )

    # Current Value
    current_value_border = tk.Frame(
        root, bg=colorf, bd=1, highlightbackground=color1, highlightthickness=1
    )
    current_value_border.place(
        relx=0.6, rely=0.02, relheight=0.14, relwidth=0.25, anchor="n"
    )
    value_label = tk.Label(root, bg=colorf)
    value_label.place(relx=0.6, rely=0.021, relheight=0.138, relwidth=0.248, anchor="n")
    current_value_label = tk.Label(
        root,
        text="Current Leak rate (mbar*l/s)",
        bg=colorf,
        font=("Arial", 10),
        justify="left",
    )
    current_value_label.place(relx=0.6, rely=0.12, anchor="n")

    # Highest Value
    highest_value_border = tk.Frame(
        root, bg=colorf, bd=1, highlightbackground=color1, highlightthickness=1
    )
    highest_value_border.place(
        relx=0.6, rely=0.165, relheight=0.125, relwidth=0.25, anchor="n"
    )
    highest_label = tk.Label(root, bg=colorf)
    highest_label.place(
        relx=0.6, rely=0.166, relheight=0.122, relwidth=0.248, anchor="n"
    )
    highest_value_label = tk.Label(
        root,
        text="Highest Leak rate (mbar*l/s)",
        bg=colorf,
        font=("Arial", 10),
        justify="left",
    )
    highest_value_label.place(relx=0.6, rely=0.25, anchor="n")

    # Delete Last Measurement Entry
    button_delete_last = tk.Button(
        root,
        text="Delete Last \nMeasurement Entry",
        font=("arial", 11),
        bg=color1,
        fg=colorf,
        command=delete_last,
    )
    button_delete_last.place(
        relx=0.0775, rely=0.93, relheight=0.057, relwidth=0.136, anchor="n"
    )

    ### Internal calibration
    button_cal = tk.Button(
        root,
        text="Internal Calibration",
        font=("arial", 11),
        bg=color1,
        fg=colorf,
        command=calibration,
    )
    button_cal.place(
        relx=0.2175, rely=0.93, relheight=0.057, relwidth=0.136, anchor="n"
    )

    ### Settings
    button_settings = tk.Button(
        root,
        text="Settings",
        font=("arial", 11),
        bg=color1,
        fg=colorf,
        command=call_settings,
    )
    button_settings.place(
        relx=0.3285, rely=0.93, relheight=0.057, relwidth=0.080, anchor="n"
    )

    ### Toggle Graph Types
    toggle_graph_button = tk.Button(
        root,
        text="Toggle Graph types",
        font=("arial", 11),
        bg=color1,
        fg=colorf,
        command=set_toggle,
    )
    toggle_graph_button.place(
        relx=0.4395, rely=0.93, relheight=0.057, relwidth=0.136, anchor="n"
    )

    ### Compare
    compare_graph = tk.Button(
        root,
        text="Compare",
        font=("arial", 11),
        bg=color1,
        fg=colorf,
        command=lambda: compare(leakware_id, mode_of_measurement, root, repository),
    )
    compare_graph.place(
        relx=0.5535, rely=0.93, relheight=0.057, relwidth=0.080, anchor="n"
    )

    ### Report
    report_button = tk.Button(
        root,
        text="Report",
        font=("arial", 11),
        bg=color1,
        fg=colorf,
        command=create_report_pem,
    )
    report_button.place(
        relx=0.6505, rely=0.93, relheight=0.057, relwidth=0.105, anchor="n"
    )

    ### Pause Test
    pause_test_button = tk.Button(
        root, text="Pause Testing", font=("arial", 11), bg=color1, fg=colorf
    )
    pause_test_button.place(
        relx=0.7775, rely=0.93, relheight=0.057, relwidth=0.136, anchor="n"
    )

    ### Stop Test
    stop_test_button = tk.Button(
        root,
        text="Stop Testing",
        font=("arial", 11),
        bg=color1,
        fg=colorf,
        command=close,
    )
    stop_test_button.place(
        relx=0.9175, rely=0.93, relheight=0.057, relwidth=0.136, anchor="n"
    )

    # get sensor data
    sensor_data = repository.get_sensor_data()
    # Room Temperature
    room_temp_label = tk.Label(
        root, text="Room temperature ", bg=colorf, font=("Arial", 10), justify="left"
    )
    room_temp_label.place(relx=0.82, rely=0.03, relwidth=0.12, anchor="n")
    room_temp_border = tk.Frame(
        root, bg=colorf, bd=1, highlightbackground=color1, highlightthickness=1
    )
    room_temp_border.place(
        relx=0.915, rely=0.02, relheight=0.06, relwidth=0.08, anchor="n"
    )
    room_temp_value = tk.Label(root, bg=colorf, text=sensor_data["temperature"])
    room_temp_value.place(
        relx=0.915, rely=0.021, relheight=0.057, relwidth=0.078, anchor="n"
    )
    room_temp_unit = tk.Label(root, text="°C", bg=colorf, font=("Arial", 10))
    room_temp_unit.place(relx=0.975, rely=0.03, anchor="n")

    # Helium Supply Pressure
    helium_pressure_label = tk.Label(
        root,
        text="Helium supply       \nPressure",
        bg=colorf,
        font=("Arial", 10),
        justify="left",
    )
    helium_pressure_label.place(relx=0.82, rely=0.09, relwidth=0.12, anchor="n")
    helium_pressure_border = tk.Frame(
        root, bg=colorf, bd=1, highlightbackground=color1, highlightthickness=1
    )
    helium_pressure_border.place(
        relx=0.915, rely=0.09, relheight=0.06, relwidth=0.08, anchor="n"
    )
    helium_pressure_value = tk.Label(root, bg=colorf, text=sensor_data["pressure"])
    helium_pressure_value.place(
        relx=0.915, rely=0.091, relheight=0.057, relwidth=0.078, anchor="n"
    )
    helium_pressure_unit = tk.Label(root, text="Bar", bg=colorf, font=("Arial", 10))
    helium_pressure_unit.place(relx=0.975, rely=0.105, anchor="n")

    # Helium Concentration
    helium_concentration_label = tk.Label(
        root,
        text="Helium                 \nConcentration",
        bg=colorf,
        font=("Arial", 10),
        justify="left",
    )
    helium_concentration_label.place(relx=0.82, rely=0.16, relwidth=0.12, anchor="n")
    helium_concentration_border = tk.Frame(
        root, bg=colorf, bd=1, highlightbackground=color1, highlightthickness=1
    )
    helium_concentration_border.place(
        relx=0.915, rely=0.16, relheight=0.06, relwidth=0.08, anchor="n"
    )
    helium_concentration_value = tk.Label(root, bg=colorf, text=sensor_data["helium"])
    helium_concentration_value.place(
        relx=0.915, rely=0.161, relheight=0.057, relwidth=0.078, anchor="n"
    )
    helium_concentration_unit = tk.Label(root, text="%", bg=colorf, font=("Arial", 10))
    helium_concentration_unit.place(relx=0.975, rely=0.17, anchor="n")

    # Helium Mass Flow
    helium_massflow_label = tk.Label(
        root, text="Helium Mass Flow", bg=colorf, font=("Arial", 10), justify="left"
    )
    helium_massflow_label.place(relx=0.82, rely=0.24, relwidth=0.12, anchor="n")
    helium_massflow_border = tk.Frame(
        root, bg=colorf, bd=1, highlightbackground=color1, highlightthickness=1
    )
    helium_massflow_border.place(
        relx=0.915, rely=0.23, relheight=0.06, relwidth=0.08, anchor="n"
    )
    helium_massflow_value = tk.Label(root, bg=colorf, text=sensor_data["sccm_value"])
    helium_massflow_value.place(
        relx=0.915, rely=0.231, relheight=0.057, relwidth=0.078, anchor="n"
    )
    helium_massflow_unit = tk.Label(root, text="SCCM", bg=colorf, font=("Arial", 9))
    helium_massflow_unit.place(relx=0.975, rely=0.24, anchor="n")

    thread1 = threading.Thread(target=update_sensor_data)
    thread1.start()
    root.mainloop()
    thread1.join()


element_no = 0
measurement = 0
on_off = 0
auto_onoff = 0
start_time = 0
seconds_elapsed = 0
xs = []
ys = []
ys2 = []
row_elemno = []
row_time = []
row_measurement = []
row_highest = []
measure_val = 0
element_listx = []
element_listy = []
serialPort_leakDetector = None
settings_onoff = False
settings_onoff2 = False
toggle_value = 0
