# Proyecto 2 - Simulador de Algoritmos de Planificación y Escenarios de Sincronización

Ana Laura Tschen 226154

## Descripción
El proycto consiste en simular los distintos algoritmos de planificación y escenarios de sincronización solicitados. Se implementaron desde cero y se realizó una interfaz gráfica para poder visualizar su funcionamiento y métricas. Se permite seleccionar el algoritmo o escenario de sincronización a utilizar y la carga de archivos según sea requerido. 


### Algoritmos de Planificación Soportados
+ First In First Out
+ Shortest Job First
+ Shortest Remaining Time
+ Round Robin (con quantum configurable)
+ Priority

### Escenarios de Sincronización Soportados
+ Mutex Locks
+ Semáforos

## Tecnologías Utilizadas
[Programming Languages](https://skillicons.dev/icons?i=py&perline=1)
- [CustomTkinter](https://customtkinter.tomschimansky.com)


## ¿Cómo correr el proyecto?
Para poder correr el proyecto debe tener instalados los paquetes de:
- Tkinter
- Customtkinter
- Matplotlib
Es recomendado que utilice un ambiente virtual, ya sea utilizando pyenv o conda.
Luego de esto, se corre:
```python main.py```