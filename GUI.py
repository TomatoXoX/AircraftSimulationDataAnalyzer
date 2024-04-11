import tkinter as tk
from tkinter import filedialog, ttk, Canvas, Frame
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        data = pd.read_csv(file_path, delimiter=',')
        return data
    return None

def plot_data(data):
    # Clear previous figures if any
    for widget in frame_plots.winfo_children():
        widget.destroy()

    # Plot 1: 3D Flight Path
    fig_flight_path = Figure(figsize=(9, 8), dpi=100)
    ax_flight_path = fig_flight_path.add_subplot(111, projection='3d')
    x, y, z = data['X_{ECI} (ft)'], data['Y_{ECI} (ft)'], data['Altitude ASL (ft)']
    ax_flight_path.plot(x, y, z, linewidth=1.5)
    ax_flight_path.scatter(x.iloc[0], y.iloc[0], z.iloc[0], color='g', label='Start', s=50)
    ax_flight_path.scatter(x.iloc[-1], y.iloc[-1], z.iloc[-1], color='r', label='End', s=50)
    ax_flight_path.set_xlabel('X (ft)', fontsize=8)
    ax_flight_path.set_ylabel('Y (ft)', fontsize=8)
    ax_flight_path.set_zlabel('Z (ft)', fontsize=8)
    ax_flight_path.set_title('Flight Path', fontsize=10)
    ax_flight_path.legend()
    canvas_flight_path = FigureCanvasTkAgg(fig_flight_path, master=frame_plots)
    canvas_flight_path.draw()
    canvas_flight_path.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Altitude vs. Time
    fig_altitude = Figure(figsize=(5, 4), dpi=100)
    ax_altitude = fig_altitude.add_subplot(111)
    ax_altitude.plot(data['Time'], data['Altitude ASL (ft)'], linewidth=1.5)
    ax_altitude.set_xlabel('Time (s)', fontsize=8)
    ax_altitude.set_ylabel('Altitude (ft)', fontsize=8)
    ax_altitude.set_title('Altitude vs. Time', fontsize=10)
    canvas_altitude = FigureCanvasTkAgg(fig_altitude, master=frame_plots)
    canvas_altitude.draw()
    canvas_altitude.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Velocity vs. Time
    fig_velocity = Figure(figsize=(5, 4), dpi=100)
    ax_velocity = fig_velocity.add_subplot(111)
    ax_velocity.plot(data['Time'], data['V_{Total} (ft/s)'], linewidth=1.5)
    ax_velocity.set_xlabel('Time (s)', fontsize=8)
    ax_velocity.set_ylabel('Velocity (ft/s)', fontsize=8)
    ax_velocity.set_title('Velocity vs. Time', fontsize=10)
    canvas_velocity = FigureCanvasTkAgg(fig_velocity, master=frame_plots)
    canvas_velocity.draw()
    canvas_velocity.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Pitch, Roll, Yaw vs. Time
    fig_attitude = Figure(figsize=(5, 6), dpi=100)
    ax_pitch = fig_attitude.add_subplot(311)
    ax_roll = fig_attitude.add_subplot(312)
    ax_yaw = fig_attitude.add_subplot(313)
    ax_pitch.plot(data['Time'], data['Theta (deg)'], linewidth=1.5)
    ax_roll.plot(data['Time'], data['Phi (deg)'], linewidth=1.5)
    ax_yaw.plot(data['Time'], data['Psi (deg)'], linewidth=1.5)
    for ax, label in zip([ax_pitch, ax_roll, ax_yaw], ['Pitch (deg)', 'Roll (deg)', 'Yaw (deg)']):
        ax.set_xlabel('Time (s)', fontsize=8)
        ax.set_ylabel(label, fontsize=8)
        ax.grid(True)
    fig_attitude.suptitle('Pitch, Roll, and Yaw vs. Time', fontsize=10)
    fig_attitude.tight_layout(rect=[0, 0, 1, 0.95])
    canvas_attitude = FigureCanvasTkAgg(fig_attitude, master=frame_plots)
    canvas_attitude.draw()
    canvas_attitude.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def load_and_plot():
    data = load_data()
    if data is not None:
        plot_data(data)

def main():
    global root, frame_plots
    root = tk.Tk()
    root.title("Aircraft Simulation Analyzer")
    root.geometry("1200x900")

    style = ttk.Style()
    style.theme_use('clam')

    # Frame for buttons
    frame_controls = ttk.Frame(root)
    frame_controls.pack(fill=tk.X, padx=10, pady=10)

    # Button to load data and display plots
    btn_load = ttk.Button(frame_controls, text="Load Data and Plot", command=load_and_plot)
    btn_load.pack(side=tk.LEFT, padx=10, pady=10)

    # Frame for plotting with a scrollbar
    canvas = Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    frame_plots = scrollable_frame

    root.mainloop()

if __name__ == "__main__":
    main()