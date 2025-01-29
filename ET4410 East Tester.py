import tkinter as tk
from tkinter import ttk
import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sys

class ImpedanceAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Impedance Analyzer")
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a 'clam' theme for a more modern look
        self.create_widgets()
        self.setup_serial()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(6, weight=1)

        # Labels and Entry fields
        self.port_entry = self.create_label_and_entry(frame, "Port:", 0, 'COM14')
        self.baudrate_entry = self.create_label_and_entry(frame, "Baudrate:", 1, '9600')
        self.dc_bias_entry = self.create_label_and_entry(frame, "DC Bias (mV):", 2, '0')
        self.ac_level_entry = self.create_label_and_entry(frame, "AC Level (mV):", 3, '300')

        self.graph_type_label = ttk.Label(frame, text="Graph Type:")
        self.graph_type_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.graph_type = ttk.Combobox(frame, values=["Points", "Line"])
        self.graph_type.grid(row=4, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.graph_type.set("Points")

        self.start_button = ttk.Button(frame, text="Start", command=self.start_measurement)
        self.start_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.fig, self.axs = plt.subplots(1, 2, squeeze=False, figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        toolbar_frame = ttk.Frame(frame)
        toolbar_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E))
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_label_and_entry(self, frame, text, row, default_value):
        label = ttk.Label(frame, text=text)
        label.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        entry = ttk.Entry(frame)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        entry.insert(0, default_value)
        return entry

    def setup_serial(self):
        self.ser = None
        self.delay = 1
        self.frequencies = [100, 120, 200, 400, 800, 1000, 2000, 4000, 8000, 10000, 15000, 20000, 40000, 50000, 80000, 100000]
        self.freq = []
        self.medidas1 = []
        self.medidas2 = []

    def query(self, command):
        if self.ser:
            self.ser.write((command + '\n').encode())
            time.sleep(self.delay)
            response = self.ser.readline().decode().strip()
            print(f"Enviado: {command}, Recebido: {response}")
            return response
        else:
            print("Erro: Porta serial não está aberta.")
            return ""

    def write(self, command):
        if self.ser:
            self.ser.write((command + '\n').encode())
            time.sleep(self.delay)
        else:
            print("Erro: Porta serial não está aberta.")

    def start_measurement(self):
        try:
            port = self.port_entry.get()
            baudrate = int(self.baudrate_entry.get())
            dc_bias = int(self.dc_bias_entry.get())
            ac_level = int(self.ac_level_entry.get())
            graph_type = self.graph_type.get()

            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(self.delay)
            print(f"Porta serial {port} aberta com baudrate {baudrate}")

            idn = self.query("*IDN?")
            if not idn:
                print("Erro: Não foi possível obter resposta do comando *IDN?")
                return
            print(f"ID do dispositivo: {idn}")
            time.sleep(self.delay)

            self.write("SYSTEM:REMOTE")
            self.write("APERTURE FAST")
            self.write(f"BIAS:VOLTAGE {dc_bias}")
            self.write(f"VOLTAGE:LEVEL {ac_level}")
            self.write("FUNCTION:IMPEDANCE:A R")
            self.write("FUNCTION:IMPEDANCE:B THR")
            self.write("FUNCTION:IMPEDANCE:RANGE:AUTO ON")

            self.freq = []
            self.medidas1 = []
            self.medidas2 = []

            self.measure_and_plot(graph_type)
        except Exception as e:
            print(f"Erro durante a medição: {e}")
        finally:
            if self.ser:
                self.write("SYSTEM:LOCAL")
                self.ser.close()
                print("Porta serial fechada")

    def measure_and_plot(self, graph_type):
        for f in self.frequencies:
            self.write(f"FREQUENCY {f}")
            time.sleep(self.delay)
            print(f"{f} Hz")
            while True:
                values = self.query("FETCH?")
                if "exec success" in values or "cmd err" in values:
                    values = self.query("MEAS:IMP?")
                if not values or "cmd err" in values:
                    print(f"Erro: Não foi possível obter resposta válida para a frequência {f}. Tentando novamente...")
                    continue
                values = values.rstrip()
                print(f"Valores recebidos: {values}")
                try:
                    freql, freqr = values.split(",")
                    self.freq.append(float(f))
                    self.medidas1.append(float(freql))
                    self.medidas2.append(float(freqr))
                    self.update_plot(graph_type)
                    break
                except ValueError:
                    print(f"Erro ao processar os valores recebidos: {values}. Tentando novamente...")

    def update_plot(self, graph_type):
        self.axs[0, 0].cla()
        self.axs[0, 1].cla()

        if graph_type == "Points":
            self.axs[0, 0].loglog(self.freq, self.medidas1, 'r.')
            self.axs[0, 1].semilogx(self.freq, self.medidas2, 'r.')
        else:
            self.axs[0, 0].loglog(self.freq, self.medidas1, 'r-')
            self.axs[0, 1].semilogx(self.freq, self.medidas2, 'r-')

        self.axs[0, 0].set_title('Re{Z}')
        self.axs[0, 1].set_title('Theta')
        for ax in self.axs.flat:
            ax.set(xlabel='Frequency (Hz)', ylabel='Medida')
            ax.grid()

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImpedanceAnalyzerApp(root)
    root.mainloop()
