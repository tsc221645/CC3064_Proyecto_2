import streamlit as st

st.title("Simulador de Algoritmos de Planificación")

#st.multiselect("Selecciona uno o más algoritmos",["First In First Out","Shortest Job First","Shortest Remaining Time", "Round Robin","Priority"])

c1, c2, c3 = st.columns(3)
c4, c5, = st.columns(2)

with st.container(border=True):
    c1.write("First In First Out")
    c2.write("Shortest Job First")
    c3.write("Round Robin")

with st.container(border=True):
    c4.write("Shortest Remaining Time")
    c5.write("Priority")
    