'''
This file helps load the necessary files for the algorithms to function
There are 3 available functions for processes, resources and actions.
'''

#This function loads the processes file with the format <PID>, <BT>, <AT>, <Priority> and returns a dictionary list with the processes
def load_process_file(file_path):
    processes = [] #array with processes
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 4:
                    raise ValueError(f"Incorrect line format: {line}")
                
                pid = parts[0] #PID
                try:
                    bt = int(parts[1]) #BT
                    at = int(parts[2]) #AT
                    priority = int(parts[3]) #Priority
                except ValueError: 
                    raise ValueError(f"Invalid numerical values in line : {line}")
                
                #appends the process to the previously defined array
                processes.append({
                    "PID": pid,
                    "BT": bt,
                    "AT": at,
                    "Priority": priority
                })
    return processes

#This function loads the resources file with the format <Resource Name> <counter> and returns a dictionary with the resources
def load_resource_file(file_path):
    resources = [] #Array for the resources
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 2:
                    raise ValueError(f"Incorrect line format in the line: {line}")
                
                name = parts[0]
                try:
                    count = int(parts[1])
                except ValueError:
                    raise ValueError(f"Invalid counter in line : {line}")
                
                #Appends resource to previously defined array
                resources.append({
                    "name": name,
                    "count": count
                })
    return resources

#This function loads the action file with the format <PID>, <ACTION> <RESOURCE>, <CICLE> and returns a dictionary with the actions
def load_action_file(file_path):
    actions = [] #actions array
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 4:
                    raise ValueError(f"Incorrect line format in line: {line}")
                
                pid = parts[0]
                action = parts[1].upper()
                resource = parts[2]
                try:
                    cycle = int(parts[3])
                except ValueError:
                    raise ValueError(f"Invalid Cicle in line : {line}")
                
                if action not in ["READ", "WRITE", "LOCK", "UNLOCK", "WAIT", "SIGNAL"]:
                    raise ValueError(f"Non-recognized action: {action}")
                #appends action to previously defined array
                actions.append({
                    "PID": pid,
                    "action": action,
                    "resource": resource,
                    "cycle": cycle
                })
    return actions