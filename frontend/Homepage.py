import streamlit as st

st.set_page_config(
    page_title="Proyecto 2 - Simulador",
)

st.title("Proyecto 2 - Simulador")
st.markdown("""
Bienvenido al simulador de planificación y sincronización de procesos.

Utiliza el menú de la izquierda para navegar a:

- **Planificación**: Simula algoritmos como FIFO, SJF, Round Robin, etc.
- **Sincronización**: Visualiza mecanismos como mutex y semáforos con acceso a recursos.

Recuerda cargar los archivos `.txt` desde la interfaz para comenzar.
""")
