import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from loadfile import load_process_file, load_resource_file, load_action_file
from scheduling import FIFO, SJF, SRT, RoundRobin, PriorityScheduling
from synchro import MutexSimulator, SemaphoreSimulator
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
        self.root.title("Simulador de Sistemas Operativos UVG 2025")
        self.root.geometry("1200x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Principal grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Side panel definition
        self.control_frame = ctk.CTkFrame(self.root)
        self.control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Select simulation type
        self.sim_type = ctk.CTkSegmentedButton(
            self.control_frame, 
            values=["Calendarización", "Sincronización"],
            command=self.change_simulation_type
        )

        #Setting default simultation type for scheduling
        self.sim_type.set("Calendarización")
        self.sim_type.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        
        # Algorithm configuration
        self.setup_scheduling_controls()
        self.setup_sync_controls()
        self.setup_file_controls()
        self.setup_action_buttons()
        
        # Viewing Area
        self.visualization_frame = ctk.CTkFrame(self.root)
        self.visualization_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Frame definition for metrics
        self.metrics_frame = ctk.CTkFrame(self.root)
        self.metrics_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0,10), sticky="ew")
        self.setup_metrics_display()

    #Setup the file controls
    def setup_file_controls(self):
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
        
        # Button to load processes -> only used in synchro mode
        self.load_resource_btn = ctk.CTkButton(
            self.file_frame, 
            text="Cargar Recursos",
            command=self.load_resource_file
        )
        self.load_resource_btn.pack(fill="x", pady=2)
        self.load_resource_btn.pack_forget()  # Hide
        
        # Button to load actions -> only used in synchro mode
        self.load_action_btn = ctk.CTkButton(
            self.file_frame, 
            text="Cargar Acciones",
            command=self.load_action_file
        )
        self.load_action_btn.pack(fill="x", pady=2)
        self.load_action_btn.pack_forget()  # Hide
        
        #Label for showing the loaded files, processes, resources, actions
        self.files_label = ctk.CTkLabel(
            self.control_frame,
            text="Archivos cargados:\n- Procesos: 0\n- Recursos: 0\n- Acciones: 0",
            justify="left"
        )
        self.files_label.grid(row=9, column=0, padx=5, pady=5, sticky="w", columnspan=2)
    
    #Setup action buttons for the GUI
    def setup_action_buttons(self):
        
        self.action_frame = ctk.CTkFrame(self.control_frame)
        self.action_frame.grid(row=10, column=0, padx=5, pady=(20,5), sticky="ew", columnspan=2)
        
        # Start simualtion button
        self.start_btn = ctk.CTkButton(
            self.action_frame,
            text="Iniciar Simulación",
            command=self.start_simulation,
            fg_color="green",
            hover_color="dark green"
        )
        self.start_btn.pack(fill="x", pady=2)
        
        # Pause button
        self.pause_btn = ctk.CTkButton(
            self.action_frame,
            text="Pausar",
            command=self.pause_simulation,
            state="disabled",
            fg_color="orange",
            hover_color="dark orange"
        )
        self.pause_btn.pack(fill="x", pady=2)
        
        # restart Button
        self.reset_btn = ctk.CTkButton(
            self.action_frame,
            text="Reiniciar",
            command=self.reset_simulation,
            fg_color="red",
            hover_color="dark red"
        )
        self.reset_btn.pack(fill="x", pady=2)
    
    #Metrics Display setup 
    def setup_metrics_display(self):
        
        self.metrics_label = ctk.CTkLabel(
            self.metrics_frame,
            text="Métricas:\n- Tiempo de espera promedio: -\n- Tiempo de retorno promedio: -\n- Tiempo de respuesta promedio: -",
            justify="left",
            font=("Arial", 12)
        )
        self.metrics_label.pack(side="left", padx=10, pady=5)

    #Scheduling control setup 
    def setup_scheduling_controls(self):
        self.algo_label = ctk.CTkLabel(self.control_frame, text="Algoritmo:")
        self.algo_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        #Algorithm selection
        self.algo_combobox = ctk.CTkComboBox(
            self.control_frame,
            values=["FIFO", "SJF", "SRT", "Round Robin", "Priority"]
        )
        self.algo_combobox.set("FIFO")
        self.algo_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.quantum_label = ctk.CTkLabel(self.control_frame, text="Quantum:")
        self.quantum_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.quantum_entry = ctk.CTkEntry(self.control_frame)
        self.quantum_entry.insert(0, "2")
        self.quantum_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    #Setup of Synchro controls
    def setup_sync_controls(self):
        self.sync_label = ctk.CTkLabel(self.control_frame, text="Mecanismo:")
        self.sync_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        #Mutex and Semathore options
        self.sync_combobox = ctk.CTkComboBox(
            self.control_frame,
            values=["Mutex", "Semaphore"]
        )
        self.sync_combobox.set("Mutex")
        self.sync_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Hide when default mode is scheduling
        self.sync_label.grid_remove()
        self.sync_combobox.grid_remove()

    # Setup Gantt Chart
    def setup_gantt_chart(self):
        self.figure, self.ax = plt.subplots(figsize=(10, 5))
        self.ax.set_title("Diagrama de Gantt") 
        self.ax.set_xlabel("Ciclos")
        self.ax.set_ylabel("Procesos")
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.visualization_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # Change simulation type
    def change_simulation_type(self, value):
        if value == "Calendarización":
            # Scheduling controls 
            self.algo_label.grid()
            self.algo_combobox.grid()
            self.quantum_label.grid()
            self.quantum_entry.grid()
            self.sync_label.grid_remove()
            self.sync_combobox.grid_remove()
            self.load_resource_btn.pack_forget()
            self.load_action_btn.pack_forget()
            
        else:
            # Show synchro controls
            self.sync_label.grid()
            self.sync_combobox.grid()
            
            #Hide scheduling controls
            self.algo_label.grid_remove()
            self.algo_combobox.grid_remove()
            self.quantum_label.grid_remove()
            self.quantum_entry.grid_remove()
            self.load_resource_btn.pack(fill="x", pady=2)
            self.load_action_btn.pack(fill="x", pady=2)

        self.update_files_label()
    
    #Load process file
    def load_process_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de procesos",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if file_path:
            try:
                self.processes = load_process_file(file_path)
                messagebox.showinfo("Éxito", f"Se cargaron {len(self.processes)} procesos")
                self.update_files_label()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
    
    #Load resource file
    def load_resource_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de recursos",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if file_path:
            try:
                self.resources = load_resource_file(file_path)
                messagebox.showinfo("Éxito", f"Se cargaron {len(self.resources)} recursos")
                self.update_files_label()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
    
    # Load action file
    def load_action_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de acciones",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if file_path:
            try:
                self.actions = load_action_file(file_path)
                messagebox.showinfo("Éxito", f"Se cargaron {len(self.actions)} acciones")
                self.update_files_label()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
    
    # Update the labels after loading the files 
    def update_files_label(self):
        text = "Archivos cargados:\n"
        text += f"- Procesos: {len(self.processes)}\n"
        
        if self.sim_type.get() == "Sincronización":
            text += f"- Recursos: {len(self.resources)}\n"
            text += f"- Acciones: {len(self.actions)}"
        
        self.files_label.configure(text=text)
    
    # Start simulation
    def start_simulation(self):
        if self.simulation_running:
            return
            
        sim_type = self.sim_type.get()
        
        if sim_type == "Calendarización":
            if not self.processes:
                messagebox.showwarning("Advertencia", "Debe cargar procesos primero") #show warning when processes are not loaded
                return
                
            self.run_scheduling_simulation()
        else:
            if not self.processes or not self.resources or not self.actions:
                messagebox.showwarning("Advertencia", "Debe cargar procesos, recursos y acciones primero") #show warning when the things are not loaded lol
                return
                
            self.run_sync_simulation()
    
    # Run scheduling simulation 
    def run_scheduling_simulation(self):
        algorithm = self.algo_combobox.get()
        quantum = None
        
        # In case of selecting Round Robin
        if algorithm == "Round Robin":
            try:
                quantum = int(self.quantum_entry.get())
                if quantum <= 0:
                    raise ValueError("Quantum debe ser positivo") # warning in case quantum is entered as negative
            except ValueError:
                messagebox.showerror("Error", "Quantum debe ser un número entero positivo") #Warning lol
                return
        
        # Create instance of selected algorithm
        if algorithm == "FIFO":
            scheduler = FIFO(self.processes)
        elif algorithm == "SJF":
            scheduler = SJF(self.processes)
        elif algorithm == "SRT":
            scheduler = SRT(self.processes)
        elif algorithm == "Round Robin":
            scheduler = RoundRobin(self.processes, quantum)
        elif algorithm == "Priority":
            scheduler = PriorityScheduling(self.processes)
        
        # Execute in separated threads
        self.simulation_thread = threading.Thread(
            target=self.execute_scheduling,
            args=(scheduler,),
            daemon=True
        )
        self.simulation_running = True
        self.start_btn.configure(state="disabled")
        self.pause_btn.configure(state="normal")
        self.simulation_thread.start()

    # Show simulation animation for dinamic gantt diagram
    def animate_simulation(self, timeline):
        def animate():
            self.ax.clear()
            self.ax.set_title("Diagrama de Gantt (Dinámico)")
            self.ax.set_xlabel("Ciclos")
            self.ax.set_ylabel("Procesos")
            self.ax.grid(True)

            if not timeline:
                self.canvas.draw()
                return

            # Unique processes
            processes = sorted(list({t['PID'] for t in timeline}))
            y_ticks = range(len(processes))
            self.ax.set_yticks(y_ticks)
            self.ax.set_yticklabels(processes)

            # Color per process
            colors = plt.cm.tab20.colors
            color_map = {pid: colors[i % len(colors)] for i, pid in enumerate(processes)}

            # Diagram drawing
            current_end = 0
            for segment in timeline:
                pid = segment['PID']
                start = segment['start']
                end = segment['end']
                duration = end - start
                y = processes.index(pid)

                for tick in range(start, end):
                    self.ax.clear()
                    self.ax.set_title(f"Diagrama de Gantt (Ciclo {tick})")
                    self.ax.set_xlabel("Ciclos")
                    self.ax.set_ylabel("Procesos")
                    self.ax.grid(True)
                    self.ax.set_yticks(y_ticks)
                    self.ax.set_yticklabels(processes)

                    # Painting the current cicle
                    for s in timeline:
                        if s['start'] >= tick:
                            continue
                        s_pid = s['PID']
                        s_start = s['start']
                        s_end = min(tick, s['end'])
                        s_y = processes.index(s_pid)
                        self.ax.broken_barh([(s_start, s_end - s_start)], (s_y - 0.4, 0.8),
                                            facecolors=color_map[s_pid], edgecolor='black')

                    self.ax.set_xlim(0, max(t['end'] for t in timeline) + 1)
                    self.canvas.draw()
                    self.root.update()
                    time.sleep(0.2)

            # Final Gant Diagram
            self.ax.clear()
            self.ax.set_title("Diagrama de Gantt")
            self.ax.set_xlabel("Ciclos")
            self.ax.set_ylabel("Procesos")
            self.ax.grid(True)
            self.ax.set_yticks(y_ticks)
            self.ax.set_yticklabels(processes)
            for segment in timeline:
                pid = segment['PID']
                start = segment['start']
                duration = segment['end'] - start
                y = processes.index(pid)
                self.ax.broken_barh([(start, duration)], (y - 0.4, 0.8),
                                    facecolors=color_map[pid], edgecolor='black')
            self.ax.set_xlim(0, max(t['end'] for t in timeline) + 1)
            self.canvas.draw()

        # Execute in separated thread to avoid freezing the UI
        threading.Thread(target=animate, daemon=True).start()

    def execute_scheduling(self, scheduler):
        #Executes in a separated thread
        try:
            # Execute simultation
            timeline, metrics = scheduler.run()
            
            # Refresh the interface of the main thread
            self.root.after(0, lambda: self.display_results(timeline, metrics))
            self.root.after(0, lambda: self.animate_simulation(timeline))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error en simulación:\n{str(e)}"))
        finally:
            self.root.after(0, lambda: self.simulation_finished())

    #Run synchro simulation
    def run_sync_simulation(self):
        mechanism = self.sync_combobox.get()
        
        if mechanism == "Mutex":
            simulator = MutexSimulator(self.processes, self.resources, self.actions)
        else:
            simulator = SemaphoreSimulator(self.processes, self.resources, self.actions)
        
        # Execute in a separate thread
        self.simulation_thread = threading.Thread(
            target=self.execute_sync,
            args=(simulator,),
            daemon=True
        )
        self.simulation_running = True
        self.start_btn.configure(state="disabled")
        self.pause_btn.configure(state="normal")
        self.simulation_thread.start()
    
    #Execute synchro
    def execute_sync(self, simulator):
        # Execute synchronization and show results
        timeline = simulator.run()
        
        # Update results in UI
        self.root.after(0, lambda: self.display_sync_results(timeline))
        self.root.after(0, lambda: self.animate_sync_simulation(timeline))
        self.root.after(0, lambda: self.simulation_finished())
    
    def pause_simulation(self):
        #pending implementation
        pass
    
    #Reset simultation after generating chart or loading processes
    def reset_simulation(self):
        if self.simulation_running:
            messagebox.showwarning("Advertencia", "Detenga la simulación actual primero")
            return
            
        self.processes = []
        self.resources = []
        self.actions = []
        self.update_files_label()
        self.clear_visualization()
        self.metrics_label.configure(
            text="Métricas:\n- Tiempo de espera promedio: -\n- Tiempo de retorno promedio: -\n- Tiempo de respuesta promedio: -"
        )
    
    #Finished simulation
    def simulation_finished(self):
        self.simulation_running = False
        self.start_btn.configure(state="normal")
        self.pause_btn.configure(state="disabled")
    
    #Show metrics as results in the UI
    def display_results(self, timeline, metrics):
        self.metrics_label.configure(
            text=f"Métricas:\n"
                 f"- Tiempo de espera promedio: {metrics['avg_wait']:.2f}\n"
                 f"- Tiempo de retorno promedio: {metrics['avg_tat']:.2f}\n"
                 f"- Tiempo de respuesta promedio: {metrics['avg_response']:.2f}"
        )
    
    #shows synchro results for the cycles, process id, status, and resource
    def display_sync_results(self, timeline):
        resumen = "Acciones registradas:\n"
        for event in timeline:
            resumen += f"- Ciclo {event['cycle']}: {event['PID']} {event['status']} {event['resource']}\n"
        
        messagebox.showinfo("Resumen de sincronización", resumen)

    # Animation of the sycnrho simulation
    def animate_sync_simulation(self, timeline):
        def animate():
            self.ax.clear()
            self.ax.set_title("Simulación de Sincronización")
            self.ax.set_xlabel("Ciclos")
            self.ax.set_ylabel("Procesos")
            self.ax.grid(True)

            if not timeline:
                self.canvas.draw()
                return

            # Obtaining unique processes
            processes = sorted(list({t['PID'] for t in timeline}))
            y_ticks = range(len(processes))
            self.ax.set_yticks(y_ticks)
            self.ax.set_yticklabels(processes)

            # Colors defined by state
            status_colors = {
                "WAITING": "orange",
                "LOCKED": "red",
                "UNLOCKED": "green",
                "ACCESSED": "blue",
                "RELEASED": "purple"
            }

            for i, event in enumerate(timeline):
                pid = event['PID']
                cycle = event['cycle']
                status = event['status']
                y = processes.index(pid)

                self.ax.scatter(cycle, y, color=status_colors.get(status, "gray"), s=100, label=f"{pid}-{status}")

                self.ax.set_xlim(0, max(e['cycle'] for e in timeline) + 1)
                self.canvas.draw()
                self.root.update()
                time.sleep(0.2)

            # Leyend without duplicates
            handles, labels = self.ax.get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            self.ax.legend(by_label.values(), by_label.keys(), title="Eventos")

            self.canvas.draw()

        threading.Thread(target=animate, daemon=True).start()

    # clear visualization removes what has been painted
    def clear_visualization(self):
        self.ax.clear()
        self.ax.set_title("Diagrama de Gantt")
        self.ax.set_xlabel("Ciclos")
        self.ax.set_ylabel("Procesos")
        self.ax.grid(True)
        self.canvas.draw()

if __name__ == "__main__":
    root = ctk.CTk()
    app = SchedulingSimulatorApp(root)
    root.mainloop()