import tkinter as tk
from tkinter import ttk
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time

esp32_ip = "192.168.1.100"  # Replace with the IP address of your ESP32

# Initialize lists for storing data
time_data = []
temperature_data = []
humidity_data = []
mq2_data = []
mq3_data = []
digital_data = []

def update_data():
    try:
        response = requests.get(f"http://{esp32_ip}/")
        if response.status_code == 200:
            sensor_data = response.text.strip().split(',')
            for data in sensor_data:
                sensor, value = data.split(':')
                if sensor == "T":
                    temperature_data.append(float(value))
                elif sensor == "H":
                    humidity_data.append(float(value))
                elif sensor == "MQ2":
                    mq2_data.append(float(value))
                elif sensor == "MQ3":
                    mq3_data.append(float(value))
                elif sensor == "D":
                    digital_data.append(int(value))
            
            # Add current time to time_data
            time_data.append(time.strftime("%H:%M:%S"))

            # Update plots
            temperature_plot.clear()
            temperature_plot.plot(time_data, temperature_data, label='Temperature (°C)')
            temperature_plot.legend()
            temperature_canvas.draw()

            humidity_plot.clear()
            humidity_plot.plot(time_data, humidity_data, label='Humidity (%)')
            humidity_plot.legend()
            humidity_canvas.draw()

            mq2_plot.clear()
            mq2_plot.plot(time_data, mq2_data, label='MQ2')
            mq2_plot.legend()
            mq2_canvas.draw()

            mq3_plot.clear()
            mq3_plot.plot(time_data, mq3_data, label='MQ3')
            mq3_plot.legend()
            mq3_canvas.draw()

            digital_plot.clear()
            digital_plot.plot(time_data, digital_data, label='Digital')
            digital_plot.legend()
            digital_canvas.draw()
    except:
        pass
    
    root.after(1000, update_data)

root = tk.Tk()
root.title("ESP32 Sensor Data Receiver")

# Create tabs for different sensor plots
tab_control = ttk.Notebook(root)
temperature_tab = ttk.Frame(tab_control)
humidity_tab = ttk.Frame(tab_control)
mq2_tab = ttk.Frame(tab_control)
mq3_tab = ttk.Frame(tab_control)
digital_tab = ttk.Frame(tab_control)
tab_control.add(temperature_tab, text='Temperature')
tab_control.add(humidity_tab, text='Humidity')
tab_control.add(mq2_tab, text='MQ2')
tab_control.add(mq3_tab, text='MQ3')
tab_control.add(digital_tab, text='Digital')
tab_control.pack(expand=1, fill="both")

# Create temperature plot
temperature_fig = Figure(figsize=(5, 4), dpi=100)
temperature_plot = temperature_fig.add_subplot(111)
temperature_plot.set_xlabel('Time')
temperature_plot.set_ylabel('Temperature (°C)')
temperature_canvas = FigureCanvasTkAgg(temperature_fig, temperature_tab)
temperature_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create humidity plot
humidity_fig = Figure(figsize=(5, 4), dpi=100)
humidity_plot = humidity_fig.add_subplot(111)
humidity_plot.set_xlabel('Time')
humidity_plot.set_ylabel('Humidity (%)')
humidity_canvas = FigureCanvasTkAgg(humidity_fig, humidity_tab)
humidity_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create MQ2 plot
mq2_fig = Figure(figsize=(5, 4), dpi=100)
mq2_plot = mq2_fig.add_subplot(111)
mq2_plot.set_xlabel('Time')
mq2_plot.set_ylabel('MQ2')
mq2_canvas = FigureCanvasTkAgg(mq2_fig, mq2_tab)
mq2_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create MQ3 plot
mq3_fig = Figure(figsize=(5, 4), dpi=100)
mq3_plot = mq3_fig.add_subplot(111)
mq3_plot.set_xlabel('Time')
mq3_plot.set_ylabel('MQ3')
mq3_canvas = FigureCanvasTkAgg(mq3_fig, mq3_tab)
mq3_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create digital sensor plot
digital_fig = Figure(figsize=(5, 4), dpi=100)
digital_plot = digital_fig.add_subplot(111)
digital_plot.set_xlabel('Time')
digital_plot.set_ylabel('Digital')
digital_canvas = FigureCanvasTkAgg(digital_fig, digital_tab)
digital_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

update_data()  # Initial data update

root.mainloop()
