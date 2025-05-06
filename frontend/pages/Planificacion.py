import sys
import os
import streamlit as st
import time

# Agregar path del backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

#imports of the implemented planning algorithms
from backend.loadfile import buildProcessesDF
from backend.planning import (
    fifoPlanning,
    round_robin,
    sjfPlanning,
    srtfPlanning,
    priorityPlanning
)

st.set_page_config(page_title="Planificación - Múltiples Algoritmos")
st.title("Simulador de Algoritmos de Planificación")


archivo = st.file_uploader("Cargar archivo de procesos (.txt)", type="txt")
algoritmos_seleccionados = st.multiselect(
    "Selecciona uno o más algoritmos:",
    ["FIFO", "Round Robin"]
)


if "Round Robin" in algoritmos_seleccionados:
    quantum = st.number_input("Quantum para Round Robin", min_value=1, value=2)

def visualizar_gantt_dinamico(gantt, titulo, delay=0.2):
    st.subheader(titulo)
    espacio = st.empty()
    colores = {}

    bloques_html = []
    ciclos_html = []

    for bloque in gantt:
        pid = bloque["pid"]
        start = bloque["start"]
        end = bloque["end"]

        if pid not in colores:
            colores[pid] = f"#{hex(hash(pid) & 0xFFFFFF)[2:].zfill(6)}"

        for ciclo in range(start, end):
            bloques_html.append(f"<div style='display:inline-block; min-width:30px; height:40px; background:{colores[pid]}; text-align:center; color:white; line-height:40px; margin-right:1px; border-radius:4px;'>{pid}</div>")
            ciclos_html.append(f"<div style='display:inline-block; min-width:30px; height:20px; text-align:center; font-size:12px; margin-right:1px; color:#555;'>{ciclo}</div>")

            full_html = f"""
            <div style='overflow-x:auto; white-space:nowrap; padding:10px; border:1px solid #ddd; border-radius:8px;'>
                <div style='margin-bottom:6px;'>{''.join(bloques_html)}</div>
                <div>{''.join(ciclos_html)}</div>
            </div>
            """
            espacio.markdown(full_html, unsafe_allow_html=True)
            time.sleep(delay)

run = st.button("Run")

if archivo and algoritmos_seleccionados and run:
    procesos = buildProcessesDF(archivo)

    if "FIFO" in algoritmos_seleccionados:
        gantt_fifo, avg_wait_fifo = fifoPlanning(procesos)
    if "Round Robin" in algoritmos_seleccionados:
        gantt_rr, avg_wait_rr = round_robin(procesos, quantum)

    if "FIFO" in algoritmos_seleccionados:
        visualizar_gantt_dinamico(gantt_fifo, "Gantt - FIFO")
        st.success(f"[FIFO] Tiempo de espera promedio: {avg_wait_fifo:.2f}")

    if "Round Robin" in algoritmos_seleccionados:
        visualizar_gantt_dinamico(gantt_rr, "Gantt - Round Robin")
        st.success(f"[Round Robin] Tiempo de espera promedio: {avg_wait_rr:.2f}")
