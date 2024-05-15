"""
compare_graph.py

This module provides functionality to compare and visualize measurements from
different leak test sessions.It creates a graphical user interface (GUI) window using Tkinter,
allowing users to select and compare multiple measurement graphs side by side.

Key Functions:
- compare(leakware_id, mode_of_measurement, root, repository): Main function to create the
comparison window.
- comparison_graph(window, selected_index): Function to plot the selected measurement graphs.
- create_checkboxes(list_frame, compare_chart_frame): Function to create checkboxes for selecting
measurements.
- on_checkbox_change(window): Function to handle checkbox state changes and update the comparison
graph.
- load_data_from_database(repository, leakware_id): Function to load measurement data from the
database.

Dependencies:
- tkinter
- matplotlib.animation
- matplotlib.pyplot
- matplotlib.backends.backend_tkagg
- json

Usage:
This module is typically imported and the `compare` function is called when the user requests
to compare measurements from different leak test sessions.
"""
import tkinter as tk
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


### compare method
def compare(leakware_id, mode_of_measurement, root, repository):
    """
    Compares measurements for a given leakware ID.

    Args:
        leakware_id (int): The ID of the leakware.
        mode_of_measurement (str): The mode of measurement, e.g., "PEM".
        root: The root tkinter object.
        repository: An instance of the database repository.

    This function loads data from the database for the specified leakware ID.
    It creates a comparison window using tkinter, displaying checkboxes for each measurement.
    The user can select the measurements they want to compare, and the comparison graph is
    updated accordingly.
    """
    global element_listx
    global element_listy
    global checkboxes

    load_data_from_database(repository, leakware_id)

    checkboxes = []
    selected_index = []

    compare_window = tk.Toplevel(root)
    compare_window.title("Compare Measurements")
    if mode_of_measurement == "PEM":
        compare_window.iconbitmap("favicon.ico")
    compare_window.configure(background="white")
    compare_window.geometry("900x600")
    ### measurement list checkbox
    measurement_list_frame = tk.Frame(compare_window, bg="white")
    measurement_list_frame.place(relx=0.001, rely=0.15, relheight=0.7, relwidth=0.2, anchor="nw")
    ### show Graph
    compare_chart_frame = tk.Frame(compare_window, bg="white")
    compare_chart_frame.place(relx=0.2, rely=0.15, relheight=0.7, relwidth=0.8, anchor="nw")
    for i in range(len(element_listx)):
        selected_index.append(i)
    comparison_graph(compare_chart_frame, selected_index)
    checkboxes = create_checkboxes(measurement_list_frame, compare_chart_frame)

### Create Compare Graph
def comparison_graph(window, selected_index):
    """
    Displays a comparison graph based on selected measurements.

    Args:
        window: The tkinter window object where the graph will be displayed.
        selected_index (list): A list of indices representing the selected measurements.

    This function generates a comparison graph using Matplotlib and displays it in the provided
    tkinter window.
    The graph shows the course of measurements for the selected specimens.
    """
    global element_listx
    global element_listy
    global Checkboxes

    for widget in window.winfo_children():
        widget.destroy()

    fig3 = plt.figure(figsize=(10,7))
    compare_graph = fig3.add_subplot(1,1,1)

    compare_graph.clear()
    compare_graph.grid()
    compare_graph.set_title('Course of the measurements')
    compare_graph.set_yscale("symlog")
    compare_graph.set_xlabel("Time2 [s]")
    compare_graph.set_ylabel("Leakrate [mbarˑl/s]")

    i=0
    for element_no_in_listy in element_listy:
        element_no_in_listx = element_listx[i]
        if i in selected_index:
            i+=1
            compare_graph.plot(
                element_no_in_listx[:-1],
                element_no_in_listy[:-1],
                label="specimen " + str(i)
            )
        else:
            i+=1
    fig3.legend()

    canvas = FigureCanvasTkAgg(fig3, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

### Checkbox and onchange
def create_checkboxes(list_frame, compare_chart_frame):
    """
    Creates checkboxes for each specimen in a list frame.

    Args:
        list_frame: The tkinter frame where checkboxes will be placed.
        compare_chart_frame: The tkinter frame associated with the comparison chart.

    Returns:
        List of tkinter BooleanVar objects representing the checkboxes.

    This function generates checkboxes for each specimen in the element_listx list.
    It assigns a command to each checkbox to update the comparison chart when clicked.
    """
    global element_listx
    global element_listy
    global checkboxes
    colorf = "#ffffff"
    color1 = "#2049b0"

    if len(element_listx) > 0:
        for i in range(len(element_listx)):
            checkbox_var = tk.BooleanVar()
            checkbox = tk.Checkbutton(
                list_frame,
                text = f"specimen {i+1}",
                variable = checkbox_var,
                font=("arial"),
                anchor="nw",
                bg=colorf,
                fg=color1,
                command=lambda i=i, var=checkbox_var: on_checkbox_change(compare_chart_frame)
            )
            checkbox.pack() # Place the checkbox in the window
            checkbox.select()
            checkboxes.append(checkbox_var)
    return checkboxes

def on_checkbox_change(window):
    """
    Updates the comparison graph based on the selected checkboxes.

    Args:
        window: The tkinter window object.

    This function is called when the state of any checkbox in the UI changes.
    It updates the comparison graph based on the checkboxes that are currently selected.
    """
    global element_listx
    global checkboxes
    selected_index = []

    for i in range(len(element_listx)):
        selected_index.append(i)

    for index, checkbox in enumerate(checkboxes):
        if not checkbox.get():
            selected_index.remove(index)
    comparison_graph(window, selected_index)

def load_data_from_database(repository, leakware_id):
    """
    Loads data from the database for a specific leakware ID.

    Args:
        repository: An instance of the database repository.
        leakware_id (int): The ID of the leakware.

    This function retrieves all specimens associated with the provided leakware ID from
    the database.
    It parses the x and y values of each specimen from JSON format and populates the global
    lists element_listx and element_listy with these values.
    """
    global element_listx
    global element_listy

    element_listx = []
    element_listy = []
    specimens = repository.get_all_specimens(leakware_id)
    for specimen in specimens:
        element_listx.append(json.loads(specimen.x_value))
        element_listy.append(json.loads(specimen.y_value))
