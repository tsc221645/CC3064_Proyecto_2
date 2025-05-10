'''
This file is used to implement the synchronization methods
It includes Mutex and Semaphore
'''
class SyncSimulator:
    def __init__(self, processes, resources, actions):
        self.processes = processes
        self.resources = {r['name']: r['count'] for r in resources}
        self.actions = sorted(actions, key=lambda x: x['cycle'])
        self.timeline = []
        self.current_cycle = 0
    
    def run(self):
        raise NotImplementedError("Must implement remaining subclasses")

# Mutex Implementation
class MutexSimulator(SyncSimulator):
    def __init__(self, processes, resources, actions):
        super().__init__(processes, resources, actions)
        self.locks = {name: False for name in self.resources.keys()} #Initialize all resource locks as unlocked

    def run(self):
        #Iterate through every action
        for action in self.actions:
            #System clock advances to the point the action must be executed
            while self.current_cycle < action['cycle']:
                self.current_cycle += 1

            #Extract relevant data
            pid = action['PID']
            resource = action['resource']
            raw_action = action['action'].upper()

            #Map action data
            if raw_action == "READ":
                action_type = "LOCK"
            elif raw_action == "WRITE":
                action_type = "UNLOCK"
            else:
                continue  # Ignore unknown actions

            #Lock the resource , process has to wait
            if action_type == "LOCK":
                if self.locks[resource]:
                    self.timeline.append({
                        'cycle': self.current_cycle,
                        'PID': pid,
                        'resource': resource,
                        'status': 'WAITING'
                    })
                else:
                    self.locks[resource] = True
                    self.timeline.append({
                        'cycle': self.current_cycle,
                        'PID': pid,
                        'resource': resource,
                        'status': 'LOCKED'
                    })
            # Unlock, ressource is now available
            elif action_type == "UNLOCK":
                if self.locks[resource]:
                    self.locks[resource] = False
                    self.timeline.append({
                        'cycle': self.current_cycle,
                        'PID': pid,
                        'resource': resource,
                        'status': 'UNLOCKED'
                    })
        #returns an event list with a cycle, process id, resource, and status
        return self.timeline

# Semaphore implementation
class SemaphoreSimulator(SyncSimulator):
    def run(self):
        #Initialize semaphores
        semaphores = {name: count for name, count in self.resources.items()}
        #iterate through all the actions
        for action in self.actions:
            #clock advances until the action occurs
            while self.current_cycle < action['cycle']:
                self.current_cycle += 1

            pid = action['PID']
            resource = action['resource']
            raw_action = action['action'].upper()

            #Map read and write
            if raw_action == "READ":
                action_type = "WAIT"
            elif raw_action == "WRITE":
                action_type = "SIGNAL"
            else:
                continue

            #action execution in case its wait
            if action_type == "WAIT":
                if semaphores[resource] > 0:
                    semaphores[resource] -= 1
                    self.timeline.append({
                        #event is registered in the timeline
                        'cycle': self.current_cycle,
                        'PID': pid,
                        'resource': resource,
                        'status': 'ACCESSED' #modifies to accessed if available
                    })
                else:
                    self.timeline.append({
                        #event is registered in the timeline
                        'cycle': self.current_cycle,
                        'PID': pid,
                        'resource': resource,
                        'status': 'WAITING' #else it is modified to waiting
                    })

            elif action_type == "SIGNAL":
                semaphores[resource] += 1
                #event is registered in the timeline
                self.timeline.append({
                    'cycle': self.current_cycle,
                    'PID': pid,
                    'resource': resource,
                    'status': 'RELEASED' #Resource is liberated and counter is increased
                })
        #returns list with cycle, process id, resource, and status
        return self.timeline
