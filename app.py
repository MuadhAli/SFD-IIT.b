import tkinter as tk
from tkinter import messagebox
import serial as sr
from matplotlib.figure import Figure  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  
import csv


class pHInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("pH Interface")
        
        self.serial_port = sr.Serial('/dev/ttyACM0', 9600)  # Change '/dev/ttyACM0' to your Arduino port
        self.serial_port.flushInput()

        # Frame for pH Value display
        self.ph_frame = tk.Frame(root)
        self.ph_frame.pack()

        self.label = tk.Label(self.ph_frame, text="pH Value:", font=("Helvetica", 12))
        self.label.pack(side=tk.LEFT, padx=5)

        self.ph_value_label = tk.Label(self.ph_frame, text="", font=("Helvetica", 12), fg="blue")
        self.ph_value_label.pack(side=tk.LEFT)

        # Milk button
        self.milk_button = tk.Button(root, text="Check Milk", command=self.check_milk, font=("Helvetica", 12), bg="lightblue", padx=10, pady=5)
        self.milk_button.pack(pady=10)

        # Chicken button
        self.chicken_button = tk.Button(root, text="Check Chicken", command=self.check_chicken, font=("Helvetica", 12), bg="lightgreen", padx=10, pady=5)
        self.chicken_button.pack()

        # Create a plot for pH values over time
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.plot = self.fig.add_subplot(111)
        self.plot.set_xlabel('Time')
        self.plot.set_ylabel('pH Value')
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # Initialize lists to store time and pH values
        self.time_values = []
        self.ph_values = []

        # File name for CSV logging
        self.csv_filename = "pH_log.csv"

        # Update plot and log pH values every second
        self.root.after(1000, self.update_plot_and_log)

    def update_plot_and_log(self):
        # Read pH value from Arduino
        ph_value = self.get_ph_value()
        if ph_value is not None:  # Check if ph_value is not None
            self.time_values.append(len(self.time_values))
            self.ph_values.append(float(ph_value))

            # Log pH value to CSV file
            self.log_to_csv(len(self.time_values), float(ph_value))

            # Plot pH values over time
            self.plot.clear()
            self.plot.plot(self.time_values, self.ph_values, marker='o', linestyle='-')
            self.plot.set_xlabel('Time')
            self.plot.set_ylabel('pH Value')
            self.canvas.draw()

        # Update plot and log every second
        self.root.after(1000, self.update_plot_and_log)
            
    def log_to_csv(self, time, ph_value):
        with open(self.csv_filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([time, ph_value])

    def check_milk(self):
        ph_value = self.get_ph_value()
        if ph_value is not None:
            ph_value = float(ph_value)
            milk_window = tk.Toplevel(self.root)
            milk_window.title("Milk Result")

            result = f"pH Value: {ph_value}\n\n"
            if 7.1 >= ph_value >= 6.4:
                result += "The milk is fresh and safe to consume."
            else:
                result += "The milk is not fresh and should not be consumed."

            result_label = tk.Label(milk_window, text=result, font=("Helvetica", 12))
            result_label.pack(padx=20, pady=20)
        else:
            messagebox.showwarning("Warning", "No pH value available. Check connection to Arduino.")


    def check_chicken(self):
        ph_value = self.get_ph_value()
        if ph_value is not None:
            ph_value = float(ph_value)
            chicken_window = tk.Toplevel(self.root)
            chicken_window.title("Chicken Result")

            result = f"pH Value: {ph_value}\n\n"
            if 6.6 >= ph_value >= 5.1:
                result += "The chicken is fresh and safe to consume."
            elif ph_value < 5:
                result += "The chicken is acidic and should not be consumed."
            elif ph_value > 6.8:
                result += "The chicken is basic and should not be consumed."
            else:
                result += "The chicken is not fresh and should not be consumed."

            result_label = tk.Label(chicken_window, text=result, font=("Helvetica", 12))
            result_label.pack(padx=20, pady=20)
        else:
            messagebox.showwarning("Warning", "No pH value available. Check connection to Arduino.")


    def get_ph_value(self):
        if self.serial_port.inWaiting() > 0:
            try:
                ph_reading = self.serial_port.readline().decode().strip()
                self.ph_value_label.config(text=ph_reading, fg="blue")
                
                # Check if the received string contains "pH value:"
                if "pH value:" in ph_reading:
                    return float(ph_reading.split(":")[1].strip())  # Extract pH value from the received string
                else:
                    print("Received string does not contain pH value")
                    return None
            except (UnicodeDecodeError, ValueError):
                print("Error reading pH value")
                return None
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = pHInterface(root)
    root.mainloop()
