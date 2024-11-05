# 01
from PIL import Image, ImageTk
import tkinter as tk
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# Define functions for start and stop buttons
def start_updates():
    pass

def stop_updates():
    pass

# Create main window
root = tk.Tk()
root.title("Mimosa Energy")
root.geometry("800x600")

# 02
# Paths for images
current_dir = os.path.dirname(os.path.abspath(__file__))
open_image_path = os.path.join(current_dir, "images/open.png")  # Adjust to match your file
close_image_path = os.path.join(current_dir, "images/close.png")  # Adjust to match your file

# Load and convert images
original_img_open = Image.open(open_image_path).resize((200, 200))  # Resize image to 200x200
original_img_closed = Image.open(close_image_path).resize((200, 200))  # Resize image to 200x200

plant_img_open = ImageTk.PhotoImage(original_img_open)
plant_img_closed = ImageTk.PhotoImage(original_img_closed)
# 03
# Display image
plant_label = tk.Label(root, image=plant_img_open)
plant_label.pack()
# 04
# Add welcome label
welcome_label = tk.Label(root, text="Welcome to the MIMOSA Energy Dashboard")
welcome_label.pack()

# Add start and stop buttons
start_button = tk.Button(root, text="Start", command=start_updates)
start_button.pack(side=tk.LEFT, padx=20)

stop_button = tk.Button(root, text="Stop", command=stop_updates)
stop_button.pack(side=tk.RIGHT, padx=20)
# 05
# Make the plant image interactive
def simulate_single_plant():
    plant_label.config(image=plant_img_closed)  # Change to closed plant image
    energy = (10 * random.random())  # Generate random energy value
    update_chart(energy)  # Update the chart with new energy value
    root.after(5000, lambda: plant_label.config(image=plant_img_open))  # Revert after 5 seconds

plant_label.bind("<Button-1>", lambda e: simulate_single_plant())
# 07
# Create a figure for the Matplotlib chart
fig, ax = plt.subplots()
ax.set_title('Energy Production (µW)')
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Energy (µW)')
ax.set_ylim(-10, 10)
line, = ax.plot([], [], lw=2)
# 08
# Function to create Matplotlib canvas
def create_canvas():
    global canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Call function to create canvas
create_canvas()

# Initialize data lists for real-time updates
time_data = []
energy_data = []
# 09
def update_chart(energy):
    global time_data, energy_data

    # Update data lists
    time_data.append(len(time_data))
    energy_data.append(energy)
    if len(time_data) > 10:
        time_data.pop(0)
        energy_data.pop(0)
    
    # Update plot data
    line.set_data(time_data, energy_data)
    ax.set_xlim(0, max(10, len(time_data)))
    canvas.draw()
# 10
# Ensure simulate_single_plant is updated to refresh chart correctly
plant_label.bind("<Button-1>", lambda e: simulate_single_plant())
# 06
# Run the Tkinter event loop
root.mainloop()
