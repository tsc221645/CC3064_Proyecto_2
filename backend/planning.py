'''
In this file the planning algorithms will be defined for later usage
'''

from backend.loadfile import buildProcessesDF

#Fist In First Out
# backend/planning.py

def fifoPlanning(procesos):
    procesos_ordenados = sorted(procesos, key=lambda p: p["at"])
    tiempo_actual = 0
    gantt = []
    tiempos_espera = []

    for p in procesos_ordenados:
        if tiempo_actual < p["at"]:
            tiempo_actual = p["at"]
        tiempos_espera.append(tiempo_actual - p["at"])
        gantt.append({
            "pid": p["pid"],
            "start": tiempo_actual,
            "end": tiempo_actual + p["bt"]
        })
        tiempo_actual += p["bt"]

    avg_wait = sum(tiempos_espera) / len(procesos)
    return gantt, avg_wait



# Shortest Job First (SJF) - No preemptivo
def sjfPlanning(procesos):
    procesos = sorted(procesos, key=lambda p: (p["at"], p["bt"]))
    lista = procesos.copy()
    completados = []
    tiempo_actual = 0
    gantt = []
    tiempos_espera = []

    while lista:
        disponibles = [p for p in lista if p["at"] <= tiempo_actual]
        if not disponibles:
            tiempo_actual += 1
            continue
        proceso = min(disponibles, key=lambda p: p["bt"])
        lista.remove(proceso)
        tiempos_espera.append(tiempo_actual - proceso["at"])
        gantt.append({
            "pid": proceso["pid"],
            "start": tiempo_actual,
            "end": tiempo_actual + proceso["bt"]
        })
        tiempo_actual += proceso["bt"]
        completados.append(proceso)

    avg_wait = sum(tiempos_espera) / len(completados)
    return gantt, avg_wait


# Shortest Remaining Time First (SRTF) - Preemptivo
def srtfPlanning(procesos):
    import heapq
    procesos = sorted(procesos, key=lambda p: p["at"])
    lista = procesos.copy()
    gantt = []
    heap = []
    tiempo_actual = 0
    i = 0
    tiempos_espera = {}
    tiempo_restante = {}

    for p in lista:
        tiempo_restante[p["pid"]] = p["bt"]
        tiempos_espera[p["pid"]] = 0

    proceso_actual = None
    tiempo_inicio = None

    while i < len(lista) or heap or proceso_actual:
        while i < len(lista) and lista[i]["at"] <= tiempo_actual:
            p = lista[i]
            heapq.heappush(heap, (tiempo_restante[p["pid"]], p["at"], p["pid"], p))
            i += 1

        if not proceso_actual and heap:
            _, _, _, proceso_actual = heapq.heappop(heap)
            tiempo_inicio = tiempo_actual

        if proceso_actual:
            tiempo_restante[proceso_actual["pid"]] -= 1
            if tiempo_restante[proceso_actual["pid"]] == 0:
                gantt.append({
                    "pid": proceso_actual["pid"],
                    "start": tiempo_inicio,
                    "end": tiempo_actual + 1
                })
                tiempos_espera[proceso_actual["pid"]] = (tiempo_actual + 1 - proceso_actual["at"] - proceso_actual["bt"])
                proceso_actual = None
            else:
                # Chequear si hay un proceso más corto listo
                if heap and heap[0][0] < tiempo_restante[proceso_actual["pid"]]:
                    gantt.append({
                        "pid": proceso_actual["pid"],
                        "start": tiempo_inicio,
                        "end": tiempo_actual
                    })
                    heapq.heappush(heap, (tiempo_restante[proceso_actual["pid"]], proceso_actual["at"], proceso_actual["pid"], proceso_actual))
                    proceso_actual = None
        tiempo_actual += 1

    avg_wait = sum(tiempos_espera.values()) / len(tiempos_espera)
    return gantt, avg_wait




#Round Robin (con quantum configurable)
def round_robin(procesos, quantum):
    procesos = sorted(procesos, key=lambda p: p["at"])
    queue = []
    tiempo_actual = 0
    gantt = []
    tiempos_espera = {p["pid"]: 0 for p in procesos}
    tiempos_restantes = {p["pid"]: p["bt"] for p in procesos}
    llegada_index = 0

    while llegada_index < len(procesos) or queue:
        while llegada_index < len(procesos) and procesos[llegada_index]["at"] <= tiempo_actual:
            queue.append(procesos[llegada_index])
            llegada_index += 1

        if not queue:
            tiempo_actual = procesos[llegada_index]["at"]
            continue

        proceso = queue.pop(0)
        pid = proceso["pid"]
        exec_time = min(quantum, tiempos_restantes[pid])

        gantt.append({
            "pid": pid,
            "start": tiempo_actual,
            "end": tiempo_actual + exec_time
        })

        tiempo_actual += exec_time
        tiempos_restantes[pid] -= exec_time

        while llegada_index < len(procesos) and procesos[llegada_index]["at"] <= tiempo_actual:
            queue.append(procesos[llegada_index])
            llegada_index += 1

        if tiempos_restantes[pid] > 0:
            queue.append(proceso)

    # Calcular tiempo de espera promedio
    fin_por_proceso = {}
    for bloque in reversed(gantt):
        if bloque["pid"] not in fin_por_proceso:
            fin_por_proceso[bloque["pid"]] = bloque["end"]

    tiempos_totales = []
    for p in procesos:
        turnaround = fin_por_proceso[p["pid"]] - p["at"]
        waiting = turnaround - p["bt"]
        tiempos_totales.append(waiting)

    avg_wait = sum(tiempos_totales) / len(tiempos_totales)
    return gantt, avg_wait


# Priority Scheduling - sin preemptivo
def priorityPlanning(procesos):
    lista = procesos.copy()
    tiempo_actual = 0
    gantt = []
    tiempos_espera = []
    completados = []

    while lista:
        disponibles = [p for p in lista if p["at"] <= tiempo_actual]
        if not disponibles:
            tiempo_actual += 1
            continue
        proceso = min(disponibles, key=lambda p: p["priority"])
        lista.remove(proceso)
        tiempos_espera.append(tiempo_actual - proceso["at"])
        gantt.append({
            "pid": proceso["pid"],
            "start": tiempo_actual,
            "end": tiempo_actual + proceso["bt"]
        })
        tiempo_actual += proceso["bt"]
        completados.append(proceso)

    avg_wait = sum(tiempos_espera) / len(completados)
    return gantt, avg_wait