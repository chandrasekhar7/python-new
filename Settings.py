"""
settings.py

This module likely contains the user interface and functionality related to the settings or configuration
options of the Leakware application. It handles the creation of the settings window, allowing users to
configure various aspects of the application, such as device settings, preferences, or other configurable
options.

Key Functions:
- settings(tk, root, leakDetector_available, is_mass_flow_controller_available, mode_of_measurement, repository):
  Function to create and configure the settings window.

Dependencies:
- tkinter (for creating the graphical user interface)
- Potentially other modules or libraries specific to handling application settings or configurations

Usage:
This module is typically imported and the `settings` function is called when the user requests to
access or modify the application settings. It sets up the necessary user interface components and
handles the retrieval, modification, and persistence of application settings or configurations.
"""
import logging
import time
import serial  # Module for serial port communication
import serial.tools.list_ports  # Helps list available serial ports
from db_model import MassFlowSensorData
from denkovi_relay import RelaySwitch

def settings(tk,
             settings,
             is_leak_detector_available,
             is_mass_flow_controller_available,
             mode_of_measurement,
             repository
             ):

    relay_switch = RelaySwitch(repository)
    relay_config = repository.get_device_info_by("Relay Switch")
    relay_connected, relay_states = relay_switch.connect(relay_config.port)#True,[True, False,True, False]
    if relay_connected:
        inficon_relay_switch = relay_states[0]
        helium_solenoid_realy_switch = relay_states[1]
        helium_realy_switch = relay_states[2]
        mass_flow_relay_switch = relay_states[3]
    on_image = tk.PhotoImage(file="./Images/on.png")
    off_image = tk.PhotoImage(file="./Images/off.png")

    def error_page(port, used_by, entered_in):
        def close_error_page():
            error_frame.place_forget()

        error_frame = tk.Frame(settings, bg=color3)
        error_frame.place(relx=0.25, rely=0.3, relwidth=0.5, relheight=0.4)
        message = port + " is in use for "+ used_by + ". \nPlease use a different port for " + entered_in
        error_text = tk.Label(error_frame, bg=color3, text=message, font=("Arial", 14), justify="left")
        error_text.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.6)
        error_close_btn = tk.Button(error_frame, bg=color1, text="Close", fg="white", command=close_error_page)
        error_close_btn.place(relx=0.7, rely=0.7, relwidth=0.2, relheight=0.2)
    if relay_connected:
        def toggle_inficon_button():
            global inficon_relay_switch
            if inficon_relay_switch:
                relay_switch.set_relay_state("Inficon", 0)
                inficon_button.configure(image=off_image)
                inficon_relay_switch = False
            else:
                relay_switch.set_relay_state("Inficon", 1)
                inficon_button.configure(image=on_image)
                inficon_relay_switch = True

        def toggle_mass_flow_button():
            global mass_flow_relay_switch
            if mass_flow_relay_switch:
                relay_switch.set_relay_state("Mass Flow Controller", 0)
                mass_flow_button.configure(image=off_image)
                mass_flow_relay_switch = False
            else:
                relay_switch.set_relay_state("Mass Flow Controller", 1)
                mass_flow_button.configure(image=on_image)
                mass_flow_relay_switch = True

        def toggle_helium_button():
            global helium_realy_switch
            if helium_realy_switch:
                relay_switch.set_relay_state("Helium Analyzer", 0)
                helium_button.configure(image=off_image)
                helium_realy_switch = False
            else:
                relay_switch.set_relay_state("Helium Analyzer", 1)
                helium_button.configure(image=on_image)
                helium_realy_switch = True

        def toggle_helium_solenoid_button():
            global helium_solenoid_realy_switch
            if helium_solenoid_realy_switch:
                relay_switch.set_relay_state("Helium Solenoid Valve", 0)
                helium_solenoid_button.configure(image=off_image)
                helium_solenoid_realy_switch = False
            else:
                relay_switch.set_relay_state("Helium Solenoid Valve", 1)
                helium_solenoid_button.configure(image=on_image)
                helium_solenoid_realy_switch = True

    leakware_config = repository.get_device_info_by("Leak Detector")
    logging.info("=================Entered into Leakware Config===========================")
    settings.title("Settings")
    if mode_of_measurement == "PEM":
        settings.iconbitmap("favicon.ico")
    settings.configure(background="white")
    settings.geometry("1250x400+50+50")

    color3 = "#e6efff"  # light color1
    color4 = "#2049b0"  # profilblau?
    color1 = color4
    colorf = "#ffffff"  # font #white

    textboxheight = 0.1

    headline = tk.Label(settings, text="Inficon", font=("arial", 15, "bold"), bg="white")
    headline.place(relx=0.02, rely=0.001, relheight=0.1, relwidth=0.185, anchor="nw")
    settings_popup = tk.Frame(settings, bg="white")
    settings_popup.place(relx=0.001, rely=0.1234, relheight=0.7, relwidth=0.25, anchor="nw")
    label_port = tk.Label(settings_popup, text="Port:", font=("arial", 13), bg="white", anchor="w")
    label_port.place(relx=0.05, rely=0.001, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_port = tk.Text(settings_popup, font=("arial", 13), bg="white")
    tb_port.place(relx=0.4, rely=0.001, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_baudrate = tk.Label(settings_popup, text="Baudrate:", font=("arial", 13), bg="white", anchor="w")
    label_baudrate.place(relx=0.05, rely=0.1234, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_baudrate = tk.Text(settings_popup, font=("arial", 13), bg="white")
    tb_baudrate.place(relx=0.4, rely=0.1234, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_bytesize = tk.Label(settings_popup, text="Bytesize:", font=("arial", 13), bg="white", anchor="w")
    label_bytesize.place(relx=0.05, rely=0.248, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_bytesize = tk.Text(settings_popup, font=("arial", 13), bg="white")
    tb_bytesize.place(relx=0.4, rely=0.248, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_parity = tk.Label(settings_popup, text="Parity:", font=("arial", 13), bg="white", anchor="w")
    label_parity.place(relx=0.05, rely=0.371, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_parity = tk.Text(settings_popup, font=("arial", 13), bg="white")
    tb_parity.place(relx=0.4, rely=0.371, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_stopbits = tk.Label(settings_popup, text="Stopbits:", font=("arial", 13), bg="white", anchor="w")
    label_stopbits.place(relx=0.05, rely=0.495, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_stopbits = tk.Text(settings_popup, font=("arial", 13), bg="white")
    tb_stopbits.place(relx=0.4, rely=0.495, relheight=textboxheight, relwidth=0.49, anchor="nw")

    if relay_connected:
        inficon_button_frame = tk.Frame(settings_popup, bg="black", border=0)
        inficon_button_frame.place(relx=.58, rely=.8, relheight=0.17, relwidth=0.33, anchor="nw")
        inficon_button = tk.Button(inficon_button_frame, image=on_image, bg="white", bd=0, command=toggle_inficon_button)
        inficon_button.pack(fill="both", expand=True)

    def focus_next_widget(event):
        event.widget.tk_focusNext().focus()
        return "break"

    tb_port.bind("<Tab>", focus_next_widget)
    tb_baudrate.bind("<Tab>", focus_next_widget)
    tb_bytesize.bind("<Tab>", focus_next_widget)
    tb_parity.bind("<Tab>", focus_next_widget)
    tb_stopbits.bind("<Tab>", focus_next_widget)

    tb_port.insert(1.0, str(leakware_config.port))
    tb_baudrate.insert(1.0, str(leakware_config.baudrate))
    tb_bytesize.insert(1.0, str(leakware_config.bytesize))
    tb_parity.insert(1.0, str(leakware_config.parity))
    tb_stopbits.insert(1.0, str(leakware_config.stopbits))

    def save_settings_leak_detector():
        global settingsdict_leakDetector

        port_leak_detector = str(tb_port.get(1.0, "end-1c")).strip()
        leakware_config.port = port_leak_detector  # Assigning the default port for other cases
        leakware_config.baudrate = int(tb_baudrate.get(1.0, "end-1c"))
        leakware_config.bytesize = int(tb_bytesize.get(1.0, "end-1c"))
        leakware_config.parity = str(tb_parity.get(1.0, "end-1c"))
        leakware_config.stopbits = int(tb_stopbits.get(1.0, "end-1c"))
        settingsdict_leakDetector = {'baudrate': leakware_config.baudrate, 'bytesize': int(leakware_config.bytesize), 'parity': leakware_config.parity,
                        'stopbits': int(leakware_config.stopbits), 'xonxoff': False, 'dsrdtr': False, 'rtscts': False, 'timeout': 1,
                        'write_timeout': None, 'inter_byte_timeout': None}
        try:
            serial_port_leak_detector = serial.Serial(port=str(leakware_config.port))
            serial_port_leak_detector.apply_settings(settingsdict_leakDetector)
            serial_port_leak_detector.write("*CLS\r".encode())
            logging.info("Settings changed for Inficon")
            print("Settings changed.")
            print(serial_port_leak_detector.get_settings())
            print("Port open: " + str(serial_port_leak_detector.isOpen()))
            repository.update_device_info()
        except:
            logging.info("No Leak Detector Found.")
            print("No Leak Detector found.")

    # Mass_Flow_Controller
    mass_flow_config = repository.get_device_info_by("Mass Flow Controller")
    logging.info("====================================Entered into Mass flow Controller=======================")
    headline2 = tk.Label(settings, text="Mass Flow Controller", font=("arial", 15, "bold"), bg="white")
    headline2.place(relx=0.20, rely=0.001, relheight=0.1, relwidth=0.33, anchor="nw")
    border_frame = tk.Frame(settings, bg="black")
    border_frame.place(relx=0.24, rely=0.0052, relheight=0.8, relwidth=0, anchor="nw")
    massflow_frame = tk.Frame(settings, bg="white")
    massflow_frame.place(relx=0.25, rely=0.1234, relheight=0.7, relwidth=.25, anchor="nw")
    label_port2 = tk.Label(massflow_frame, text="Port:", font=("arial", 13), bg="white", anchor="w")
    label_port2.place(relx=0.04, rely=0.001, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_port2 = tk.Text(massflow_frame, font=("arial", 13), bg="white")
    tb_port2.place(relx=0.4, rely=0.001, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_baudrate2 = tk.Label(massflow_frame, text="Baudrate:", font=("arial", 13), bg="white", anchor="w")
    label_baudrate2.place(relx=0.04, rely=0.1234, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_baudrate2 = tk.Text(massflow_frame, font=("arial", 13), bg="white")
    tb_baudrate2.place(relx=0.4, rely=0.1234, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_bytesize2 = tk.Label(massflow_frame, text="Bytesize:", font=("arial", 13), bg="white", anchor="w")
    label_bytesize2.place(relx=0.04, rely=0.248, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_bytesize2 = tk.Text(massflow_frame, font=("arial", 13), bg="white")
    tb_bytesize2.place(relx=0.4, rely=0.248, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_parity2 = tk.Label(massflow_frame, text="Parity:", font=("arial", 13), bg="white", anchor="w")
    label_parity2.place(relx=0.04, rely=0.371, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_parity2 = tk.Text(massflow_frame, font=("arial", 13), bg="white")
    tb_parity2.place(relx=0.4, rely=0.371, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_stopbits2 = tk.Label(massflow_frame, text="Stopbits:", font=("arial", 13), bg="white", anchor="w")
    label_stopbits2.place(relx=0.04, rely=0.495, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_stopbits2 = tk.Text(massflow_frame, font=("arial", 13), bg="white")
    tb_stopbits2.place(relx=0.4, rely=0.495, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_sccm = tk.Label(massflow_frame, text="SCCM He:", font=("arial", 13, "bold"), bg="white", anchor="w")
    label_sccm.place(relx=0.04, rely=0.62, relheight=textboxheight, relwidth=0.45, anchor="nw")
    tb_sccm = tk.Text(massflow_frame, font=("arial", 13, "bold"), bg="white")
    tb_sccm.place(relx=0.4, rely=0.62, relheight=textboxheight, relwidth=0.49, anchor="nw")

    if relay_connected:
        mass_flow_button_frame = tk.Frame(massflow_frame, bg="black", border=0)
        mass_flow_button_frame.place(relx=.58, rely=.8, relheight=0.17, relwidth=0.33, anchor="nw")
        mass_flow_button = tk.Button(mass_flow_button_frame, image=on_image, bg="white", bd=0, command=toggle_mass_flow_button)
        mass_flow_button.pack(fill="both", expand=True)

    def focus_next_widget(event):
        event.widget.tk_focusNext().focus()
        return "break"

    tb_port2.bind("<Tab>", focus_next_widget)
    tb_baudrate2.bind("<Tab>", focus_next_widget)
    tb_bytesize2.bind("<Tab>", focus_next_widget)
    tb_parity2.bind("<Tab>", focus_next_widget)
    tb_stopbits2.bind("<Tab>", focus_next_widget)
    tb_sccm.bind("<Tab>", focus_next_widget)

    tb_port2.insert(1.0, str(mass_flow_config.port))
    tb_baudrate2.insert(1.0, str(mass_flow_config.baudrate))
    tb_bytesize2.insert(1.0, str(mass_flow_config.bytesize))
    tb_parity2.insert(1.0, str(mass_flow_config.parity))
    tb_stopbits2.insert(1.0, str(mass_flow_config.stopbits))
    tb_sccm.insert(1.0, str(mass_flow_config.sccm_value))

    def save_settings_mass_flow_controller():
        global serialPort_massFlowController
        global is_mass_flow_controller_available
        global settingsdict_massFlowController

        try:
            serialPort_massFlowController.close()
        except:
            logging.info("No serial port for Massflow Controller")
            print("no serialPort_massFlowController")

        port_mass_flow = str(tb_port2.get(1.0, "end-1c")).strip()
        mass_flow_config.port = port_mass_flow  # Assigning the default port for other cases
        mass_flow_config.baudrate = int(tb_baudrate2.get(1.0, "end-1c"))
        mass_flow_config.bytesize = int(tb_bytesize2.get(1.0, "end-1c"))
        mass_flow_config.parity = str(tb_parity2.get(1.0, "end-1c"))
        mass_flow_config.stopbits = int(tb_stopbits2.get(1.0, "end-1c"))
        mass_flow_config.sccm_value = float(tb_sccm.get(1.0, "end-1c"))
        settingsdict_massFlowController = {'baudrate': mass_flow_config.baudrate, 'bytesize': int(mass_flow_config.bytesize), 'parity': mass_flow_config.parity,
                           'stopbits': int(mass_flow_config.stopbits), 'xonxoff': False, 'dsrdtr': False, 'rtscts': False,
                           'timeout': 1, 'write_timeout': None, 'inter_byte_timeout': None}

        try:
            serialPort_massFlowController = serial.Serial(port=str(mass_flow_config.port))
            serialPort_massFlowController.apply_settings(settingsdict_massFlowController)
            print("Settings changed for Mass_Flow_Controller.")
            logging.info("Setting Changed for Mass flow Controller - in Settings")
            print(serialPort_massFlowController.get_settings())
            print("Port open: " + str(serialPort_massFlowController.isOpen()))
            flowrate = str(mass_flow_config.sccm_value * 64000 / 500)
            print(flowrate)
            logging.info("Flowrate for massflow: %s", flowrate)
            serialPort_massFlowController.flushInput()
            serialPort_massFlowController.write("*@=A\r".encode())
            time.sleep(0.2)
            serialPort_massFlowController.flushInput()
            serialPort_massFlowController.write(("*" + flowrate + "\r").encode())
            serialPort_massFlowController.flushOutput()
            repository.update_device_info()

            for i in range(0, 2):
                i += 1
                serialPort_massFlowController.flushInput()
                serialPort_massFlowController.write("*@=A\r".encode())
                serialPort_massFlowController.flushInput()
                value_sens = serialPort_massFlowController.read_until('\r').decode()
                value_sens_list = value_sens.split(" ")
            print(value_sens)

            psi_v = value_sens_list[1]
            temp_v = value_sens_list[2]
            ccm_v = value_sens_list[3]
            sccm_val = value_sens_list[4]

            mass_flow_sensor_data = MassFlowSensorData(
                device_id = mass_flow_config.device_id,
                psi_v = psi_v,
                temp_v = temp_v,
                ccm_v = ccm_v,
                sccm_val = sccm_val
            )
            # create_mass_flow_sensor_data
            repository.create_mass_flow_sensor_data(mass_flow_sensor_data)

            sensor_data = tk.Toplevel(settings)
            sensor_data.title("Sensor Data")
            sensor_data.configure(background="white")
            sensor_data.geometry("400x200")
            textboxheight2 = 0.15
            lb_psi = tk.Label(sensor_data, text="PSIA:", font=("arial", 13), bg="white")
            lb_psi.place(relx=0.005, rely=0.001, relheight=textboxheight2, relwidth=0.6, anchor="nw")
            lb_psi_value = tk.Label(sensor_data, text=psi_v, font=("arial", 13), bg="white")
            lb_psi_value.place(relx=0.6, rely=0.001, relheight=textboxheight2, relwidth=0.4, anchor="nw")
            lb_temp = tk.Label(sensor_data, text="Temperature [°C]:", font=("arial", 13), bg="white")
            lb_temp.place(relx=0.005, rely=0.25, relheight=textboxheight2, relwidth=0.6, anchor="nw")
            lb_temp_value = tk.Label(sensor_data, text=temp_v, font=("arial", 13), bg="white")
            lb_temp_value.place(relx=0.6, rely=0.25, relheight=textboxheight2, relwidth=0.4, anchor="nw")
            lb_ccm = tk.Label(sensor_data, text="CCM:", font=("arial", 13), bg="white")
            lb_ccm.place(relx=0.005, rely=0.5, relheight=textboxheight2, relwidth=0.6, anchor="nw")
            lb_ccm_value = tk.Label(sensor_data, text=ccm_v, font=("arial", 13), bg="white")
            lb_ccm_value.place(relx=0.6, rely=0.5, relheight=textboxheight2, relwidth=0.4, anchor="nw")
            lb_sccm = tk.Label(sensor_data, text="SCCM:", font=("arial", 13), bg="white")
            lb_sccm.place(relx=0.005, rely=0.75, relheight=textboxheight2, relwidth=0.6, anchor="nw")
            lb_sccm_value = tk.Label(sensor_data, text=sccm_val, font=("arial", 13), bg="white")
            lb_sccm_value.place(relx=0.6, rely=0.75, relheight=textboxheight2, relwidth=0.4, anchor="nw")

        except:
            logging.info("No Mass flow Controller Found.")
            print("No Mass Flow Controller found.")

        ###         Helium Analyzer            ###
    helium_analyzer_config = repository.get_device_info_by("Helium Analyzer")
    logging.info("====================Entered into Helium Analyzer=======================")
    headline3 = tk.Label(settings, text="Helium Analyzer", font=("arial", 15, "bold"), bg="white")
    headline3.place(relx=0.45, rely=0.001, relheight=0.1, relwidth=0.32, anchor="nw")
    border_frame = tk.Frame(settings, bg="black")
    border_frame.place(relx=0.49, rely=0.0052, relheight=0.8, relwidth=0.001, anchor="nw")
    helium_frame = tk.Frame(settings, bg="white")
    helium_frame.place(relx=0.50, rely=0.1234, relheight=0.7, relwidth=.25, anchor="nw")
    label_port3 = tk.Label(helium_frame, text="Port:", font=("arial", 13), bg="white", anchor="w")
    label_port3.place(relx=0.04, rely=0.001, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_port3 = tk.Text(helium_frame, font=("arial", 13), bg="white")
    tb_port3.place(relx=0.4, rely=0.001, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_baudrate3 = tk.Label(helium_frame, text="Baudrate:", font=("arial", 13), bg="white", anchor="w")
    label_baudrate3.place(relx=0.04, rely=0.1234, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_baudrate3 = tk.Text(helium_frame, font=("arial", 13), bg="white")
    tb_baudrate3.place(relx=0.4, rely=0.1234, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_bytesize3 = tk.Label(helium_frame, text="Bytesize:", font=("arial", 13), bg="white", anchor="w")
    label_bytesize3.place(relx=0.04, rely=0.248, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_bytesize3 = tk.Text(helium_frame, font=("arial", 13), bg="white")
    tb_bytesize3.place(relx=0.4, rely=0.248, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_parity3 = tk.Label(helium_frame, text="Parity:", font=("arial", 13), bg="white", anchor="w")
    label_parity3.place(relx=0.04, rely=0.37, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_parity3 = tk.Text(helium_frame, font=("arial", 13), bg="white")
    tb_parity3.place(relx=0.4, rely=0.37, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_stopbits3 = tk.Label(helium_frame, text="Stopbits:", font=("arial", 13), bg="white", anchor="w")
    label_stopbits3.place(relx=0.04, rely=0.495, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_stopbits3 = tk.Text(helium_frame, font=("arial", 13), bg="white")
    tb_stopbits3.place(relx=0.4, rely=0.495, relheight=textboxheight, relwidth=0.49, anchor="nw")

    if relay_connected:
        helium_button_frame = tk.Frame(helium_frame, bg="black", border=0)
        helium_button_frame.place(relx=.58, rely=.8, relheight=0.17, relwidth=0.33, anchor="nw")
        helium_button = tk.Button(helium_button_frame, image=on_image, bg="white", bd=0, command=toggle_helium_button)
        helium_button.pack(fill="both", expand=True)

    def focus_next_widget(event):
        event.widget.tk_focusNext().focus()
        return "break"

    tb_port3.bind("<Tab>", focus_next_widget)
    tb_baudrate3.bind("<Tab>", focus_next_widget)
    tb_bytesize3.bind("<Tab>", focus_next_widget)
    tb_parity3.bind("<Tab>", focus_next_widget)
    tb_stopbits3.bind("<Tab>", focus_next_widget)

    tb_port3.insert(1.0, str(helium_analyzer_config.port))
    tb_baudrate3.insert(1.0, str(helium_analyzer_config.baudrate))
    tb_bytesize3.insert(1.0, str(helium_analyzer_config.bytesize))
    tb_parity3.insert(1.0, str(helium_analyzer_config.parity))
    tb_stopbits3.insert(1.0, str(helium_analyzer_config.stopbits))

    def save_settings_helium_analyzer():
        global serial_port_helium_analyzer
        global is_mass_flow_controller_available
        global settingsdict_massFlowController

        try:
            serialPort_massFlowController.close()
        except:
            logging.info("No Helium Analyzer")
            print("no Helium Analyzer")

        port_helium = str(tb_port3.get(1.0, "end-1c")).strip()
        helium_analyzer_config.port = port_helium  # Assigning the default port for other cases
        helium_analyzer_config.baudrate = int(tb_baudrate3.get(1.0, "end-1c"))
        helium_analyzer_config.bytesize = int(tb_bytesize3.get(1.0, "end-1c"))
        helium_analyzer_config.parity = str(tb_parity3.get(1.0, "end-1c"))
        helium_analyzer_config.stopbits = int(tb_stopbits3.get(1.0, "end-1c"))
        settingsdict_helium_analyzer = {'baudrate': helium_analyzer_config.baudrate, 'bytesize': int(helium_analyzer_config.bytesize), 'parity': helium_analyzer_config.parity,
                           'stopbits': int(helium_analyzer_config.stopbits), 'timeout': 1}

        try:
            helium_analyzer = serial.Serial(port=helium_analyzer_config.port, baudrate=helium_analyzer_config.baudrate, bytesize=helium_analyzer_config.bytesize,
                                            parity=helium_analyzer_config.parity, stopbits=helium_analyzer_config.stopbits, timeout=1)
            response = helium_analyzer.readline().decode('utf-8').strip()
            if "He" in response and "O2" in response:
                helium_analyzer.close()
                repository.update_device_info()
        except:
            logging.info("No Helium Analyzer Found")
            print("No Helium Analyzer found.")

    ###         Relay Switch            ###
    realy_config = repository.get_device_info_by("Relay Switch")
    relay_headline = tk.Label(settings, text="Relay", font=("arial", 15, "bold"), bg="white")
    relay_headline.place(relx=0.72, rely=0.001, relheight=0.1, relwidth=0.32, anchor="nw")
    border_frame = tk.Frame(settings, bg="black")
    border_frame.place(relx=0.74, rely=0.0052, relheight=0.8, relwidth=0.001, anchor="nw")
    relay_frame = tk.Frame(settings, bg="white")
    relay_frame.place(relx=0.75, rely=0.1234, relheight=0.7, relwidth=.25, anchor="nw")
    label_port_relay = tk.Label(relay_frame, text="Port:", font=("arial", 13), bg="white", anchor="w")
    label_port_relay.place(relx=0.04, rely=0.001, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_port_relay = tk.Text(relay_frame, font=("arial", 13), bg="white")
    tb_port_relay.place(relx=0.4, rely=0.001, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_baudrate_relay = tk.Label(relay_frame, text="Baudrate:", font=("arial", 13), bg="white", anchor="w")
    label_baudrate_relay.place(relx=0.04, rely=0.1234, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_baudrate_relay = tk.Text(relay_frame, font=("arial", 13), bg="white")
    tb_baudrate_relay.place(relx=0.4, rely=0.1234, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_bytesize_relay = tk.Label(relay_frame, text="Bytesize:", font=("arial", 13), bg="white", anchor="w")
    label_bytesize_relay.place(relx=0.04, rely=0.248, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_bytesize_relay = tk.Text(relay_frame, font=("arial", 13), bg="white")
    tb_bytesize_relay.place(relx=0.4, rely=0.248, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_parity_relay = tk.Label(relay_frame, text="Parity:", font=("arial", 13), bg="white", anchor="w")
    label_parity_relay.place(relx=0.04, rely=0.371, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_parity_relay = tk.Text(relay_frame, font=("arial", 13), bg="white")
    tb_parity_relay.place(relx=0.4, rely=0.371, relheight=textboxheight, relwidth=0.49, anchor="nw")
    label_stopbits_relay = tk.Label(relay_frame, text="Stopbits:", font=("arial", 13), bg="white", anchor="w")
    label_stopbits_relay.place(relx=0.04, rely=0.495, relheight=textboxheight, relwidth=0.4, anchor="nw")
    tb_stopbits_relay = tk.Text(relay_frame, font=("arial", 13), bg="white")
    tb_stopbits_relay.place(relx=0.4, rely=0.495, relheight=textboxheight, relwidth=0.49, anchor="nw")

    # Helium soilenoid button
    if relay_connected:
        helium_solenoid_label = tk.Label(relay_frame, text="Helium Solenoid \nSwitch",
                                         font=("arial", 13, "bold"), bg="white", anchor="w")
        helium_solenoid_label.place(relx=.1, rely=0.8, relwidth=0.7, relheight=0.2, anchor="nw")
        helium_solenoid_button_frame = tk.Frame(relay_frame,  bg="black", border=0)
        helium_solenoid_button_frame.place(relx=.58, rely=.8, relheight=0.17, relwidth=0.33,
                                           anchor="nw")
        helium_solenoid_button = tk.Button(helium_solenoid_button_frame, image=on_image,
                                           bg="white", bd=0, command=toggle_helium_solenoid_button)
        helium_solenoid_button.pack(fill="both", expand=True)

    def focus_next_widget(event):
        event.widget.tk_focusNext().focus()
        return "break"

    tb_port_relay.bind("<Tab>", focus_next_widget)
    tb_baudrate_relay.bind("<Tab>", focus_next_widget)
    tb_bytesize_relay.bind("<Tab>", focus_next_widget)
    tb_parity_relay.bind("<Tab>", focus_next_widget)
    tb_stopbits_relay.bind("<Tab>", focus_next_widget)

    tb_port_relay.insert(1.0, str(realy_config.port))
    tb_baudrate_relay.insert(1.0, str(realy_config.baudrate))
    tb_bytesize_relay.insert(1.0, str(realy_config.bytesize))
    tb_parity_relay.insert(1.0, str(realy_config.parity))
    tb_stopbits_relay.insert(1.0, str(realy_config.stopbits))

    def save_settings_relay_switch():
        realy_config.port = str(tb_port_relay.get(1.0, "end-1c")).strip()
        # Assigning the default port for other cases
        realy_config.baudrate = int(tb_baudrate.get(1.0, "end-1c"))
        realy_config.bytesize = int(tb_bytesize.get(1.0, "end-1c"))
        realy_config.parity = str(tb_parity.get(1.0, "end-1c"))
        realy_config.stopbits = int(tb_stopbits.get(1.0, "end-1c"))

        try:
            relay = serial.Serial(str(realy_config.port), realy_config.baudrate)
            relay.write(b'\x5B\x01\x5D')  # Command: [01]
            time.sleep(0.1)
            logging.info("Settings changed for Relay")
            print("Settings changed.")
            repository.update_device_info()
        except:
            logging.info("No Relay Switch Found.")
            print("No Relay Switch found.")

    def save_all_settings():
        leakware_port = str(tb_port.get(1.0, "end-1c")).strip()
        if leakware_port == mass_flow_config.port:
            error_page(leakware_port, mass_flow_config.name, leakware_config.name)
            return
        elif leakware_port == helium_analyzer_config.port:
            error_page(leakware_port, helium_analyzer_config.name, leakware_config.name)
            return

        mass_flow_port = str(tb_port2.get(1.0, "end-1c")).strip()
        if mass_flow_port == leakware_config.port:
            error_page(mass_flow_port, leakware_config.name, mass_flow_config.name)
            return
        elif mass_flow_port == helium_analyzer_config.port:
            error_page(mass_flow_port, helium_analyzer_config.name, mass_flow_config.name)
            return

        helium_analyzer_port = str(tb_port3.get(1.0, "end-1c")).strip()
        if helium_analyzer_port == leakware_config.port:
            error_page(helium_analyzer_port, leakware_config.name, helium_analyzer_config.name)
            return
        elif helium_analyzer_port == mass_flow_config.port:
            error_page(helium_analyzer_port, mass_flow_config.name, realy_config.name)
            return

        relay_switch_port = str(tb_port_relay.get(1.0, "end-1c")).strip()
        if relay_switch_port == leakware_config.port:
            error_page(relay_switch_port, leakware_config.name, helium_analyzer_config.name)
            return
        elif relay_switch_port == mass_flow_config.port:
            error_page(relay_switch_port, mass_flow_config.name, helium_analyzer_config.name)
            return

        save_settings_leak_detector()
        save_settings_mass_flow_controller()
        save_settings_helium_analyzer()
        save_settings_relay_switch()
    button_save_all = tk.Button(settings, text="Save all", font=("arial", 10),
                                bg=color1, fg=colorf, command=save_all_settings)
    button_save_all.place(relx=.5, rely=0.88, relheight=0.1, relwidth=0.18, anchor="n")

    settings.mainloop()
