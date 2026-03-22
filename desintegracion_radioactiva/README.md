# Monte Carlo Simulation of Radioactive Decay
Simulación por **Monte Carlo** del decaimiento radiactivo de un conjunto de núcleos a lo largo del tiempo, usando Python.  
El programa modela eventos de desintegración aleatorios y muestra la evolución del número de núcleos vivos.


###  Descripción
Este proyecto simula el decaimiento radiactivo de `N` núcleos mediante un método de Monte Carlo.  
En cada paso temporal, cada núcleo tiene una probabilidad `λ` de desintegrarse.  
Cuando ocurre una desintegración, se genera aleatoriamente la energía liberada y se registra el evento.

Las energías asociadas a cada evento de desintegración se generan de forma aleatoria y no están ligadas a un isótopo concreto. Esta elección es deliberada y permite centrar la simulación en los aspectos estadísticos del decaimiento, manteniendo el modelo general y fácilmente extensible.

La estructura del código facilita la sustitución del modelo de energía por distribuciones físicamente realistas si se requiere mayor nivel de detalle.

Al final, se grafica el número de núcleos vivos en función del tiempo.

### Tecnologías utilizadas
- Python 3.13.11
- `random`
- `time`
- `matplotlib`

### Parámetros del modelo
En el código se pueden modificar fácilmente:

- `lambda_`: constante de decaimiento
- `N0`: número inicial de núcleos
- `tmaximo`: tiempo máximo de simulación

Ejemplo:
```python
lambda_ = 0.1
N0 = 100
```

### Cómo ejecutar 
1. Asegúrate de tener Python 3 instalado.
2. Instala matplotlib si no lo tienes:
```bash
pip install matplotlib
```