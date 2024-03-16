import tkinter as tk
import serial

class pHInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("pH Interface")
        
        self.serial_port = serial.Serial('/dev/ttyACM0', 9600)  # Change '/dev/ttyACM0' to your Arduino port

        # pH Value label
        self.ph_label = tk.Label(root, text="pH Value:", font=("Helvetica", 14))
        self.ph_label.pack()

        # pH Value display
        self.ph_value = tk.Label(root, text="", font=("Helvetica", 18), fg="blue")
        self.ph_value.pack()

        # Refresh pH Value button
        self.refresh_button = tk.Button(root, text="Refresh", command=self.refresh_ph_value, font=("Helvetica", 12))
        self.refresh_button.pack(pady=10)

    def refresh_ph_value(self):
        if self.serial_port.isOpen():
            try:
                # Read data from Arduino
                data = self.serial_port.readline().decode().strip()
                if data.startswith("pH value:"):
                    ph_value = data.split(":")[1].strip()
                    self.ph_value.config(text=ph_value)
                else:
                    self.ph_value.config(text="Invalid data received")
            except serial.SerialException:
                self.ph_value.config(text="Error reading from serial port")
        else:
            self.ph_value.config(text="Serial port not open")

if __name__ == "__main__":
    root = tk.Tk()
    app = pHInterface(root)
    root.mainloop()
