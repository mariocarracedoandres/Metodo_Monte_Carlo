# Monte Carlo simulation of radioactive decay
# Author: Mario Carracedo Andres
# Year: 2025
# License: MIT
# Description: Simulates radioactive decay of N nuclei over time

import time
import random

import matplotlib.pyplot as plt
########################### 
# Funciones auxiliares / Helper functions
###########################
def seed(): 
    """
    Generates a large integer seed based on system's monotonic clock.
    Returns: integer seed for random number generator
    """
    ns = time.monotonic() * 1e9 
    return int(ns) 

def scalerandom(rn, a, b): 
    """
    Scales a random number from [0,1] to [a,b].
    rn: random number in [0,1]
    a: lower bound
    b: upper bound
    Returns: scaled number in [a,b]
    """
    return a + (b - a) * rn

########################### 
# Programa principal / main script
########################### 
#1. Initialize seed
random.seed(seed())

#2. Parameters
lambda_ = 0.1                   # decay constant
N0 = 100                        # initial number of nuceli
Nt = N0                         # number of nucleo over time
tmaximo = int(5 / lambda_)      # maximum time

#3. Monte-Carlo loop
tiempos = []
nucleos_vivos = []

for tiempo in range(tmaximo + 1):
    tiempos.append(tiempo)
    nucleos_vivos.append(Nt)

    Nvivos = Nt
    for _ in range(Nvivos):
        rn = random.random()
        
        if rn < lambda_:  # decide decay event
            Nt = Nt - 1
            energia = scalerandom(random.random(), 0, 10)  # random energy released
            print(f"Tiempo {tiempo}: núcleo desintegrado, energía={energia:.2f}")

#4. Graficamos
plt.plot(tiempos, nucleos_vivos, marker='o')
plt.title("Radioactive decay (Monte Carlo)")
plt.xlabel("Time")
plt.ylabel("Number of alive nuclei")
plt.grid(True)

plt.show()