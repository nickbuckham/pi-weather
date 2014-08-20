import os
import glob
import time
import Tkinter as tk

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

class Data(object):
    def read_temp_raw(self):
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f

class Display(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.data = Data()
        self.canvas = tk.Canvas(self, background="black")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.c_line = self.canvas.create_line(0, 0, 0, 0, fill="red")
        self.f_line = self.canvas.create_line(0, 0, 0, 0, fill="blue")
        self.update_plot()

    def update_plot(self):
        c = self.data.read_temp()[0]
        f = self.data.read_temp()[1]
        self.add_point(self.c_line, c)
        self.add_point(self.f_line, f)
        self.canvas.xview_moveto(1.0)
        self.after(100, self.update_plot)

    def add_point(self, line, y):
        coords = self.canvas.coords(line)
        x = coords[-2] + 1
        coords.append(x)
        coords.append(y)
        coords = coords[-200:]
        self.canvas.coords(line, *coords)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    Display(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
