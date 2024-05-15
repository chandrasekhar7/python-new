"""
profil_specification.py

This module likely contains the user interface and functionality specific to the PROFIL mode
of the Leakware application. It handles the creation of the PROFIL-specific user interface
and any related operations or data processing required for the PROFIL leak testing process.

Key Functions:
- profil_specification(tk, root, mode_of_measurement, leakware_id, repository):
  Function to create and configure the PROFIL mode user interface.

Dependencies:
- tkinter (for creating the graphical user interface)
- Potentially other modules or libraries specific to PROFIL mode functionality

Usage:
This module is typically imported and the `profil_specification` function is called when the
user selects the PROFIL mode in the Leakware application. It sets up the necessary user
interface components and handles any PROFIL-specific operations or data processing required
for leak testing in PROFIL mode.
"""
from datetime import date, datetime
from db_model import DataInformation

def profil_specification(tk, data_header, mode_of_measurement, leakware_id, repository):
    '''
    This is for profil mode specification
    '''
    # textbox for specimen properties
    global txt_pn_var, txt_elem_var, txt_material_var, txt_thickness_var, txt_die_var, \
        txt_hprep_var, txt_mh_var, txt_coating_var, txt_inspector_var, txt_holesize_var, \
        txt_hardness_var, txt_force_var, txt_tooling_var, txt_note_var
    global elem_direction

    ### direction images
    rb_direction_variable = tk.IntVar()
    rb_direction_variable.set(6)
    rnd_up_img = tk.PhotoImage(file="./Images/nut_facing_upwards.gif")
    rnd_down_img = tk.PhotoImage(file="./Images/nut_facing_downwards.gif")
    capnut_up_img = tk.PhotoImage(file="./Images/capnut_facing_upwards.gif")
    capnut_down_img = tk.PhotoImage(file="./Images/capnut_facing_downwards.gif")
    sbf_up_img = tk.PhotoImage(file="./Images/bolt_facing_upwards.gif")
    sbf_down_img = tk.PhotoImage(file="./Images/bolt_facing_downwards.gif")

    # check the last data information for leakware load the data.
    specification = repository.get_specification(leakware_id, mode_of_measurement)
    if specification:
        txt_pn_var=specification.project_number
        txt_elem_var=specification.element
        txt_thickness_var=specification.thickness
        txt_hprep_var=specification.hole_prepation
        txt_coating_var=specification.coating
        txt_note_var=specification.note
        txt_material_var=specification.material
        txt_die_var=specification.die_button
        txt_mh_var=specification.mh_mab
        txt_inspector_var=specification.inspector
        txt_holesize_var=specification.holesize
        txt_hardness_var=specification.material_hardness
        txt_force_var=specification.installation_force
        txt_tooling_var=specification.installation_tooling
        rb_direction_variable.set(specification.direction_of_measurements)

    # color1 = "#c4e4ff"
    # color1 = "#c4cfff" #light blue
    color4 = "#2049b0"  # profilblau?
    color1 = color4
    colorf = "#ffffff"  # font #white

    data_header.title("Data information")
    data_header.configure(bg="white")
    data_header.geometry("750x560")
    labelfont = ("arial", 14)
    txtfont = ("arial", 12)
    ## Labels + Textbox
    tk.Label(data_header, text="Project-No.:", font=labelfont, fg=color1,
             bg="white").place(relx=0.02, rely=0.005, relheight=0.04, relwidth=0.2)
    txt_pn = tk.Text(data_header, font=txtfont)
    txt_pn.place(relx=0.27, rely=0.01, relheight=0.04, relwidth=0.2)
    tk.Label(data_header, text="Date:", font=labelfont, fg=color1,
             bg="white").place(relx=0.52, rely=0.005, relheight=0.04, relwidth=0.2)
    tk.Label(data_header, text=str(date.today()), font=labelfont, fg=color1,
             bg="white").place(relx=0.77, rely=0.005, relheight=0.04, relwidth=0.2)
    tk.Label(data_header, text="Element:", font=labelfont, fg=color1,
             bg="white").place(relx=0.02, rely=0.06, relheight=0.04, relwidth=0.2)
    txt_elem = tk.Text(data_header, font=txtfont)
    txt_elem.place(relx=0.27, rely=0.06, relheight=0.04, relwidth=0.2)
    tk.Label(data_header, text="Material:", font=labelfont, fg=color1,
             bg="white").place(relx=0.52, rely=0.06, relheight=0.04, relwidth=0.2)
    txt_material = tk.Text(data_header, font=txtfont)
    txt_material.place(relx=0.77, rely=0.06, relheight=0.04, relwidth=0.2)
    tk.Label(data_header, text="Thickness:", font=labelfont, fg=color1,
             bg="white").place(relx=0.02, rely=0.12, relheight=0.04, relwidth=0.2)
    txt_thickness = tk.Text(data_header, font=txtfont)
    txt_thickness.place(relx=0.27, rely=0.12, relheight=0.04, relwidth=0.15)
    tk.Label(data_header, text="mm", font=labelfont, fg=color1,
             bg="white").place(relx=0.42, rely=0.12, relheight=0.04, relwidth=0.06)
    tk.Label(data_header, text="Die Button:", font=labelfont, fg=color1,
             bg="white").place(relx=0.52, rely=0.12, relheight=0.04, relwidth=0.2)
    txt_die = tk.Text(data_header, font=txtfont)
    txt_die.place(relx=0.77, rely=0.12, relheight=0.04, relwidth=0.2)
    tk.Label(data_header, text="Mh-Maß:", font=labelfont, fg=color1,
             bg="white").place(relx=0.02, rely=0.18, relheight=0.04, relwidth=0.2)
    txt_mhmass = tk.Text(data_header, font=txtfont)
    txt_mhmass.place(relx=0.27, rely=0.18, relheight=0.04, relwidth=0.2)
    tk.Label(data_header, text="Hole Preparation:", font=labelfont, fg=color1,
             bg="white").place(relx=0.52, rely=0.18, relheight=0.04, relwidth=0.2)
    txt_holeprep = tk.Text(data_header, font=txtfont)
    txt_holeprep.place(relx=0.77, rely=0.18, relheight=0.04, relwidth=0.2)
    tk.Label(data_header, text="Coating:", font=labelfont, fg=color1,
             bg="white").place(relx=0.02, rely=0.24, relheight=0.04, relwidth=0.2)
    txt_coating = tk.Text(data_header, font=txtfont)
    txt_coating.place(relx=0.27, rely=0.24, relheight=0.04, relwidth=0.2)
    tk.Label(data_header, text="Inspector:", font=labelfont, fg=color1,
             bg="white").place(relx=0.52, rely=0.24, relheight=0.04, relwidth=0.2)
    txt_inspector = tk.Text(data_header, font=txtfont)
    txt_inspector.place(relx=0.77, rely=0.24, relheight=0.04, relwidth=0.2)
    tk.Label(data_header, text="Hole Size:", font=labelfont, fg=color1,
             bg="white").place(relx=0.02, rely=0.30, relheight=0.04, relwidth=0.2)
    txt_holesize = tk.Text(data_header, font=txtfont)
    txt_holesize.place(relx=0.27, rely=0.30, relheight=0.04, relwidth=0.2)
    tk.Label(data_header, text="Material Hardness:", font=labelfont,
             fg=color1, bg="white").place(relx=0.52, rely=0.30, relheight=0.04, relwidth=0.21)
    txt_hardness = tk.Text(data_header, font=txtfont)
    txt_hardness.place(relx=0.77, rely=0.30, relheight=0.04, relwidth=0.2)
    tk.Label(data_header, text="Installation Force:", font=labelfont,
             fg=color1, bg="white").place(relx=0.02, rely=0.36, relheight=0.04, relwidth=0.2)
    txt_force = tk.Text(data_header, font=txtfont)
    txt_force.place(relx=0.27, rely=0.36, relheight=0.04, relwidth=0.2)
    tk.Label(data_header, text="Installation Tooling:", font=labelfont,
             fg=color1, bg="white").place(relx=0.52, rely=0.36, relheight=0.04, relwidth=0.21)
    txt_tooling = tk.Text(data_header, font=txtfont)
    txt_tooling.place(relx=0.77, rely=0.36, relheight=0.04, relwidth=0.2)
    tk.Label(data_header, text="Note:", font=labelfont, fg=color1,
             bg="white").place(relx=0.04, rely=0.74, relheight=0.06, relwidth=0.08)
    txt_notehead = tk.Text(data_header, font=txtfont)
    txt_notehead.place(relx=0.15, rely=0.75, relheight=0.08, relwidth=0.8)
    ##radiobuttons Prüfrichtung
    frame_rb_data = tk.Frame(data_header, bg="white")
    frame_rb_data.place(relx=0, rely=0.42, relheight=0.33, relwidth=1)
    lbl_rb_data = tk.Label(frame_rb_data, text="Direction of measurements:",
                           font=labelfont, bg="white", fg=color1)
    lbl_rb_data.place(relx=0.02, rely=0.02, relheight=0.2, relwidth=0.385)
    rb_1_direction = tk.Radiobutton(frame_rb_data, text="", fg=color1,
                                    bg="white", variable=rb_direction_variable, value=0)
    rb_1_direction.place(relx=0.1, rely=0.25, relheight=0.1, relwidth=0.05)
    rnd_up_lbl = tk.Label(frame_rb_data, image=rnd_up_img, bg="white")
    rnd_up_lbl.place(relx=0.05, rely=0.35, relheight=0.6, relwidth=0.15)
    rb_2_direction = tk.Radiobutton(frame_rb_data, text="", fg=color1,
                                    bg="white", variable=rb_direction_variable, value=1)
    rb_2_direction.place(relx=0.25, rely=0.25, relheight=0.1, relwidth=0.05)
    rnd_down_lbl = tk.Label(frame_rb_data, image=rnd_down_img, bg="white")
    rnd_down_lbl.place(relx=0.2, rely=0.35, relheight=0.6, relwidth=0.15)
    rb_3_direction = tk.Radiobutton(frame_rb_data, text="", fg=color1,
                                    bg="white", variable=rb_direction_variable, value=2)
    rb_3_direction.place(relx=0.4, rely=0.25, relheight=0.1, relwidth=0.05)
    capnut_up_lbl = tk.Label(frame_rb_data, image=capnut_up_img, bg="white")
    capnut_up_lbl.place(relx=0.35, rely=0.35, relheight=0.6, relwidth=0.15)
    rb_4_direction = tk.Radiobutton(frame_rb_data, text="", fg=color1,
                                    bg="white", variable=rb_direction_variable, value=3)
    rb_4_direction.place(relx=0.55, rely=0.25, relheight=0.1, relwidth=0.05)
    capnut_down_lbl = tk.Label(frame_rb_data, image=capnut_down_img, bg="white")
    capnut_down_lbl.place(relx=0.5, rely=0.35, relheight=0.6, relwidth=0.15)
    rb_5_direction = tk.Radiobutton(frame_rb_data, text="", fg=color1,
                                    bg="white", variable=rb_direction_variable, value=4)
    rb_5_direction.place(relx=0.7, rely=0.25, relheight=0.1, relwidth=0.05)
    sbf_up_lbl = tk.Label(frame_rb_data, image=sbf_up_img, bg="white")
    sbf_up_lbl.place(relx=0.65, rely=0.35, relheight=0.6, relwidth=0.15)
    rb_6_direction = tk.Radiobutton(frame_rb_data, text="", fg=color1,
                                    bg="white", variable=rb_direction_variable, value=5)
    rb_6_direction.place(relx=0.85, rely=0.25, relheight=0.1, relwidth=0.05)
    sbf_down_lbl = tk.Label(frame_rb_data, image=sbf_down_img, bg="white")
    sbf_down_lbl.place(relx=0.8, rely=0.35, relheight=0.6, relwidth=0.15)

    if specification :
        txt_pn.insert(tk.END, txt_pn_var)
        txt_elem.insert(tk.END, txt_elem_var)
        txt_material.insert(tk.END, txt_material_var)
        txt_thickness.insert(tk.END, txt_thickness_var)
        txt_die.insert(tk.END, txt_die_var)
        txt_mhmass.insert(tk.END, txt_mh_var)
        txt_holeprep.insert(tk.END, txt_hprep_var)
        txt_coating.insert(tk.END, txt_coating_var)
        txt_inspector.insert(tk.END, txt_inspector_var)
        txt_holesize.insert(tk.END, txt_holesize_var)
        txt_hardness.insert(tk.END, txt_hardness_var)
        txt_force.insert(tk.END, txt_force_var)
        txt_tooling.insert(tk.END, txt_tooling_var)
        txt_notehead.insert(tk.END, txt_note_var)

    def textbox_vars_head():
        global txt_pn_var, txt_elem_var, txt_material_var, txt_thickness_var, \
            txt_die_var, txt_hprep_var, txt_mh_var, txt_coating_var, txt_inspector_var, \
            txt_holesize_var, txt_hardness_var, txt_force_var, txt_tooling_var, txt_note_var
        global elem_direction
        global data_information_id
        txt_pn_var = txt_pn.get(1.0, "end-1c")
        txt_elem_var = txt_elem.get(1.0, "end-1c")
        txt_material_var = txt_material.get(1.0, "end-1c")
        txt_thickness_var = txt_thickness.get(1.0, "end-1c")
        txt_die_var = txt_die.get(1.0, "end-1c")
        txt_hprep_var = txt_holeprep.get(1.0, "end-1c")
        txt_mh_var = txt_mhmass.get(1.0, "end-1c")
        txt_coating_var = txt_coating.get(1.0, "end-1c")
        txt_inspector_var = txt_inspector.get(1.0, "end-1c")
        txt_holesize_var = txt_holesize.get(1.0, "end-1c")
        txt_hardness_var = txt_hardness.get(1.0, "end-1c")
        txt_force_var = txt_force.get(1.0, "end-1c")
        txt_tooling_var = txt_tooling.get(1.0, "end-1c")
        txt_note_var = txt_notehead.get(1.0, "end-1c")
        direction_variable = rb_direction_variable.get()
        # elem_direction = get_elem_direction_value(direction_variable)

        # insert data to the data_information table
        data_information = DataInformation(
            leakware_id=leakware_id,
            project_number=txt_pn_var,
            element=txt_elem_var,
            thickness=txt_thickness_var,
            hole_prepation=txt_hprep_var,
            coating=txt_coating_var,
            direction_of_measurements= direction_variable,
            note=txt_note_var,
            date=datetime.now(),
            material=txt_material_var,
            die_button=txt_die_var,
            mh_mab=txt_mh_var,
            inspector=txt_inspector_var,
            holesize=txt_holesize_var,
            material_hardness=txt_hardness_var,
            installation_force=txt_force_var,
            installation_tooling=txt_tooling_var,
            active=True)
        data_information_id = repository.insert_data_information(data_information).data_information_id

        btn_text3.set("Changes saved.")
        data_header.after(800, lambda:data_header.destroy())
    btn_text3 = tk.StringVar()
    btn_text3.set("save")
    button_save3 = tk.Button(data_header, textvariable=btn_text3, font=("arial", 12),
                             bg=color1, fg=colorf, command=textbox_vars_head)
    button_save3.place(relx=.36, rely=0.890, relheight=0.06, relwidth=0.15, anchor="nw")

    def tb_clearall():
        global txt_pn_var, txt_elem_var, txt_material_var, txt_thickness_var, \
            txt_die_var, txt_hprep_var, txt_mh_var, txt_coating_var, txt_inspector_var, \
            txt_holesize_var, txt_hardness_var, txt_force_var, txt_tooling_var, txt_note_var
        global elem_direction

        txt_pn_var = ""
        txt_elem_var = ""
        txt_material_var = ""
        txt_thickness_var = ""
        txt_die_var = ""
        txt_mh_var = ""
        txt_hprep_var = ""
        txt_coating_var = ""
        txt_inspector_var = ""
        txt_holesize_var = ""
        txt_hardness_var = ""
        txt_force_var = ""
        txt_tooling_var = ""
        elem_direction = ""
        txt_note_var = ""
        txt_pn.delete(1.0, tk.END)
        txt_elem.delete(1.0, tk.END)
        txt_material.delete(1.0, tk.END)
        txt_thickness.delete(1.0, tk.END)
        txt_die.delete(1.0, tk.END)
        txt_mhmass.delete(1.0, tk.END)
        txt_holeprep.delete(1.0, tk.END)
        txt_coating.delete(1.0, tk.END)
        txt_inspector.delete(1.0, tk.END)
        txt_holesize.delete(1.0, tk.END)
        txt_hardness.delete(1.0, tk.END)
        txt_force.delete(1.0, tk.END)
        txt_tooling.delete(1.0, tk.END)
        txt_notehead.delete(1.0, tk.END)
        rb_direction_variable.set(6)

    button_clearall = tk.Button(data_header, text="clear all", font=("arial", 12),
                                bg=color1, fg=colorf, command=tb_clearall)
    button_clearall.place(relx=.205, rely=0.89, relheight=0.06, relwidth=0.15, anchor="nw")

    def focus_next_widget(event):
        event.widget.tk_focusNext().focus()
        return "break"
    txt_pn.bind("<Tab>", focus_next_widget)
    txt_elem.bind("<Tab>", focus_next_widget)
    txt_material.bind("<Tab>", focus_next_widget)
    txt_thickness.bind("<Tab>", focus_next_widget)
    txt_die.bind("<Tab>", focus_next_widget)
    txt_mhmass.bind("<Tab>", focus_next_widget)
    txt_holeprep.bind("<Tab>", focus_next_widget)
    txt_coating.bind("<Tab>", focus_next_widget)
    txt_inspector.bind("<Tab>", focus_next_widget)
    txt_holesize.bind("<Tab>", focus_next_widget)
    txt_hardness.bind("<Tab>", focus_next_widget)
    txt_force.bind("<Tab>", focus_next_widget)
    txt_tooling.bind("<Tab>", focus_next_widget)
    txt_notehead.bind("<Tab>", focus_next_widget)


    data_header.mainloop()
