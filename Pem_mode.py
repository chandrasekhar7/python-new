"""
pem_mode.py

This module likely contains the user interface and functionality specific to the PEM
(Profiled Elastomeric Moulding)
mode of the Leakware application. It handles the creation of the PEM-specific user
interface and any related
operations or data processing required for the PEM leak testing process.

Key Functions:
- pem_mode_config(tk, root, mode_of_measurement, leakware_id, repository):
  Function to create and configure the PEM mode user interface.

Dependencies:
- tkinter (for creating the graphical user interface)
- Potentially other modules or libraries specific to PEM mode functionality

Usage:
This module is typically imported and the `pem_mode_config` function is called when the user selects
the PEM mode in the Leakware application. It sets up the necessary user interface components and
handles any PEM-specific operations or data processing required for leak testing in PEM mode.
"""
import tkinter.font as tkFont
from datetime import date
from datetime import datetime

from db_model import PemSpecificElements


def pem_mode_config(tk, data_header_pem, mode_of_measurement, leakware_id, repository):
    # textbox for specimen properties
    '''
    configuration for pem mode, it mean element specification for pem mode.
    '''
    global project_no, inspector, fastener_type, plating_on_fastener, \
        panel, plating_on_panel, panel_thickness, hole_diameter, selected_hole_prep_method, \
        panel_hardness, data_note, selected_install_machine_options_var, \
        selected_installation_direction, installation_force, installation_anvil, \
        installation_punch, test_direction_clinch, test_direction
    global elem_direction

    specification = repository.get_specification(leakware_id, mode_of_measurement)
    print(specification)

    def get_image_size(image):
        return image.width() / 78, image.height() / 84

    if specification:
        project_no=specification.project_number
        inspector=specification.inspector
        fastener_type=specification.fastener_type
        plating_on_fastener=specification.plating_on_fastener
        panel=specification.panel
        plating_on_panel=specification.plating_on_panel
        panel_thickness=specification.panel_thickness
        hole_diameter=specification.hole_diameter
        selected_hole_prep_method=specification.hole_preparation
        panel_hardness=specification.panel_hardness
        selected_install_machine_options_var=specification.install_machine_type
        selected_installation_direction=specification.installation_direction
        installation_force=specification.installation_force
        installation_anvil=specification.installation_anvil
        data_note=specification.note
        installation_punch=specification.installation_punch
        test_direction_clinch=specification.test_direction_clinch
        test_direction=specification.test_direction

    data_header_pem.title("Data Information.")
    data_header_pem.configure(bg="white")
    data_header_pem.iconbitmap("favicon.ico")
    data_header_pem.geometry("840x760")
    labelfont = ("arial", 10)
    txtfont = ("arial", 8)

    ### direction images
    rb_direction_variable = tk.IntVar()
    rb_direction_variable.set(6)

    ### direction images
    rb_direction_variable_dir = tk.IntVar()
    rb_direction_variable_dir.set(4)
    # Calculate the resizing factor
    rnd_up_img = tk.PhotoImage(file="./Images/all_direction.png")
    width_factor, height_factor = get_image_size(rnd_up_img)
    rnd_up_img = rnd_up_img.subsample(int(width_factor), int(height_factor))
    rnd_down_img = tk.PhotoImage(file="./Images/top_left.png")
    width_factor, height_factor = get_image_size(rnd_down_img)
    rnd_down_img = rnd_down_img.subsample(int(width_factor), int(height_factor))
    capnut_up_img = tk.PhotoImage(file="./Images/top_right.png")
    width_factor, height_factor = get_image_size(capnut_up_img)
    capnut_up_img = capnut_up_img.subsample(int(width_factor), int(height_factor))
    capnut_down_img = tk.PhotoImage(file="./Images/bottom_right.png")
    width_factor, height_factor = get_image_size(capnut_down_img)
    capnut_down_img = capnut_down_img.subsample(int(width_factor), int(height_factor))
    sbf_up_img = tk.PhotoImage(file="./Images/bottom_left.png")
    width_factor, height_factor = get_image_size(sbf_up_img)
    sbf_up_img = sbf_up_img.subsample(int(width_factor), int(height_factor))

    color4 = "#2049b0"  # profilblau?
    color1 = color4
    colorf = "#ffffff"  # font #white

    tk.Label(data_header_pem, text="Project-No.:", font=labelfont,
             fg=color1, bg="white").place(relx=0.02, rely=0.005, relheight=0.04, relwidth=0.2)
    txt_pn = tk.Text(data_header_pem, font=txtfont)
    txt_pn.place(relx=0.24, rely=0.01, relheight=0.04, relwidth=0.2)
    tk.Label(data_header_pem, text="Date:", font=labelfont, fg=color1,
             bg="white").place(relx=0.52, rely=0.005, relheight=0.04, relwidth=0.2)
    tk.Label(data_header_pem, text=str(date.today()), font=labelfont,
             fg=color1, bg="white").place(relx=0.77, rely=0.005, relheight=0.04, relwidth=0.2)
    tk.Label(data_header_pem, text="Inspector:", font=labelfont, fg=color1,
             bg="white").place(relx=0.02, rely=0.06, relheight=0.04, relwidth=0.2)
    txt_inspector = tk.Text(data_header_pem, font=txtfont)
    txt_inspector.place(relx=0.24, rely=0.06, relheight=0.04, relwidth=0.2)
    tk.Label(data_header_pem, text="Fastener Type:", font=labelfont,
             fg=color1, bg="white").place(relx=0.52, rely=0.06, relheight=0.04, relwidth=0.2)
    txt_fastener_type = tk.Text(data_header_pem, font=txtfont)
    txt_fastener_type.place(relx=0.74, rely=0.06, relheight=0.04, relwidth=0.2)
    tk.Label(data_header_pem, text="Plating on Fastener:", font=labelfont,
             fg=color1, bg="white").place(relx=0.02, rely=0.12, relheight=0.04, relwidth=0.2)
    txt_plating_fastener = tk.Text(data_header_pem, font=txtfont)
    txt_plating_fastener.place(relx=0.24, rely=0.12, relheight=0.04, relwidth=0.2)

    tk.Label(data_header_pem, text="Panel:", font=labelfont, fg=color1,
             bg="white").place(relx=0.52, rely=0.12, relheight=0.04, relwidth=0.2)
    txt_panel = tk.Text(data_header_pem, font=txtfont)
    txt_panel.place(relx=0.74, rely=0.12, relheight=0.04, relwidth=0.2)

    tk.Label(data_header_pem, text="Plating on Panel:", font=labelfont,
             fg=color1, bg="white").place(relx=0.02, rely=0.18, relheight=0.04, relwidth=0.2)
    txt_plating_panel = tk.Text(data_header_pem, font=txtfont)
    txt_plating_panel.place(relx=0.24, rely=0.18, relheight=0.04, relwidth=0.2)

    tk.Label(data_header_pem, text="Panel Thickness:", font=labelfont,
             fg=color1, bg="white").place(relx=0.52, rely=0.18, relheight=0.04, relwidth=0.2)
    txt_panel_thickness = tk.Text(data_header_pem, font=txtfont)
    txt_panel_thickness.place(relx=0.74, rely=0.18, relheight=0.03, relwidth=0.15)
    # Create a StringVar to store the selected unit
    unit_var = tk.StringVar()
    unit_var.set("mm")  # Set the default unit to mm

    # Create the dropdown menu with options
    options = ["mm", "inch"]
    dropdown = tk.OptionMenu(data_header_pem, unit_var, *options)
    dropdown.place(relx=0.90, rely=0.18, relheight=0.05, relwidth=0.07)

    dropdown_font = tkFont.Font(family='arial', size=10)  # Replace with your desired font
    menu = data_header_pem.nametowidget(dropdown.menuname)
    menu.config(font=dropdown_font)

    tk.Label(data_header_pem, text="Hole Diameter:", font=labelfont, fg=color1,
             bg="white").place(relx=0.02, rely=0.24, relheight=0.04, relwidth=0.2)
    txt_hole_dia = tk.Text(data_header_pem, font=txtfont)
    txt_hole_dia.place(relx=0.24, rely=0.24, relheight=0.03, relwidth=0.15)

    # Create a StringVar to store the selected unit
    unit_var_hole_dia = tk.StringVar()
    unit_var_hole_dia.set("mm")  # Set the default unit to mm

    # Create the dropdown menu with options
    options = ["mm", "inch"]
    dropdown_dia = tk.OptionMenu(data_header_pem, unit_var_hole_dia, *options)
    dropdown_dia.place(relx=0.41, rely=0.24, relheight=0.05, relwidth=0.07)

    dropdown_font_dia = tkFont.Font(family='arial', size=10)  # Replace with your desired font
    menu = data_header_pem.nametowidget(dropdown_dia.menuname)
    menu.config(font=dropdown_font_dia)

    lbl_hole_prepation = tk.Label(data_header_pem, text="Hole Preparation:",
                                  font=labelfont, fg=color1, bg="white"
                                  ).place(relx=0.52, rely=0.24, relheight=0.04, relwidth=0.2)

    # Create a StringVar to store the selected unit
    unit_var_hole = tk.StringVar()
    unit_var_hole.set("Punched")  # Set the default unit to mm
    options_hole = ["Punched", "Machined", "Laser Cut"]
    dropdown_hole = tk.OptionMenu(data_header_pem, unit_var_hole, *options_hole)
    dropdown_hole.place(relx=0.74, rely=0.24, relheight=0.04, relwidth=0.2)

    tk.Label(data_header_pem, text="Panel Hardness:", font=labelfont, fg=color1, bg="white"
             ).place(relx=0.02, rely=0.30, relheight=0.04, relwidth=0.2)
    txt_panel_hardness = tk.Text(data_header_pem, font=txtfont)
    txt_panel_hardness.place(relx=0.24, rely=0.30, relheight=0.03, relwidth=0.15)

    # Create a StringVar to store the selected unit
    unit_panel_hardness = tk.StringVar()
    unit_panel_hardness.set("HRB")  # Set the default unit to mm
    options_panel_hardness = ["HRB", "HB", "HRC"]
    dropdown_panel_hardness = tk.OptionMenu(data_header_pem, unit_panel_hardness,
                                            *options_panel_hardness)
    dropdown_panel_hardness.place(relx=0.41, rely=0.30, relheight=0.05, relwidth=0.07)

    tk.Label(data_header_pem, text="Install Machine Type:", font=labelfont, fg=color1,
             bg="white").place(relx=0.52, rely=0.30, relheight=0.04, relwidth=0.2)
    # Create a StringVar to store the selected unit
    unit_var_machine_type = tk.StringVar()
    unit_var_machine_type.set("Haeger")  # Set the default unit to mm
    options_machine_type = ["Haeger", "Pemserter"]
    dropdown_machine_type = tk.OptionMenu(data_header_pem, unit_var_machine_type,
                                          *options_machine_type)
    dropdown_machine_type.place(relx=0.74, rely=0.30, relheight=0.04, relwidth=0.2)

    tk.Label(data_header_pem, text="Installation Direction:", font=labelfont, fg=color1,
             bg="white").place(relx=0.02, rely=0.36, relheight=0.04, relwidth=0.2)
    unit_var_direction = tk.StringVar()
    unit_var_direction.set("Punched side")  # Set the default unit to mm
    options_installation_direction = ["Punched side", "Blowout side"]
    dropdown_installation_direction = tk.OptionMenu(data_header_pem, unit_var_direction,
                                                    *options_installation_direction)
    dropdown_installation_direction.place(relx=0.24, rely=0.36, relheight=0.04, relwidth=0.2)
    tk.Label(data_header_pem, text="Installation Force:", font=labelfont, fg=color1, bg="white"
             ).place(relx=0.52, rely=0.36, relheight=0.04, relwidth=0.2)
    txt_installation_force = tk.Text(data_header_pem, font=txtfont)
    txt_installation_force.place(relx=0.74, rely=0.36, relheight=0.03, relwidth=0.2)
    tk.Label(data_header_pem, text="kN", font=labelfont, fg=color1, bg="white"
             ).place(relx=0.92, rely=0.36,relheight=0.03,relwidth=0.05)
    tk.Label(data_header_pem, text="Installation Anvil:", font=labelfont, fg=color1,bg="white"
             ).place(relx=0.02, rely=0.42, relheight=0.04, relwidth=0.2)
    txt_installation_anvil = tk.Text(data_header_pem, font=txtfont)
    txt_installation_anvil.place(relx=0.27, rely=0.42, relheight=0.04, relwidth=0.2)
    tk.Label(data_header_pem, text="Installation Punch:", font=labelfont, fg=color1, bg="white"
             ).place(relx=0.52, rely=0.42, relheight=0.04, relwidth=0.2)
    txt_installation_punch = tk.Text(data_header_pem, font=txtfont)
    txt_installation_punch.place(relx=0.74, rely=0.42, relheight=0.04, relwidth=0.2)

    tk.Label(data_header_pem, text="Note:", font=labelfont, fg=color1, bg="white"
             ).place(relx=0.04, rely=0.42, relheight=0.04, relwidth=0.08)
    txt_notehead = tk.Text(data_header_pem, font=txtfont)
    txt_notehead.place(relx=0.15, rely=0.43, relheight=0.08, relwidth=0.8)

    ##radiobuttons Prüfrichtung
    frame_rb_data = tk.Frame(data_header_pem, bg="white")
    frame_rb_data.place(relx=0, rely=0.41, relheight=0.25, relwidth=1)
    lbl_rb_data = tk.Label(frame_rb_data, text="Test direction:", font=labelfont,
                           bg="white", fg=color1)
    lbl_rb_data.place(relx=0.27, rely=0.02, relheight=0.2, relwidth=0.385)

    rb_1_direction = tk.Radiobutton(frame_rb_data, text="", fg=color1, bg="white",
                                    variable=rb_direction_variable, value=0)
    rb_1_direction.place(relx=0.1, rely=0.25, relheight=0.1, relwidth=0.05)
    rnd_up_lbl = tk.Label(frame_rb_data, image=rnd_up_img, bg="white")
    rnd_up_lbl.place(relx=0.05, rely=0.35, relheight=0.6, relwidth=0.15)

    rb_2_direction = tk.Radiobutton(frame_rb_data, text="", fg=color1, bg="white",
                                    variable=rb_direction_variable, value=1)
    rb_2_direction.place(relx=0.25, rely=0.25, relheight=0.1, relwidth=0.05)
    rnd_down_lbl = tk.Label(frame_rb_data, image=rnd_down_img, bg="white")
    rnd_down_lbl.place(relx=0.2, rely=0.35, relheight=0.6, relwidth=0.15)
    rb_3_direction = tk.Radiobutton(frame_rb_data, text="", fg=color1, bg="white",
                                    variable=rb_direction_variable, value=2)
    rb_3_direction.place(relx=0.4, rely=0.25, relheight=0.1, relwidth=0.05)
    capnut_up_lbl = tk.Label(frame_rb_data, image=capnut_up_img, bg="white")
    capnut_up_lbl.place(relx=0.35, rely=0.35, relheight=0.6, relwidth=0.15)
    rb_4_direction = tk.Radiobutton(frame_rb_data, text="", fg=color1, bg="white",
                                    variable=rb_direction_variable, value=3)
    rb_4_direction.place(relx=0.55, rely=0.25, relheight=0.1, relwidth=0.05)
    capnut_down_lbl = tk.Label(frame_rb_data, image=capnut_down_img, bg="white")
    capnut_down_lbl.place(relx=0.5, rely=0.35, relheight=0.6, relwidth=0.15)
    rb_5_direction = tk.Radiobutton(frame_rb_data, text="", fg=color1, bg="white",
                                    variable=rb_direction_variable, value=4)
    rb_5_direction.place(relx=0.7, rely=0.25, relheight=0.1, relwidth=0.05)
    sbf_up_lbl = tk.Label(frame_rb_data, image=sbf_up_img, bg="white")
    sbf_up_lbl.place(relx=0.65, rely=0.35, relheight=0.6, relwidth=0.15)

    ##radiobuttons Test direction
    frame_rb_data_dir = tk.Frame(data_header_pem, bg="white")
    frame_rb_data_dir.place(relx=0, rely=0.65, relheight=0.25, relwidth=1)

    # Notes
    lbl_rb_data_dir = tk.Label(frame_rb_data_dir, text="Note: ", font=labelfont,
                               bg="white", fg=color1, bd=1)
    lbl_rb_data_dir.place(relx=0.1, rely=0, relheight=0.15, relwidth=0.8, anchor="n")
    notes_input = tk.Frame(frame_rb_data_dir, bd=0.5, relief="solid")
    notes_input.place(relx=0.1, rely=0.2, relheight=0.6, relwidth=0.85)
    txt_note = tk.Text(notes_input, font=("Arial", 10))
    txt_note.pack(fill="both", expand=True)

    if specification:
        txt_pn.insert(tk.END, project_no)
        txt_inspector.insert(tk.END, inspector)
        txt_fastener_type.insert(tk.END, fastener_type)
        txt_plating_fastener.insert(tk.END, plating_on_fastener)
        txt_panel.insert(tk.END, panel)
        txt_plating_panel.insert(tk.END, plating_on_panel)
        txt_panel_thickness.insert(tk.END, panel_thickness)
        txt_hole_dia.insert(tk.END, hole_diameter)
        txt_panel_hardness.insert(tk.END, panel_hardness)
        txt_installation_force.insert(tk.END, installation_force)
        txt_note.insert(tk.END, data_note)
        rb_direction_variable.set(test_direction)
        rb_direction_variable_dir.set(test_direction_clinch)

    def textbox_vars_head_pem_mode():
        global project_no, inspector, fastener_type, plating_on_fastener, \
            panel, plating_on_panel, panel_thickness, hole_diameter, selected_hole_prep_method, \
            panel_hardness,data_note, selected_install_machine_options_var, \
            selected_installation_direction, installation_force, installation_anvil, \
            installation_punch,test_direction_clinch,test_direction

        global elem_direction
        global pem_specific_id

        project_no = txt_pn.get(1.0, "end-1c")
        inspector = txt_inspector.get(1.0, "end-1c")
        # date = text_widgets[2].get("1.0", "end-1c")
        fastener_type = txt_fastener_type.get("1.0", "end-1c")
        plating_on_fastener = txt_plating_fastener.get("1.0", "end-1c")
        panel = txt_panel.get("1.0", "end-1c")
        plating_on_panel = txt_plating_panel.get("1.0", "end-1c")
        panel_thickness = txt_panel_thickness.get("1.0", "end-1c")
        hole_diameter = txt_hole_dia.get("1.0", "end-1c")
        # hole_preparation = text_widgets[9].get("1.0", "end-1c")
        selected_hole_prep_method = unit_var_hole.get()
        panel_hardness = txt_panel_hardness.get("1.0", "end-1c")
        selected_install_machine_options_var = unit_var_machine_type.get()
        selected_installation_direction = unit_var_direction.get()
        installation_force = txt_installation_force.get("1.0", "end-1c")
        installation_anvil = txt_installation_anvil.get("1.0", "end-1c")
        installation_punch = txt_installation_punch.get("1.0", "end-1c")
        data_note = txt_note.get("1.0", "end-1c")
        test_direction_clinch = rb_direction_variable_dir.get()
        test_direction = rb_direction_variable.get()

        selected_panel_thickness = unit_var.get()
        selected_hole_dia = unit_var_hole_dia.get()
        selected_panel_hardness = unit_panel_hardness.get()

        # insert data to the data_information table
        data_pennspecificelements = PemSpecificElements(
            leakware_id=leakware_id,
            project_number=project_no,
            inspector=inspector,
            date=datetime.now(),
            fastener_type=fastener_type,
            plating_on_fastener=plating_on_fastener,
            panel=panel,
            plating_on_panel=plating_on_panel,
            panel_thickness=panel_thickness,
            panel_thickness_dia=selected_panel_thickness,
            hole_diameter=hole_diameter,
            hole_preparation=selected_hole_prep_method,
            hole_preparation_dia=selected_hole_dia,
            panel_hardness=panel_hardness,
            panel_hardness_type=selected_panel_hardness,
            install_machine_type=selected_install_machine_options_var,
            installation_direction=selected_installation_direction,
            installation_force=installation_force,
            installation_anvil=installation_anvil,
            note=data_note,
            installation_punch=installation_punch,
            test_direction_clinch=test_direction_clinch,
            test_direction=test_direction,
            active=True,
        )
        pem_specific_id = repository.insert_penn_specific_elements(data_pennspecificelements).pem_specific_id

        btn_text3.set("Changes saved.")
        data_header_pem.after(800, lambda:data_header_pem.destroy())
    btn_text3 = tk.StringVar()
    btn_text3.set("Save")
    button_save3 = tk.Button(data_header_pem, textvariable=btn_text3, font=("arial", 12),
                             bg=color1, fg=colorf, command=textbox_vars_head_pem_mode)
    button_save3.place(relx=.46, rely=0.91, relheight=0.06, relwidth=0.15, anchor="nw")

    def tb_clearall_pem_mode():
        global project_no, inspector, fastener_type, plating_on_fastener, \
            panel, plating_on_panel, panel_thickness, hole_diameter, selected_hole_prep_method, \
            panel_hardness, selected_install_machine_options_var, selected_installation_direction, \
            installation_force, installation_anvil, installation_punch, test_direction_clinch, \
            test_direction
        global elem_direction

        project_no = ""
        inspector = ""
        fastener_type = ""
        plating_on_fastener = ""
        plating_on_panel = ""
        panel_thickness = ""
        hole_diameter = ""
        panel_hardness = ""
        installation_force = ""
        installation_anvil = ""
        installation_punch = ""
        test_direction_clinch = ""
        test_direction = ""
        elem_direction = ""
        txt_pn.delete(1.0, tk.END)
        txt_inspector.delete(1.0, tk.END)
        txt_fastener_type.delete(1.0, tk.END)
        txt_plating_fastener.delete(1.0, tk.END)
        txt_panel.delete(1.0, tk.END)
        txt_plating_panel.delete(1.0, tk.END)
        txt_panel_thickness.delete(1.0, tk.END)
        txt_hole_dia.delete(1.0, tk.END)
        txt_panel_hardness.delete(1.0, tk.END)
        txt_installation_force.delete(1.0, tk.END)
        txt_note.delete(1.0, tk.END)
        rb_direction_variable.set(6)
        rb_direction_variable_dir.set(4)

    button_clearall = tk.Button(data_header_pem, text="Clear", font=("arial", 12), bg=color1,
                                fg=colorf, command=tb_clearall_pem_mode)
    button_clearall.place(relx=.305, rely=0.91, relheight=0.06, relwidth=0.15, anchor="nw")

    def focus_next_widget(event):
        event.widget.tk_focusNext().focus()
        return "break"

    txt_pn.bind("<Tab>", focus_next_widget)
    txt_inspector.bind("<Tab>", focus_next_widget)
    txt_fastener_type.bind("<Tab>", focus_next_widget)
    txt_plating_fastener.bind("<Tab>", focus_next_widget)
    txt_panel.bind("<Tab>", focus_next_widget)
    txt_plating_panel.bind("<Tab>", focus_next_widget)
    txt_panel_thickness.bind("<Tab>", focus_next_widget)
    txt_hole_dia.bind("<Tab>", focus_next_widget)
    txt_panel_hardness.bind("<Tab>", focus_next_widget)
    txt_installation_force.bind("<Tab>", focus_next_widget)

    data_header_pem.mainloop()
