"""
Module for creating a report interface.

This module provides functionality for creating a graphical user interface (GUI)
for generating reports.

Dependencies:
    - base64
    - tkinter.filedialog
    - create_pdf.create_pdf
    - db_model.Report

Constants:
    - COLOR1: Color code for the primary color.
    - COLOR_BLACK: Color code for black.
    - COLOR_WHITE: Color code for white.
    - default_font: Default font style.

Functions:
    - create_report: Function to create the report interface.

Usage:
    To use this module, import it and call the create_report function with the necessary parameters.
"""
import base64
from tkinter import filedialog

from create_pdf import create_pdf
from db_model import Report

COLOR1 = "#2049b0"
COLOR_BLACK = "black"
COLOR_WHITE = "white"
default_font = ("Arial", 10)
filename=""


def create_report(tk, report_root, repository, leakware_id, mode_of_measurement):
    """
    Create a report interface.

    Args:
        tk: The Tkinter module.
        report_root: The root window for the report interface.
        repository: The repository object.
        leakware_id: The ID of the leakware.
        mode_of_measurement: The mode of measurement (e.g., "PEM").

    Returns:
        None
    """
    def upload_image():
        global filename
        filename = filedialog.askopenfilename(parent=report_root, initialdir="/",
                                              title="Select Image",
                                              filetypes=(
                                              ("Image Files", "*.png *.jpg *.jpeg *.gif"),
                                              ("All Files", "*.*")))

        display_text = "Image \nuploaded" if filename else "No image \nselected"
        image_status.configure(text=display_text)
        image_status.place_forget()
        image_status.place(relx=0.85, rely=0.08, relheight=0.1, relwidth=0.3, anchor="n")
        if rb_choose_medium.get() == 1:
            image_status.place(relx=0.9, rely=0.025, relheight=0.1, relwidth=0.15, anchor="n")

    def create():
        global filename
        medium = "He" if rb_choose_medium.get() == 0 else "Air"
        notes = txt_note.get("1.0", "end-1c")
        pressure_difference = pressure_diff.get(1.0, "end-1c")
        graph_type = rb_choose_graph.get()
        if not pressure_difference:
            pressure_difference=0
        unit = rate_unit.get()

        if filename:
            with open(filename, "rb") as image_file:
                image_data = image_file.read()
            encoded_image = base64.b64encode(image_data).decode('utf-8')
        else:
            encoded_image = ""
        report_data = Report(
            leakware_id=leakware_id,
            test_medium=medium,
            note=notes,
            image=encoded_image,
            pressure_difference=pressure_difference,
            rate_unit=unit,
            graph_type=int(graph_type)
        )

        report_data = repository.save_report_data(report_data)
        create_pdf(leakware_id, repository, report_data, mode_of_measurement)
        report_root.after(0, lambda: report_root.destroy())

    def upload_image_layout():
        global options_rate_unit

        image_status.place_forget()
        if rb_choose_medium.get() == 0:
            options_rate_unit = ["Mbar*L/s", "cm³/min"]
            dropdown_rate_unit = tk.OptionMenu(report_root, rate_unit, *options_rate_unit)
            dropdown_rate_unit.place(relx=0.65, rely=0.25, relheight=0.075, relwidth=0.2)
            pressure_diff.place_forget()
            pressure_diff_label.place_forget()
            pressure_diff_unit.place_forget()
            upload_image_label.place(relx=0.5, rely=0, relheight=0.15, relwidth=0.385, anchor="n")
            upload_frame.place(relx=0.5, rely=0.13, relheight=0.05, relwidth=0.15)
            upload_button.pack(fill="both", expand=True)
            rate_unit.set(options_rate_unit[0])

        elif rb_choose_medium.get() == 1:
            options_rate_unit = ["cm³/min", "SCCM"]
            dropdown_rate_unit = tk.OptionMenu(report_root, rate_unit, *options_rate_unit)
            dropdown_rate_unit.place(relx=0.65, rely=0.25, relheight=0.075, relwidth=0.2)
            upload_frame.place(relx=0.65, rely=0.05, relheight=0.05, relwidth=0.15)
            upload_button.pack(fill="both", expand=True)
            pressure_diff_label.place(relx=0.5, rely=0.15, relheight=0.05,
                                      relwidth=0.385, anchor="n")
            pressure_diff.place(relx=0.65, rely=0.15, relheight=0.06, relwidth=0.25)
            pressure_diff_unit.place(relx=0.955, rely=0.15, anchor="n")
            rate_unit.set(options_rate_unit[0])

    report_root.title("Report Specifications")
    if mode_of_measurement == "PEM":
        report_root.iconbitmap("favicon.ico")
    report_root.configure(bg="white")
    report_root.geometry("500x400")

    rb_choose_medium = tk.IntVar()
    rb_choose_medium.set(0)
    filename = ""
    rb_choose_graph = tk.IntVar()
    rb_choose_graph.set(0)

    # Choose Medium Radio Buttons
    lbl_rb_data_dir = tk.Label(report_root, text="Choose Medium: ", font=default_font,
                               bg=COLOR_WHITE, fg=COLOR1, bd=1)
    lbl_rb_data_dir.place(relx=0.16, rely=0, relheight=0.15, relwidth=0.385, anchor="n")
    tk.Radiobutton(report_root, text="   Helium", fg=COLOR_BLACK, bg=COLOR_WHITE,
                   command=upload_image_layout, variable=rb_choose_medium,
                   value=0, font=default_font
                   ).place(relx=0.15, rely=0.125)
    tk.Radiobutton(report_root, text="   Air", fg=COLOR_BLACK, bg=COLOR_WHITE,
                   command=upload_image_layout,
                   variable=rb_choose_medium, value=1, font=default_font).place(relx=0.15, rely=0.2)

    # Upload image button
    upload_image_label = tk.Label(report_root, text="Upload Test Image:", font=default_font,
                                  bg=COLOR_WHITE, fg=COLOR1, bd=1)
    upload_frame = tk.Frame(report_root, bd=1, relief="solid")
    upload_button = tk.Button(upload_frame, text="Upload", command=upload_image,
                              fg=COLOR_BLACK, bg=COLOR_WHITE,
                              font=default_font, border=0.5)
    image_status = tk.Label(report_root, font=default_font, bg=COLOR_WHITE, fg=COLOR1, bd=1)

    # Pressure Difference
    pressure_diff_label = tk.Label(report_root, text="Pressure Difference:", font=default_font,
                                  bg=COLOR_WHITE, fg=COLOR1, bd=1)
    pressure_diff = tk.Text(report_root, font=default_font)
    pressure_diff_unit = tk.Label(report_root, text="Bar", bg="white", font=("Arial", 10))

    # Results presented(Unit of Leakrate)
    rate_unit_label = tk.Label(report_root, text="Unit of Leakrate:", font=default_font,
                               bg=COLOR_WHITE, fg=COLOR1, bd=1)
    rate_unit = tk.StringVar()
    rate_unit_label.place(relx=0.475, rely=0.25, relheight=0.05, relwidth=0.385, anchor="n")

    upload_image_layout()

    # Choose Graphs
    choose_graph_label = tk.Label(report_root, text="Choose Graph Type:", font=default_font,
                                  bg=COLOR_WHITE, fg=COLOR1, bd=1)
    choose_graph_label.place(relx=0.16, rely=0.32, relheight=0.15, relwidth=0.385, anchor="n")
    tk.Radiobutton(report_root, text="   Leak Rate", fg=COLOR_BLACK, bg=COLOR_WHITE,
                   variable=rb_choose_graph, value=0, font=default_font
                   ).place(relx=0.15, rely=0.455)
    tk.Radiobutton(report_root, text="   Highest Leak", fg=COLOR_BLACK, bg=COLOR_WHITE,
                   variable=rb_choose_graph, value=1, font=default_font
                   ).place(relx=0.15, rely=0.535)
    tk.Radiobutton(report_root, text="   Both", fg=COLOR_BLACK, bg=COLOR_WHITE,
                   variable=rb_choose_graph, value=2, font=default_font
                   ).place(relx=0.15, rely=0.615)

    # Notes Text box
    lbl_rb_data_dir = tk.Label(report_root, text="Note: ", font=default_font,
                               bg=COLOR_WHITE, fg=COLOR1, bd=1)
    lbl_rb_data_dir.place(relx=0.415, rely=0.32, relheight=0.15, relwidth=0.1, anchor="n")
    notes_input = tk.Frame(report_root, bd=0.5, relief="solid")
    notes_input.place(relx=0.43, rely=0.44, relheight=0.25, relwidth=0.52)
    txt_note = tk.Text(notes_input, font=default_font)
    txt_note.pack(fill="both", expand=True)

    # Save Button
    tk.Button(report_root, text="Create Report", font=("Arial", 10, "bold"),
              bg=COLOR1, command=create,
              fg=COLOR_WHITE).place(relx=0.08, rely=0.8, relheight=0.075, relwidth=0.25)

    report_root.mainloop()
