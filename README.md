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
[![Programming Languages](https://skillicons.dev/icons?i=py&perline=1)]
- [CustomTkinter](https://customtkinter.tomschimansky.com)


## ¿Cómo correr el proyecto?
Para poder correr el proyecto debe tener instalados los paquetes de:
- Tkinter
- Customtkinter
- Matplotlib
Es recomendado que utilice un ambiente virtual, ya sea utilizando pyenv o conda.
Luego de esto, se corre:
```python main.py```
Luego de ejecutar el archivo main.py podra seleccionar los archivos a cargar segun las acciones que desee realizar. Asimismo, puede seleccionar el algoritmo de planificacion o el escenario de sincronización. Se puede visualizar la informacion de los procesos, acciones y recursos cargados, reiniciar la simulacion, correr la simulación y visualizar las estadisticas.

## Preview del Proyecto
![image](<https://github.com/user-attachments/assets/9453efae-173b-45e2-b1c8-cd3fc2b235cd> "Diagrama de Gantt utilizando el algoritmo FIFO")
![image](<https://github.com/user-attachments/assets/80201f3d-a347-40e3-8a52-b0a63a1be870> "Diagrama de Gantt utilizando el algoritmo SJF")
![image](<https://github.com/user-attachments/assets/96ec74a5-f13e-4d68-8e0a-cab16874f143> "Diagrama utilizando semaforo como mecanismo de sincronizacion")
![image](<https://github.com/user-attachments/assets/498aa866-f378-408c-9b3f-966cc44464ba> "Informacion de los procesos cargados")
![image](<https://github.com/user-attachments/assets/d1c9fae6-64ea-4088-82d8-b898057819d5> "Informacion de los recursos cargados")
![image](<https://github.com/user-attachments/assets/13a52b9a-1e65-46c8-88d5-946feb509ca8> "Informacion de las acciones cargadas")





