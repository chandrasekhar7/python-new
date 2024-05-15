"""
create_pdf.py

This module provides functionality to generate PDF reports based on the collected leak test data.
It creates a PDF document using the FPDF library and includes various sections such as test
specifications,
measurement results, graphs, and notes.

Key Functions:
- create_pdf(leakware_id, repository, report_data, mode_of_measurement): Main function to generate
the PDF report.
- load_data_from_database_pdf(): Function to load measurement data from the database for the
PDF report.
- create_graphs(): Function to create graphs for the PDF report.
- image_title(title, height=cell_height): Function to add an image title section in the PDF.
- element_spec_design(): Function to set the design for the element specification section.
- results_design(): Function to set the design for the results section.
- decode_image(encoded_image): Function to decode a base64-encoded image.
- insert_image(pdf_canvas, image): Function to insert an image into the PDF.
- convert_he_to_air(he_leak_rate, average_temperature): Function to convert helium leak rate
to air leak rate.
- get_elem_direction_value(direction): Function to get the element direction value.

Dependencies:
- base64
- datetime
- json
- os
- datetime
- io
- matplotlib.pyplot
- PIL
- fpdf
- copy
- db_model

Usage:
This module is typically imported and the `create_pdf` function is called when the user requests
to generate a PDF report for a specific leak test session.
"""
import base64
import datetime
import json
import os
from datetime import datetime
from io import BytesIO

import copy
import matplotlib.pyplot as plt
from PIL import Image
from fpdf import FPDF
from db_model import Report

ETA_HE = 19.6  # Viscosity of helium (in μPa·s)
ETA_AIR = 18.19  # Viscosity of air (in μPa·s)
PA1 = 1.0  # Constant pressure (in bar)
PA2 = 0.0  # Constant pressure (in bar)
PB2 = 1.0  # Constant pressure (in bar)
T1 = 273.0  # Constant temperature (in K)


def create_pdf(leakware_id, repository, report_data: Report, mode_of_measurement):
    """
    Creates a PDF report based on the provided data.

    Args:
        leakware_id (str): The ID of the leakware.
        repository: The repository object for accessing data.
        report_data (Report): An object containing report data.
        mode_of_measurement (str): The mode of measurement, either "PEM" or "PROFIL".

    Returns:
        None

    This function generates a PDF report based on the provided data, including project details,
    measurement results, graphical representations, and notes. It saves the PDF file and opens
    it using the default application.
    """
    pdf = FPDF()
    pdf.add_page(orientation="L")
    pdf.add_font('DejaVuSans', '', './Fonts/DejaVuSans.ttf', uni=True)
    cell_height = 6

    if mode_of_measurement == "PEM":
        pdf.image("./Images/PEM.png", x=220, y=-13, w=120, h=70)
    else:
        pdf.image("./Images/PROFIL.png", x=200, y=-13, w=120, h=70)

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(270, 1, "Vacuum Leak Test Report", align="C")

    pdf.set_xy(10, 15)
    pdf.set_font('Arial', 'B', 13)
    pdf.cell(50, 10, "Leak Testing:")
    pdf.ln()
    specification = repository.get_specification(leakware_id, mode_of_measurement)

    def load_data_from_database_pdf():
        global element_listx
        global element_listy
        element_listx = []
        element_listy = []
        specimens = repository.get_all_specimens(leakware_id)

        for specimen in specimens:
            converted_leak_rates = []
            for y_value in json.loads(specimen.y_value):
                if report_data.rate_unit == "cm³/min":
                    y_value = y_value * 60
                if report_data.test_medium == "Air":
                    y_value = convert_he_to_air(y_value, measurement.average_temperature)
                converted_leak_rates.append(y_value)

            element_listy.append(converted_leak_rates)
            element_listx.append(json.loads(specimen.x_value))

    def create_graphs(graph_type):
        global ys
        global xs
        global element_listx
        global element_listy

        fig2 = plt.figure(figsize=(10, 4))
        ax_pdf = fig2.add_subplot(1, 1, 1)
        ax_pdf.clear()
        ax_pdf.grid()

        if graph_type == 0:
            ax_pdf.set_title('Course of the measurements')
            ax_pdf.set_yscale("symlog")
            ax_pdf.set_xlabel("Time [s]")
            ax_pdf.set_ylabel("Leakrate [mbarˑl/s]")

            i = 0
            for element_no_in_listy in element_listy:
                element_no_in_listx = element_listx[i]
                i += 1
                ax_pdf.plot(element_no_in_listx[:-1],
                            element_no_in_listy[:-1],
                            label="specimen " + str(i))
            fig2.legend()  # loc='upper right'
            return fig2

        elif graph_type == 1:
            ax_pdf.set_xlabel('Specimen/Location')
            ax_pdf.set_ylabel('Highest Leakrate [mbarˑl/s]')
            ax_pdf.set_title('Trend of Highest Leak rates')

            highest_values = []
            for element_no_in_listy in element_listy:
                highest_values.append(max(element_no_in_listy))

            x_values = list(range(1, len(highest_values) + 1))

            ax_pdf.plot(x_values, highest_values, marker='o', color='blue', label='specimen')
            plt.legend()

            return fig2

    def image_title(title, height=cell_height):
        pdf.set_draw_color(32, 73, 176)
        pdf.set_line_width(1)
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(32, 73, 176)
        pdf.cell(42, height, "")
        pdf.cell(76, height, title, 1, 0, 'L', True)

    def element_spec_design():
        pdf.set_line_width(0.1)
        pdf.set_font('Arial', '', 8)
        pdf.set_text_color(0, 0, 0)
        pdf.set_draw_color(0, 0, 0)

    def results_design():
        pdf.set_draw_color(0, 0, 0)
        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_font('Arial', 'B', 9)
        pdf.set_line_width(0.3)

    def decode_image(encoded_image):
        if encoded_image:
            image_data = base64.b64decode(encoded_image)
            img = Image.open(BytesIO(image_data))
            return img
        else:
            return None

    def insert_image(pdf_canvas, image):
        if image:
            temp_image_path = "./test_image.png"
            image.save(temp_image_path)

            pdf_canvas.image(temp_image_path, x=215, y=56, w=76, h=40)
            os.remove(temp_image_path)

    def convert_he_to_air(he_leak_rate, average_temperature):

        pb1 = float(report_data.pressure_difference) + 1

        delta_p = (pb1 ** 2 - PB2 ** 2) / (PA1 ** 2 - PA2 ** 2)
        air_leakrate = float(he_leak_rate) * (ETA_HE / ETA_AIR)

        if delta_p > 0:
            air_leakrate = air_leakrate * delta_p
        if report_data.rate_unit == "SCCM":
            air_leakrate_cm3_min = air_leakrate * 60
            air_leakrate = air_leakrate_cm3_min * ((average_temperature / T1) ** 0.5)

        return air_leakrate

    col_width = [32, 46, 32, 48]
    date = datetime.now()
    formatted_date = date.strftime("%d %b %Y")
    element_spec_design()

    if specification is None:
        if mode_of_measurement == "PEM":
            data = [['Project No:', '', 'Date:', formatted_date],
                    ['Inspector:', '', 'Fastener type:', ''],
                    ['Plating on Fastener:', '', 'Panel:', ''],
                    ['Plating on panel:', '', 'Panel thickness:', '' + ' mm'],
                    ['Hole Diameter:', '', 'Hole Preparation:', ''],
                    ['Panel Hardness:', '' + ' HRB', 'Install Machine Type:', ''],
                    ['Installation Direction:', '', 'Installation Force:', '' + ' kN'],
                    ['Test direction:', '', 'Test direction clinch:', '']]
        else:
            data = [["Project-No.: ", '', "Date: ", formatted_date],
                    ["Element: ", '', "Material: ", ''],
                    ["Thickness [mm]: ", '', "Die Button: ", ''],
                     ["Hole Preparation: ", '', "Mh-Maß: ", ''],
                     ["Coating: ", '', "Inspector: ", ''],
                     ["Hole Size: ", '', "Material Hardness: ", ''],
                     ["Installation Force: ", '', "Installation Tooling: ", ''],
                     ["Direction tested: ", '']]
    else:
        # Usage:
        if mode_of_measurement == "PEM":
            elem_direction_value = get_elem_direction_value(specification.test_direction)
            data = [['Project No:', specification.project_number, 'Date:', formatted_date],
                    ['Inspector:', specification.inspector, 'Fastener type:', specification.fastener_type],
                    ['Plating on Fastener:', specification.plating_on_fastener, 'Panel:', specification.panel],
                    ['Plating on panel:', specification.plating_on_panel, 'Panel thickness:', specification.panel_thickness +" "+ specification.panel_thickness_dia],
                    ['Hole Diameter:', specification.hole_diameter + " " + specification.hole_preparation_dia , 'Hole Preparation:', specification.hole_preparation],
                    ['Panel Hardness:', specification.panel_hardness + " " + specification.panel_hardness_type, 'Install Machine Type:', specification.install_machine_type],
                    ['Installation Direction:', specification.installation_direction, 'Installation Force:', specification.installation_force + ' kN'],
                    ['Test direction:', elem_direction_value, 'Test direction clinch:', specification.test_direction_clinch]]
        else:
            elem_direction_value = get_elem_direction_value(specification.direction_of_measurements)
            data = [["Project-No.: ", specification.project_number, "Date: ", formatted_date],
                    ["Element: ", specification.element, "Material: ", specification.material],
                    ["Thickness [mm]: ", specification.thickness, "Die Button: ", specification.die_button],
                    ["Hole Preparation: ", specification.hole_prepation, "Mh-Maß: ", specification.mh_mab],
                    ["Coating: ", specification.coating, "Inspector: ", specification.inspector],
                    ["Hole Size: ", specification.holesize, "Material Hardness: ", specification.material_hardness],
                    ["Installation Force: ", specification.installation_force, "Installation Tooling: ", specification.installation_tooling],
                    ["Direction tested: ", elem_direction_value]]

    pdf.set_fill_color(255, 255, 255)
    for index, row in enumerate(data):
        for i, item in enumerate(row):
            if i == 2:
                pdf.cell(5, 10, '', "")
            if i % 2 == 0:
                pdf.set_font('Arial', 'B', 8)
            else:
                pdf.set_font('Arial', '', 8)
            pdf.cell(col_width[i], cell_height, "  " + str(item), 1, 0, 'L', True)
        if index == 4:
            image_title("  Image of Test")
            element_spec_design()
            pdf.set_fill_color(255, 255, 255)
        pdf.ln()

    pdf.ln(5)
    pdf.set_fill_color(255, 255, 255)

    image = decode_image(report_data.image)
    insert_image(pdf, image)
    pressure_difference = str(report_data.pressure_difference \
    if report_data.pressure_difference else 0.0)

    pdf.set_font("DejaVuSans", size=11)
    pdf.cell(20, 8, "\u0394 of Air:", align='L', fill=True, ln=0, border="")
    pdf.set_draw_color(32, 73, 176)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(20, 8, pressure_difference, 1, 0, 'C', True)
    pdf.set_font('Arial', '', 11)
    pdf.cell(20, 8, " bar", ln=0, align='L', fill=True, border="L")

    pdf.set_draw_color(255, 255, 255)
    pdf.set_font('Arial', '', 10)
    pdf.cell(40, 8, "Results Presented in", 1, 0, 'L', True)
    pdf.set_draw_color(32, 73, 176)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(25, 8, report_data.test_medium, 1, 0, 'C', True)

    pdf.set_font('Arial', '', 9)
    pdf.set_line_width(0)
    pdf.multi_cell(20, 8, report_data.rate_unit, border="L", fill=True, align="C")
    pdf.ln(1)

    pdf.set_font('Arial', 'B', 13)
    pdf.cell(50, 10, "Results:")
    pdf.ln()

    headings = ["Panel No", "Location No", "Time (sec)", "Leak rate("+report_data.rate_unit+")",
                "Max Leak rate("+report_data.rate_unit+")"]
    measurements_list = copy.deepcopy(repository.get_all_measurements_data(leakware_id))

    flag = True
    for measurement in measurements_list:
        if report_data.rate_unit == "cm³/min":
            measurement.max_value = measurement.max_value * 60
            measurement.value_mbarl_second = measurement.value_mbarl_second * 60
            flag = False
        if report_data.test_medium == "Air":
            measurement.max_value = convert_he_to_air(measurement.max_value,
                                                      measurement.average_temperature)
            measurement.value_mbarl_second = convert_he_to_air(measurement.value_mbarl_second,
                                                               measurement.average_temperature)
            flag = False
        if flag:
            break

    col_width = [26, 26, 26, 42, 43]
    results_design()
    for index, heading in enumerate(headings):
        pdf.cell(col_width[index], 8, heading, 1, 0, 'C', True)

    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(0, 0, 0)

    df_list = []
    if measurements_list:  # Check if measurements_list is not empty
        for measurement in measurements_list:
            df_list.append(
                [measurement.panel_no, measurement.location_no,
                 round(measurement.time_in_seconds, 1),
                 f"{measurement.value_mbarl_second:10.1e}",
                 f"{float(measurement.max_value):10.1e}"])

    load_data_from_database_pdf()

    pdf.ln()
    results_design()
    graph_location = 135

    for index, row in enumerate(df_list):
        if pdf.get_y() > 185:
            for index, heading in enumerate(headings):
                pdf.cell(col_width[index], 8, heading, 1, 0, 'C', True)
            pdf.ln()
        for index, item in enumerate(row):
            pdf.cell(col_width[index], cell_height, str(item), 1, 0, 'C', True)

        if index == len(df_list) - 1:
            graph_location = pdf.get_y() + 10
        pdf.ln()

    if pdf.get_y() > 135:
        pdf.add_page(orientation="L")
        graph_location = 15

    pdf.cell(163, 40, "", border="")
    image_title("   Notes")
    pdf.ln()
    pdf.cell(205, 40, "", border="")
    pdf.set_font("DejaVuSans", size=10)
    pdf.set_fill_color(230, 239, 255)
    pdf.set_text_color(0, 0, 0)
    pdf.set_line_width(1)

    text = ""
    note_no = 1
    if specification is not None and specification.note != "":
        text = text + "Note 1: \n" + specification.note
        note_no = 2
    if report_data.note:
        text = text + f"\nNote {note_no}: \n" + report_data.note

    pdf.set_draw_color(32, 73, 176)
    pdf.multi_cell(76, 5, txt=text.strip(), fill=True, border="T")

    width = 270
    height = 85

    if report_data.graph_type != 2:
        create_graphs(report_data.graph_type).savefig("tmp.png")
        oimage = Image.open("tmp.png")
        rimage = oimage.rotate(0, expand=True)
        rimage.save("tmp.png")
        pdf.image("tmp.png", 1, graph_location, width - 70, height - 20)
    else:
        create_graphs(0).savefig("tmp.png")
        oimage = Image.open("tmp.png")
        rimage = oimage.rotate(0, expand=True)
        rimage.save("tmp.png")
        pdf.image("tmp.png", 1, graph_location, width - 70, height - 20)
        if pdf.get_y() > 105:
            pdf.add_page(orientation="L")
            graph_location = 15
        else:
            graph_location = graph_location + 70
        create_graphs(1).savefig("tmp1.png")
        oimage = Image.open("tmp1.png")
        rimage = oimage.rotate(0, expand=True)
        rimage.save("tmp1.png")
        pdf.image("tmp1.png", 1, graph_location, width - 70, height - 20)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdf_name = f"{current_time}_new_report.pdf"
    directory_path_data = ".\\Data\\"
    pdf_data_path = os.path.join(directory_path_data, pdf_name)
    pdf.output(pdf_data_path, "F")
    os.startfile(pdf_data_path)
    if report_data.graph_type in (0,2):
        os.remove("tmp.png")
    if report_data.graph_type in (1,2):
        file_path = "tmp1.png"
        if os.path.exists(file_path):
            os.remove(file_path)


def get_elem_direction_value(direction):
    """
    Retrieves the direction value description based on the provided direction code.

    Args:
        direction (str): The direction code.

    Returns:
        str: The description of the direction value.

    This function maps the provided direction code to its corresponding description.
    It returns a string describing the direction value, such as "Nut facing upwards" or
    "Bolt facing downwards".
    If the provided direction code does not match any known values, an empty string is returned.
    """
    if direction == "0":
        return "Nut facing upwards"
    elif direction == "1":
        return "Nut facing downwards"
    elif direction == "2":
        return "Capnut facing upwards"
    elif direction == "3":
        return "Capnut facing downwards"
    elif direction == "4":
        return "Bolt facing upwards"
    elif direction == "5":
        return "Bolt facing downwards"
    else:
        return ""
