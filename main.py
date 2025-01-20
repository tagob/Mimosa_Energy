# 01: Import necessary libraries
from PIL import Image, ImageTk
import tkinter as tk
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# Constants for energy levels and update intervals
BASELINE_ENERGY = 0.5  # Baseline energy level in µW
SPIKE_ENERGY = 1.5     # Energy spike level in µW
UPDATE_INTERVAL = 1000  # Interval in ms for live updates


# 02: Initialize main window
root = tk.Tk()
root.title("Mimosa Energy")
root.geometry("800x600")

# 01: Add a Canvas and Scrollbar to make the window scrollable
canvas_frame = tk.Frame(root)
canvas_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(canvas_frame)
scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a frame for all content inside the canvas
content_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# Update the scroll region when content is added
def update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

content_frame.bind("<Configure>", update_scroll_region)


# 03: Define paths for open and closed plant images
current_dir = os.path.dirname(os.path.abspath(__file__))
open_image_path = os.path.join(current_dir, "images/open.png")
close_image_path = os.path.join(current_dir, "images/close.png")

# Load, resize, and convert images for display
plant_img_open = ImageTk.PhotoImage(Image.open(open_image_path).resize((200, 200)))
plant_img_closed = ImageTk.PhotoImage(Image.open(close_image_path).resize((200, 200)))

# Display initial plant image in a label
plant_label = tk.Label(root, image=plant_img_open)
plant_label.pack()

# 04: Welcome label at the top
welcome_label = tk.Label(root, text="Welcome to the MIMOSA Energy Dashboard")
welcome_label.pack()

# 10: Function to simulate sensor data
def get_sensor_data():
    # Simulate sensor data for energy production
    return random.uniform(BASELINE_ENERGY, SPIKE_ENERGY)

# 05: Create figure and axis for Matplotlib chart
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Configure plot limits and styling
ax.set_title('Energy Production (µW)', color='blue')
ax.set_xlabel('Time (seconds)', color='green')
ax.set_ylabel('Energy (µW)', color='green')
ax.set_ylim(0, 2)  # Y-axis limit from 0 to 2 µW
ax.grid(True, which='both', linestyle='--', linewidth=0.5)  # Add grid lines for better readability

# Initialize plot line and data lists
line, = ax.plot([], [], lw=2, color='red', label='Energy Production')  # Add label for legend
ax.legend(loc='upper right')  # Add legend to the chart

# Initialize data lists for time and energy
time_data = []
energy_data = []


# 06: Function to update chart with new energy value
def update_chart():
    global time_data, energy_data, current_energy, last_annotation
    time_data.append(len(time_data))  # Append time as length of time_data
    energy_data.append(current_energy)  # Append current energy value

    # Keep only the last 60 seconds of data
    if len(time_data) > 60:
        time_data, energy_data = time_data[-60:], energy_data[-60:]

    # Update line data and redraw chart
    line.set_data(range(len(time_data)), energy_data)
    ax.set_xlim(0, 60)  # Ensure x-axis is fixed

    # If there is an active annotation, remove it
    if 'last_annotation' in globals() and last_annotation:
        last_annotation.remove()

    # Add or update annotation only for energy spikes above baseline
    if current_energy > BASELINE_ENERGY:
        y_offset = 15 if current_energy < 1.5 else -15  # Adjust position based on energy level
        last_annotation = ax.annotate(f'{current_energy:.2f} µW',
                                      xy=(len(time_data)-1, current_energy),
                                      textcoords='offset points',
                                      xytext=(0, y_offset),
                                      ha='center',
                                      color='blue',
                                      fontsize=8,
                                      bbox=dict(boxstyle="round,pad=0.3", edgecolor="blue", facecolor="lightyellow"))
    else:
        last_annotation = None  # Clear the annotation when energy returns to baseline

    canvas.draw()


# Inside simulate_single_plant function (smooth energy decay in decay_to_baseline)
def simulate_single_plant():
    global current_energy
    plant_label.config(image=plant_img_closed)  # Change to closed plant image
    current_energy = SPIKE_ENERGY  # Immediate spike
    update_chart()  # Update chart with immediate spike

    # Inner function for decaying energy back to baseline
    def decay_to_baseline():
        global current_energy
        if current_energy > BASELINE_ENERGY:
            current_energy -= 0.05  # Smoother, slower decay
            update_chart()
            root.after(100, decay_to_baseline)
        else:
            current_energy = BASELINE_ENERGY  # Set back to baseline
            update_chart()
            plant_label.config(image=plant_img_open)  # Revert image to open

    root.after(100, decay_to_baseline)


# 07
# Function to simulate continuous energy readings
def live_update():
    global current_energy
    update_chart()  # Update chart with current energy
    if update_active:  # Check if updates are active
        root.after(UPDATE_INTERVAL, live_update)  # Schedule the next update
    else:
        current_energy = BASELINE_ENERGY  # Reset to baseline if stopped


# 08
# Function to simulate energy spike and decay
def simulate_single_plant():
    global current_energy
    plant_label.config(image=plant_img_closed)  # Change to closed plant image
    current_energy = SPIKE_ENERGY  # Immediate spike
    update_chart()  # Update chart with immediate spike

    # Inner function for decaying energy back to baseline
    def decay_to_baseline():
        global current_energy
        if current_energy > 0:
            current_energy -= 0.1  # Smooth decay to 0.0
            update_chart()
            root.after(100, decay_to_baseline)
        else:
            current_energy = BASELINE_ENERGY  # Finally set back to 0.5 µW
            update_chart()
            plant_label.config(image=plant_img_open)  # Revert image to open

    root.after(100, decay_to_baseline)

# Bind click event to plant image for spike simulation
plant_label.bind("<Button-1>", lambda e: simulate_single_plant())


# 09: Initialize energy level
current_energy = BASELINE_ENERGY
update_chart()  # Initial update to set base level

# 11: Function to display flow chart
def display_flow_chart():
    flow_chart = """
    Energy Production Flow Chart:
    1. Plant Movement Detected by Sensors
    2. Energy Spike Generated (1.5 µW)
    3. Energy Decay to Baseline (0.5 µW)
    4. Energy Stored in Battery or Flywheel
    5. Energy Utilization for Dashboard Visualization
    """
    flow_chart_label.config(text=flow_chart)

# Flow chart display button
flow_chart_button = tk.Button(root, text="Show Flow Chart", command=display_flow_chart)
flow_chart_button.pack()

# Flow chart label
flow_chart_label = tk.Label(root, text="")
flow_chart_label.pack()

# 12: Function to simulate flywheel mechanism
def simulate_flywheel():
    global flywheel_energy
    flywheel_energy += current_energy  # Add current energy to flywheel storage
    flywheel_energy_label.config(text=f"Flywheel Energy: {flywheel_energy:.2f} µW")
    root.after(UPDATE_INTERVAL, simulate_flywheel)

# Initialize flywheel energy storage
flywheel_energy = 0.0

# Flywheel energy label
flywheel_energy_label = tk.Label(root, text=f"Flywheel Energy: {flywheel_energy:.2f} µW")
flywheel_energy_label.pack()

# Start flywheel simulation
simulate_flywheel()

# 13: Function to update battery status
def update_battery_status():
    global battery_energy
    if current_energy > BASELINE_ENERGY:
        battery_energy += current_energy - BASELINE_ENERGY  # Charge battery with excess energy
    else:
        battery_energy = max(0, battery_energy - BASELINE_ENERGY + current_energy)  # Discharge battery to maintain baseline

    battery_energy_label.config(text=f"Battery Energy: {battery_energy:.2f} µW")
    root.after(UPDATE_INTERVAL, update_battery_status)

# Initialize battery energy storage
battery_energy = 0.0

# Battery energy label
battery_energy_label = tk.Label(root, text=f"Battery Energy: {battery_energy:.2f} µW")
battery_energy_label.pack()

# Start battery status updates
update_battery_status()

# 14
update_active = False  # Variable to control if updates are active

def start_updates():
    global update_active
    update_active = True  # Activate live updates
    live_update()  # Start live updates

def stop_updates():
    global update_active
    update_active = False  # Deactivate live updates

# Create Start and Stop buttons
start_button = tk.Button(root, text="Start", command=start_updates)
start_button.pack(side=tk.LEFT, padx=20)

stop_button = tk.Button(root, text="Stop", command=stop_updates)
stop_button.pack(side=tk.RIGHT, padx=20)


# 15: Multiple Plant Energy Production (100 Plants)

# Create a new figure and axis for the 100-plant chart
fig_100, ax_100 = plt.subplots()
canvas_100 = FigureCanvasTkAgg(fig_100, master=root)
canvas_100.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Configure plot limits and styling for 100 plants
ax_100.set_title('Energy Production from 100 Plants (µW)', color='blue')
ax_100.set_xlabel('Time (seconds)', color='green')
ax_100.set_ylabel('Energy (µW)', color='green')
ax_100.set_ylim(0, 200)  # Adjust y-axis limit to 0-200 µW for 100 plants
ax_100.grid(True, linestyle='--', linewidth=0.5)

# Initialize plot line and data lists for 100-plant simulation
line_100, = ax_100.plot([], [], lw=2, color='purple', label='100 Plants Energy Production')
ax_100.legend(loc='upper right')
time_data_100 = []
energy_data_100 = []

# 15: Function to start updates for 100-plant chart
def start_updates_100():
    global update_active_100
    update_active_100 = True  # Activate live updates for 100 plants
    live_update_100()  # Start live updates for 100 plants

def stop_updates_100():
    global update_active_100
    update_active_100 = False  # Deactivate live updates for 100 plants

# Create Start and Stop buttons for 100-plant simulation
start_button_100 = tk.Button(content_frame, text="Start 100 Plants", command=start_updates_100)
start_button_100.pack(side=tk.LEFT, padx=20)

stop_button_100 = tk.Button(content_frame, text="Stop 100 Plants", command=stop_updates_100)
stop_button_100.pack(side=tk.RIGHT, padx=20)


# 16: Function to update 100-plant chart
def update_chart_100():
    global time_data_100, energy_data_100, current_energy
    time_data_100.append(len(time_data_100))  # Append time as length of time_data_100
    energy_data_100.append(current_energy * 100)  # Append 100 times current energy

    # Keep only the last 60 seconds of data
    if len(time_data_100) > 60:
        time_data_100, energy_data_100 = time_data_100[-60:], energy_data_100[-60:]

    # Update line data and redraw 100-plant chart
    line_100.set_data(range(len(time_data_100)), energy_data_100)
    ax_100.set_xlim(0, 60)  # Ensure x-axis is fixed
    canvas_100.draw()

# 17: Function to display flow chart for 100 plants
def display_flow_chart_100():
    flow_chart_100 = """
    Energy Production Flow Chart for 100 Mimosa Plants:
    1. Plant Movements Detected by Sensors
    2. 100 Energy Spikes Generated (150 µW)
    3. Energy Decay to Baseline (50 µW)
    4. Energy Stored in Battery or Flywheel
    5. Energy Utilization for Dashboard Visualization
    """
    flow_chart_label_100.config(text=flow_chart_100)

# 18: Add button and label for 100-plant flow chart
flow_chart_button_100 = tk.Button(root, text="Show Flow Chart for 100 Plants", command=display_flow_chart_100)
flow_chart_button_100.pack()
flow_chart_label_100 = tk.Label(root, text="")
flow_chart_label_100.pack()




#last block
# Start main Tkinter loop
root.mainloop()

