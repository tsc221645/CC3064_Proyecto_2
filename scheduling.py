'''
This file contains the scheduling algorithms and their implementation for their simulation
'''
class Scheduler:

    def __init__(self,processes):
        self.processes = processes.copy
        self.timeline = []
        self.current_time = 0
        self.completed = []
        self.ready_queue
    
    def run(self):
        raise NotImplementedError("Subclasses must be implemented to work!")
    
    #Metrics calculation for the selected scheduling algorithm
    def calculate_metrics(self):
        if not self.completed:
            return {"avg_wait": 0, 
                    "avg_tat": 0, 
                    "avg_response":0}
        
        #Calculate waiting times
        total_wait = sum(p['wait_time']for p in self.completed)
        avg_wait = total_wait /len(self.completed)

        #Complete turnaround time (TAT) - total time to complete a task or process (inittiation to completion)
        for p in self.completed:
            p['tat'] = p['wait_time']+p['BT']
        total_tat = sum(p['tat'] for p in self.completed)
        avg_tat = total_tat / len(self.completed)

        #Response time calculation
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

#Implementation of FIFO Scheduling Algorithm ---------------------------------------------------------------------------------------
class FIFO(Scheduler):
    def run(self):
        #Order processes by arrival time -> Who arrives first is served first 
        self.process.sort(key=lambda x: x['AT'])
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