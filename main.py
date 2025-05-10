import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from loadfile import load_process_file, load_resource_file, load_action_file
from scheduling import FIFO
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time

'''
This file is mainly for the GUI 
It also imports the already implemented algorithms from scheduling.py and synchro.py
All imports here are used for rendering the GUI
'''

class SchedulingSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.setup_gantt_chart()
        self.processes = []
        self.resources = []
        self.actions = []
        self.simulation_running = False
    
    #initial ui and window setup
    def setup_ui(self):
        self.root.title("Sistemas Operativos - Simulador")
        self.root.geometry("1200x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        #principal grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        #side panel definition
        self.control_frame = ctk.CTkFrame(self.root)
        self.control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        #Select simulation type
        self.sim_type = ctk.CTkSegmentedButton(
            self.control_frame, 
            values=["Calendarización", "Sincronización"],
            command=self.change_simulation_type
        )
        #default simulation type
        self.sim_type.set("Calendarización")
        self.sim_type.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        
        # configuration
        self.setup_scheduling_controls()
        self.setup_sync_controls()
        self.setup_file_controls()
        self.setup_action_buttons()
        
        # Viewing area
        self.visualization_frame = ctk.CTkFrame(self.root)
        self.visualization_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Show metrics fram definition
        self.metrics_frame = ctk.CTkFrame(self.root)
        self.metrics_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0,10), sticky="ew")
        self.setup_metrics_display()

        #Setup the file controls
        def setup_fle_controls(self):
            # Frame for the file controls
            self.file_frame = ctk.CTkFrame(self.control_frame)
            self.file_frame.grid(row=8, column=0, padx=5, pady=(20,5), sticky="ew", columnspan=2)
            
            # Load processes file
            self.load_process_btn = ctk.CTkButton(
                self.file_frame, 
                text="Cargar Procesos",
                command=self.load_process_file
            )
            self.load_process_btn.pack(fill="x", pady=2)
            
            # Button to load processe -> only used in synchro mode
            self.load_resource_btn = ctk.CTkButton(
                self.file_frame, 
                text="Cargar Recursos",
                command=self.load_resource_file
            )
            self.load_resource_btn.pack(fill="x", pady=2)
            self.load_resource_btn.pack_forget()  #Hidden initially
            
            # Button to load actions -> only used in synchro mode
            self.load_action_btn = ctk.CTkButton(
                self.file_frame, 
                text="Cargar Acciones",
                command=self.load_action_file
            )
            self.load_action_btn.pack(fill="x", pady=2)
            self.load_action_btn.pack_forget() #Hidden Initially
            
            # Shows loaded files and amount of each category
            self.files_label = ctk.CTkLabel(
                self.control_frame,
                text="Archivos cargados:\n- Procesos: 0\n- Recursos: 0\n- Acciones: 0",
                justify="left"
            )
            self.files_label.grid(row=9, column=0, padx=5, pady=5, sticky="w", columnspan=2)


        


if __name__ == "__main__":
    root = ctk.CTk()
    app = SchedulingSimulatorApp(root)
    root.mainloop()