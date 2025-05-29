'''
This file contains the scheduling algorithms and their implementation for their simulation
'''

class Scheduler:
    def __init__(self, processes):
        self.processes = processes.copy()
        self.timeline = []
        self.current_time = 0
        self.completed = []
        self.ready_queue = []
    
    def run(self):
        raise NotImplementedError("Debe implementarse en subclases")
    
    #Metrics calculation for the selected scheduling algorithm
    def calculate_metrics(self):
        if not self.completed:
            return {"avg_wait": 0, "avg_tat": 0, "avg_response": 0}
        
        # Calculate waiting times
        total_wait = sum(p['wait_time'] for p in self.completed)
        avg_wait = total_wait / len(self.completed)
        
        ##Complete turnaround time (TAT) - total time to complete a task or process (inittiation to completion)
        for p in self.completed:
            p['tat'] = p['wait_time'] + p['BT']
        total_tat = sum(p['tat'] for p in self.completed)
        avg_tat = total_tat / len(self.completed)
        
        # Response time calculation for first time it executes
        response_times = []
        for p in self.completed:
            first_exec = next((t for t in self.timeline if t['PID'] == p['PID']), None)
            if first_exec:
                response_time = first_exec['start'] - p['AT']
                p['response_time'] = max(0, response_time)
                response_times.append(p['response_time'])
        
        avg_response = sum(response_times) / len(response_times) if response_times else 0
        
        return {
            "avg_wait": avg_wait,
            "avg_tat": avg_tat,
            "avg_response": avg_response,
            "throughput": len(self.completed) / max(t['end'] for t in self.timeline) if self.timeline else 0
        }

#Implmentation of FIFO Scheduling Algorithm -----------------------------------------------------------------------------------------
#Executed in order of arrival without priority or interruption
class FIFO(Scheduler):
    def run(self):
        # Order processes by arrival time -> who arrives first is served first
        self.processes.sort(key=lambda x: x['AT'])
        timeline = []
        current_time = 0
        
        #Iterate through ordered processes
        for process in self.processes:
            # Calculate waiting time -> if process arrives after current time it gets assigned a waiting time of zero
            wait_time = max(0, current_time - process['AT'])
            process['wait_time'] = wait_time
            
            # Calculate execution time -> start time and end time
            start_time = max(current_time, process['AT'])
            end_time = start_time + process['BT']
            
            # Register to timeline (data used to generat our gantt chart)
            timeline.append({
                'PID': process['PID'],
                'start': start_time,
                'end': end_time
            })
            #Clock continues and marks the process as completed
            current_time = end_time
            self.completed.append(process)

        #Saves the timeline in the object and calculates metrics
        self.timeline = timeline
        return timeline, self.calculate_metrics()

#Shortest Job First Implementation -> Selects the one with the lowest burt time (BT) -------------------------------------------
#Process executes the process with the lowest execution time or burst time. Not interrupted
class SJF(Scheduler):
    def run(self):
        #Orders by arrival time and burst time
        self.processes.sort(key=lambda x: (x['AT'], x['BT']))
        remaining = self.processes.copy() #Copies the process list
        self.current_time = 0 #Clock time
        
        while remaining:
            # Get processs by arrival time
            arrived = [p for p in remaining if p['AT'] <= self.current_time]
            #Clock moves if there arent any processes yet
            if not arrived:
                self.current_time += 1
                continue
                
            # Select the shortest process -> Lowest burst time
            arrived.sort(key=lambda x: x['BT'])
            current = arrived[0]
            remaining.remove(current)
            
            # Calculate waiting time
            wait_time = max(0, self.current_time - current['AT'])
            current['wait_time'] = wait_time
            
            # Execute the process
            start_time = self.current_time
            self.current_time += current['BT']
            
            # Register event in the timeline
            self.timeline.append({
                'PID': current['PID'],
                'start': start_time,
                'end': self.current_time
            })
            
            #Mark process as completed
            self.completed.append(current)
        
        #Resturns the timeline tu be used to graph, and the metrics
        return self.timeline, self.calculate_metrics()

#Implementation de Shortest Remaining Time
#The process with the lowest remaining time is executed, interruption allowed
class SRT(Scheduler):
    def run(self):
        # Copies processes
        processes = [p.copy() for p in self.processes]
        processes.sort(key=lambda x: x['AT'])  # Orders by arrival time 
        
        remaining = processes.copy() # processes that havent finished executing
        current_time = 0
        current_process = None
        remaining_bt = {} #Remaining time b yid
        
        # Initialize remaining times of each process
        for p in processes:
            remaining_bt[p['PID']] = p['BT']
        
        while remaining:
            # Find the processes that have arrived
            arrived = [p for p in remaining if p['AT'] <= current_time]
            
            #In case none have arrived, the clock moves
            if not arrived:
                current_time += 1
                continue
                
            # Select the process with the shortest remaining time
            arrived.sort(key=lambda x: remaining_bt[x['PID']])
            next_process = arrived[0]
            
            # In case of context switch
            if current_process != next_process['PID']:
                if current_process is not None:
                    # Registrar el tiempo del proceso anterior
                    self.timeline[-1]['end'] = current_time
                
                # Register new process
                self.timeline.append({
                    'PID': next_process['PID'],
                    'start': current_time,
                    'end': current_time + 1  # has to be upgraded later in the timeline
                })
                current_process = next_process['PID']
            
            # Execute one cycle of the process
            remaining_bt[next_process['PID']] -= 1
            current_time += 1
            
            # Verify if the process has ended
            if remaining_bt[next_process['PID']] == 0:
                # Calcular tiempo de espera
                wait_time = (current_time - next_process['AT'] - next_process['BT'])
                next_process['wait_time'] = max(0, wait_time)
                
                # Change timeline
                self.timeline[-1]['end'] = current_time
                
                # Move process to completed
                self.completed.append(next_process)
                remaining.remove(next_process)
                current_process = None
        
        # Calculate metrics
        metrics = self.calculate_metrics()
        #Returns the timeline and the metrics
        return self.timeline, metrics
    
#Implementation of Round Robin -------------------------------------------------------------------------------------
#Process is assigned quantum or a time block
#if it hasnt finished, it is placed at the end of the tail
class RoundRobin(Scheduler):
    def __init__(self, processes, quantum):
        super().__init__(processes)
        self.quantum = quantum #defined quantum value
    
    def run(self):
        processes = [p.copy() for p in self.processes]
        processes.sort(key=lambda x: x['AT'])  # Order by arrival time
        
        remaining_bt = {p['PID']: p['BT'] for p in processes}
        ready_queue = []
        current_time = 0
        timeline_idx = -1  # Index of the last process in the timeline
        
        # Saves the remaining burst time for each process
        ready_queue = [p for p in processes if p['AT'] <= current_time] # process that can start because their arrival time is less or equal to zero
        remaining = [p for p in processes if p['AT'] > current_time] #havent arrived
        
        while ready_queue or remaining:
            if not ready_queue:
                current_time += 1
                # Verify if new processes have arrived
                new_arrivals = [p for p in remaining if p['AT'] <= current_time]
                ready_queue.extend(new_arrivals)
                for p in new_arrivals:
                    remaining.remove(p)
                continue
            
            # Select the next process
            current_process = ready_queue.pop(0)
            pid = current_process['PID']
            
            # FIFO - first in the line
            self.timeline.append({
                'PID': pid,
                'start': current_time,
                'end': current_time + min(self.quantum, remaining_bt[pid])
            })
            timeline_idx += 1
            
            # Execute by execution time and advance the real time and remaining time
            execution_time = min(self.quantum, remaining_bt[pid])
            remaining_bt[pid] -= execution_time
            current_time += execution_time
            
            # Verify arrival of other processes during the other  process executed
            new_arrivals = [
                p for p in remaining 
                if p['AT'] <= current_time and p['AT'] >= current_time - execution_time
            ]
            ready_queue.extend(new_arrivals)
            for p in new_arrivals:
                remaining.remove(p)
            
            # if the process has finished wait_time is calculated, else its set to waiting
            if remaining_bt[pid] > 0:
                ready_queue.append(current_process)
            else:
                # Calcular tiempo de espera
                wait_time = (current_time - current_process['AT'] - current_process['BT'])
                current_process['wait_time'] = max(0, wait_time)
                self.completed.append(current_process)
        
       #Merge processes
        self.merge_timeline_intervals()
        
        # Calculate metrics
        metrics = self.calculate_metrics()
        return self.timeline, metrics
    #For gantt chart uses, it groups the blocks when the same processes have been executed
    def merge_timeline_intervals(self):
        if not self.timeline:
            return
            
        merged = [self.timeline[0]]
        for current in self.timeline[1:]:
            last = merged[-1]
            if last['PID'] == current['PID'] and last['end'] == current['start']:
                # Fusionar intervalos contiguos
                merged[-1]['end'] = current['end']
            else:
                merged.append(current)
        self.timeline = merged

#Implementation of Priority Scheduling ------------------------------------------------------------------------------------------------
#Highest priority to lowest priority
class PriorityScheduling(Scheduler):
    def run(self):
        processes = [p.copy() for p in self.processes]
        processes.sort(key=lambda x: (x['AT'], x['Priority']))  #Order by arrival time and priority
        
        remaining_bt = {p['PID']: p['BT'] for p in processes}
        remaining = processes.copy()
        current_time = 0
        
        while remaining:
            # get processes
            arrived = [p for p in remaining if p['AT'] <= current_time]
            
            #Clock moves if no processes have arrived
            if not arrived:
                current_time += 1
                continue
                
            # Select the process with the highest priority, the lesser the number the higher the priority
            arrived.sort(key=lambda x: x['Priority'])
            current_process = arrived[0]
            
            # Register the execution
            self.timeline.append({
                'PID': current_process['PID'],
                'start': current_time,
                'end': current_time + current_process['BT']
            })
            
            # Time moves
            current_time += current_process['BT']
            
            # Calculate waiting time
            wait_time = max(0, self.timeline[-1]['start'] - current_process['AT'])
            current_process['wait_time'] = wait_time
            
            # Move to completed
            self.completed.append(current_process)
            remaining.remove(current_process)
        
        # Calculate metrics
        metrics = self.calculate_metrics()
        return self.timeline, metrics