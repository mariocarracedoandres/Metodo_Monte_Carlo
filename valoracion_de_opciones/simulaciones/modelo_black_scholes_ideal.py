####################################################
# modelo_black_scholes_ideal.py
# Author: Mario Carracedo Andres
# Year: 2026
# Description: Simulación de cobertura dinámica ideal bajo el modelo de Black-Scholes.
####################################################

import numpy as np # para cálculos numéricos
import scipy.stats# para funciones de distribución
import matplotlib.pyplot as plt # para gráficos
import matplotlib.colors as colors
from matplotlib.collections import LineCollection
import matplotlib.cm as cm
import pandas as pd # para manejar datos en formato de tablas (dataframes)
import time # para tiempos
import random # para números aleatorios
import os # para obtener el directorio de trabajo
#plt.ioff() # para que no se muestren los gráficos en la consola

guardar_csv = False # True para guardar los datos en formato Excel (csv)

####################################################################### FUNCIONES AUXILIARES
###############-----############### Semilla aleatoria
def seed():
    """
    Nos da un numero entero muy grande dependeiendo de la hora local, como nunca podremos repetir esa msima hora pues el timepo avanza,
    Se considera al seed como una fomra de generar numeros aleatorios.
    """
    ns = time.monotonic() * 1e9 # obtenemos el tiempo local en nanosegundos
    return int(ns % (2**32)) # devolvemos el tiempo como un entero, modulo 2^32 para asegurarnos de que el número no sea demasiado grande para el generador de números aleatorios, que suele aceptar semillas de hasta 32 bits (0 a 2^32-1)
    
###############-----############### modelo de Black-Scholes
def black_scholes(S0, K, T, r, sigma, tipo_opcion):

    if T <= 1e-7:
        if tipo_opcion == "C":
            if S0 > K: # para evitar problemas con el T en el denominador
                return max(0.0, S0 - K), 1.0
            else:
                return max(0.0, S0 - K), 0.0
        else: # esto si es put P(venta)
            if S0 < K:
                return max(0.0, K - S0), -1.0
            else:
                return max(0.0, K - S0), 0.0
    
    # Cálculo de d1 y d2
    numerador_d1 = np.log(S0/K) + (r + (sigma**2)/2) * T
    denominador = sigma * np.sqrt(T)

    d1 = numerador_d1 / denominador
    d2 = d1 -sigma*np.sqrt(T)

    delta = scipy.stats.norm.cdf(d1)

    # Cálculo del precio de la opción "V" V = C si es call, V = P si es put
    if tipo_opcion == "C":
        V = S0*delta - K*np.exp(-r*T)*scipy.stats.norm.cdf(d2) #scipy.stats.norm() = N() es la función de distribución acumulada de la distribución normal estándar, nos dice el area bajo la curva == probabilidad
                                                                #N(d1) = cuanto cambia el precio de la opcion por euro/dolar que el activo subyacente varíe
                                                                #N(d2) = probabilidad de que la opción termine in the money, es decir, que el precio del activo subyacente sea mayor que el precio de ejercicio K al vencimiento T 
    else:
        V = K*np.exp(-r*T)*scipy.stats.norm.cdf(-d2) - S0*scipy.stats.norm.cdf(-d1)
        # Cálculo del precio de la opción de venta (put)
        delta = delta - 1 # el -1 es poque ahora las acciones no son comprar y vender, sino que ahora tomas prestado 1 accion, la vendes y la compras de tal manera que al devolverlas al dueño, temngas (ejeemplo: pides prestado, la vendes a 18, si la accion baja, compras a 10, la devuelves, ganas 18-10=8 euros, el vendedor te vende la accion a 18(lo acordado), tu la compras y la vendes a 10(precio actual), pierdes 8 euros, pero como gaste 8 antes, te quedas en 0, te cubriste)
    
    return V, delta

####################################################################### PROGRAMA PRICIPAL
###############-----############### Inicializamos la semilla
semilla = seed() # generamos una semilla aleatoria
#random.seed(40) # random.seed() inizializa el generador de numeros con una semilla especifica, como dentro va nuestra funcion seed(), esa es aletoria y nunca se repite || se puede poner radnom.seed(numero que quieras) para generar el mismo movimiento
np.random.seed(semilla) # np.random.seed() hace lo mismo que justo el de la linea de arriba, pero usa esa semilla para todo lo aleatorio de numpy, es decir todo lo de np.cosas. si no se pone, no habrá reproducibilidad en los resultados.


###############-----############### Parámetros movimiento browniano geometrico
print("\n" + "="*50)
print("Parámetros del modelo")
print("="*50)

# Tamaño del paso temporal / dt = desviación tipica 
dt = 0.0001  #segundos
while True: #calulamos el valor de T (en AÑOS)
    try:
        entrada = input("Indica el tiempo de vencimiento (T) en años (0.5 = 6 meses): \n")# nº de trayectorias a simular
        T = float(entrada)

        if T == float(entrada) and T > 0:
            break
        else:
            print("El valor (T) debe ser un número positivo \n")
    except ValueError: #se ejecuta si no es float
        print("El valor de (T) debe ser un número real positivo \n")

n_pasos = int(T/dt + 1) #+1 es porque el range acabe en n_pasos-1
while True:
    try:
        entrada = input("Indica número de trayectorias: \n")# nº de trayectorias a simular
        n_trayectorias = int(entrada)

        if n_trayectorias > 0:
            break
        else:
            print("EL número de trayectorias debe ser un número entero positivo \n")

    except ValueError: #se ejecuta si no es int
            print("EL número de trayectorias debe ser un número entero \n")
    


# condiciones iniciales
tiempo0 = 0.0
while True:
    try:
        entrada = input("Indica valor inicial del activo subyacente (S0): \n")# posición inicial
        posicion0 = float(entrada)

        if posicion0 == float(entrada) and posicion0 > 0:
            break
        else:
            print("La posición inicial debe ser un número real > 0 \n")

    except ValueError: #se ejecuta si no es float > 0
            print("La posición inicial debe ser un número real > 0 \n")


# Parametros para contolar tendencia en el movimiento
while True: #calulamos el valor de K
    try:
        entrada = input("Indica la tendencia (mu): \n")
        mu = float(entrada)

        if mu == float(entrada) and mu > 0:
            break
        else:
            print("El valor de (mu) debe ser un número positivo \n")
    except ValueError: #se ejecuta si no es float
        print("El valor de (mu) debe ser un número real positivo \n")

while True: #calulamos el valor de K
    try:
        entrada = input("Indica la volatilidad (sigma): \n")
        sigma = float(entrada)

        if sigma == float(entrada) and sigma > 0:
            break
        else:
            print("El valor de (sigma) debe ser un número positivo \n")
    except ValueError: #se ejecuta si no es float
        print("El valor de (sigma) debe ser un número real positivo \n")

###############-----############### Parametros  de V y prima (V0)
#Parámetros
S0 = posicion0 #Valor incial del precio de la acción
while True: #calulamos el valor de K
    try:
        entrada = input("Indica el valor del precio de ejercicio (K): \n")# nº de trayectorias a simular
        K = float(entrada)

        if K == float(entrada) and K > 0:
            break
        else:
            print("El valor de (K) debe ser un número positivo \n")
    except ValueError: #se ejecuta si no es float
        print("El valor de (K) debe ser un número real positivo \n")

while True: #calulamos el valor de r anual
    try:
        entrada = input("Indica la tasa libre de riesgo (r) anual: \n")# nº de trayectorias a simular
        r = float(entrada)

        if r == float(entrada) and r > 0:
            break
        else:
            print("El valor (r) debe ser un número positivo \n")
    except ValueError: #se ejecuta si no es float
        print("El valor de (r) debe ser un número real positivo \n")

sigma = sigma

# cáluclo del precio de la opción "V" dependiendo si es compra = C (call), o venta = P (put)
while True:
    tipo_opcion = input("Indica el tipo de opción (C para call, P para put): \n").upper().strip() # pedimos al usuario que indique el tipo de opción, y convertimos la respuesta a mayúsculas para facilitar la comparación || .strip() por si hay error al pomner espacios
    if tipo_opcion == "C" or tipo_opcion == "P":
        break
    else: 
        print("Debe ser C o P \n")

# precio de la prima
V0, delta0 = black_scholes(S0, K, T, r, sigma, tipo_opcion)


###############-----############### Lista para almacenar las trayectorias
t = np.linspace(0, T, n_pasos) # la lista comienza con el valor inicial

S = [posicion0] # la lista comienza con el valor inicial || seria S_t
V = [V0] # la lista comienza con el valor inicial || Contiene el valor de la prima y los demas V hata el vencimiento son el valor de la opcion en el mercado (puedes vender tu opcion antes del vencimiento )
delta = [delta0] # la lista comienza con el valor inicial || Contiene el valor de la prima y los demas V hata el vencimiento son el valor de la opcion en el mercado

trayectorias = [] # comienza sin nada porque vamos a ir meteiendo trayectorias en la lisa || sería cada trayectoriad de S para diferentes S_t
trayectorias_opciones = [] # comienza sin nada porque vamos a ir meteiendo trayectorias en la lisa || sería cada trayectoria de opciones para diferentes S_t
trayectorias_delta = [] # comienza sin nada porque vamos a ir meteiendo trayectorias en la lisa || sería cada trayectoria de delta para diferentes S_t

print("Calculando trayectorias... por favor espere.")
tiempo_inicio = time.time() #inizializo el tiempo

for j in range(1, n_trayectorias+1):
    S = [posicion0] # la lista comienza con el valor inicial
    V = [V0] # la lista comienza con el valor inicial
    delta = [delta0] # la lista comienza con el valor inicial

    for i in range(1, n_pasos): # T + 1 porque el tiempo 0 no se incluye en la lista
        ##### Calculamos S en cada paso
        tiempo_actual = i*dt

        z = np.random.normal(0, 1) # generamos un numero aleatorio de la distribución normal

        S_t = S[-1]*np.exp((mu-sigma**2/2)*dt + sigma*np.sqrt(dt)*z) # posicion ultima + salto aleatorio
        S.append(S_t) # guardamos la nueva posicion en la lista de posiciones

        ##### Calculamos V en cada paso
        t_hasta_vencimiento = T-tiempo_actual
        V_t, delta_t = black_scholes(S_t, K, t_hasta_vencimiento, r, sigma, tipo_opcion)

        V.append(V_t)
        delta.append(delta_t)

    # Esto es para combinar todas las trayectroias en una sola grafica
    trayectorias.append(S) # guardamos una trayectroia en una lista de treyectorias
    trayectorias_opciones.append(V)
    trayectorias_delta.append(delta)
    #guardamos los resultados de la primer iteración

print(f"Simulacion desde t=0 hasta t={T}\n")

tiempo_fin = time.time()
duracion = tiempo_fin - tiempo_inicio
print(f"Tiempo total de simulación: {duracion} segundos")

###############-----############### Graficamos figura 1 (movimiento browniano geometrico)
fig = plt.figure()
fig_ax = fig.add_subplot(111)

# plot de todas las trayectorias
for i in range(len(trayectorias)): #listas van de 0 a n_trayectorias-1 == trayectorias[0] = trayectorias 1 ..... trayectorias[49] = trayectorias 50, por eso el +1 en el label, pero el 1 en el plot interno
        fig_ax.plot(t, trayectorias[i],lw = 1, alpha = 0.5)


fig_ax.set_title(f"Movimiento Browniano (Monte Carlo) para {n_trayectorias} trayectorias\n"
                 rf"Tendencia: mu={mu}; Volatilidad: $\sigma$={sigma}; Semilla: {semilla}")
fig_ax.set_xlabel("Tiempo (años)")
fig_ax.set_ylabel("Precios (€)")
fig_ax.grid(True)

# lo que se va a plotear
t = np.array(t) # convertimos la lista de tiempos a un array de numpy para facilitar el manejo

#eje_x = fig_ax.axhline(0, color='black', alpha = 0.5, label = "y=0") # línea horizontal en y=0 para referencia || ya devuelve un unico objeto

eje_inicial, = fig_ax.plot(t, np.full_like(t, posicion0), color = "black", alpha = 0.5,label = f"Posición inicial {posicion0}") # graficamos la posición inicial
#trayectoria, = fig_ax.plot(t, posiciones,lw = 1, label = "Trayectoria de la partícula") # graficamos la trayectoria de la partícula

valor_esperado, = fig_ax.plot(t, posicion0*np.exp(t*mu), lw=1, color = "red", label = "Valor esperado") # graficamos el valor esperado de la posición en cada tiempo || nos dice el promesdio de todas las trayectorias
mediana, = fig_ax.plot(t, posicion0 * np.exp((mu - 0.5 * sigma**2) * t), lw=1, color = "green", label = "Mediana") # graficamos la mediana || nos dice donde es mas probable que estes

#desviacion_tipca, = fig_ax.plot(tiempos, np.sqrt(np.array(tiempos))*sigma, lw=1, color = "black", label = "Desviación típica") # graficamos la desviación típica de la posición en cada tiempo 
log_tendencia = (mu - 0.5 * sigma**2) * t
margen = 1.96 * sigma * np.sqrt(t)

inferior = posicion0 * np.exp(log_tendencia - margen)
superior = posicion0 * np.exp(log_tendencia + margen)

desviacion_tipca_down, = fig_ax.plot(t, inferior , lw=1, alpha = 0.7, color = "purple", label = "Desviación down")
desviacion_tipca_up, = fig_ax.plot(t, superior , lw=1, alpha = 0.7, color = "purple", label = "Desviación up") 

area_posible = fig_ax.fill_between(t, inferior, superior, color='purple', alpha=0.1, label="Zona de Confianza Log-Normal(95%)")

# legenda
fig_ax.legend(handles=[eje_inicial, mediana, valor_esperado, area_posible]) 
    

###############-----############### Graficamos FIGURA 2 (Opciones)
fig2 = plt.figure(figsize=(10, 6))
ax_opciones = fig2.add_subplot(111)

# Plot de todas las trayectorias de las opciones
opcion_inicial, = ax_opciones.plot(t, np.full_like(t, V0), color='purple', lw=2, zorder=10, label = f"Precio de la prima{V0}")   
for i in range(len(trayectorias_opciones)): 
    ax_opciones.plot(t, trayectorias_opciones[i], lw=1, alpha=0.5)

# Calculamos la mediana para cada paso de tiempo (eje de las trayectorias)
mediana_opciones, = ax_opciones.plot(t, np.median(trayectorias_opciones, axis=0), color='blue', lw=2, label='Mediana de la Opción', zorder=10)

ax_opciones.set_title(f"Evolución del valor de la Opción ({tipo_opcion})\n"
                      rf"Strike K={K}; Tasa r={r}; Volatilidad $\sigma$={sigma}")
ax_opciones.set_xlabel("Tiempo (años)")
ax_opciones.set_ylabel("Precio de la Opción (€)")
ax_opciones.grid(True, alpha=0.3)

# Añadimos una línea en el 0 para ver claramente cuáles expiran sin valor
ax_opciones.axhline(0, color='black', lw=1, zorder=10)

# legenda1
ax_opciones.legend(handles=[opcion_inicial, mediana_opciones]) 


###############-----############### Graficamos FIGURA 3 (Delta vs precio) y (Delta vs tiempo)
fig3 = plt.figure(figsize=(15, 6))
############### Delta vs precio
ax_deltas = fig3.add_subplot(121)

# Plot de todas las trayectorias de las opciones
if tipo_opcion == "C":
    delta_inferior = ax_deltas.axhline(0, color='red', linestyle='--', alpha=0.5, label = r"límite $\Delta$ inferior")
    delta_superior = ax_deltas.axhline(1, color='green', linestyle='--', alpha=0.5, label = r"límite $\Delta$ superior")
else:
    delta_inferior = ax_deltas.axhline(-1, color='red', linestyle='--', alpha=0.5, label = r"límite $\Delta$ inferior")
    delta_superior = ax_deltas.axhline(0, color='green', linestyle='--', alpha=0.5, label = r"límite $\Delta$ superior")

cmap = plt.get_cmap('viridis') #viridis , winter, plasma, inferno, magma, cividis, Greys, Purples, Blues, Greens, Oranges, Reds, YlOrBr, YlOrRd, OrRd, PuRd, RdPu, BuPu, GnBu, PuBu, YlGnBu, PuBuGn, BuGn, YlGn
norm = colors.Normalize(vmin=t.min(), vmax=t.max())

for i in range(len(trayectorias_delta)):
    S_i = trayectorias[i]
    Delta_i = trayectorias_delta[i]
    
    # Creamos segmentos que unen el punto (i) con el (i+1)
    puntos = np.array([S_i, Delta_i]).T.reshape(-1, 1, 2)
    segmentos = np.concatenate([puntos[:-1], puntos[1:]], axis=1)
    
    # Creamos la colección de líneas
    lc = LineCollection(segmentos, cmap='viridis', norm=norm) #coleccion de las lineas coloridas
    
    # Le pasamos el array de tiempos para que coloree cada segmento
    lc.set_array(t[:-1]) # para 100 puntos tienes 99 segmentos, por eslo :-1
    lc.set_linewidth(0.5) # Grosor de la línea
    lc.set_alpha(0.5)     # Transparencia
    
    ax_deltas.add_collection(lc)

# Calculamos la curva teórica de delta
S_min = np.min(trayectorias)
S_max = np.max(trayectorias)
S_limite = np.linspace(S_min, S_max, n_pasos) # al igual que para tiempos lo teniamos ordenado, para S igual

deltas_teoricos = [black_scholes(s, K, T, r, sigma, tipo_opcion)[1] for s in S_limite]

# Graficamos curva teórica
curva_teorica, = ax_deltas.plot(S_limite, deltas_teoricos, color='purple', alpha = 0.9, lw=2.5, label=r"$\Delta$ Teórico (Black-Scholes) para $t_v$ = T", zorder=100)# zorder=10 para que la curva teórica no se superponga sobre la curva de la cobertura

ax_deltas.set_title(rf"Evolución del valor de $\Delta$"                
                    rf"\n Strike K={K}; Tasa r={r}; Volatilidad $\sigma$={sigma}")
ax_deltas.set_xlabel("Precio (€)")
ax_deltas.set_ylabel(r"$\Delta (acciones)$")
ax_deltas.grid(True, alpha=0.3)

# legenda1
ax_deltas.legend(handles=[delta_inferior, delta_superior, curva_teorica]) 

#mapa con colores para el subplot(1,1,1)
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([]) # Esto es necesario para matplotlib

cbar = fig3.colorbar(sm, ax=ax_deltas, pad=0.05) 
cbar.set_label('Tiempo transcurrido (años)')

############### Delta vs tiempo
ay_deltas = fig3.add_subplot(122)

for i in range(len(trayectorias_delta)): 
    ay_deltas.plot(t, trayectorias_delta[i], lw=0.5)

# mediana
mediana_delta = np.median(trayectorias_delta, axis=0)
ay_deltas.plot(t, mediana_delta, color='black', lw=1, zorder=10, label = r"Mediana $\Delta$") # zorder=10 para que la linea de media no se superponga sobre la curva

# Añadimos líneas de referencia en 0 y 1 (límites de la Delta para Call)
if tipo_opcion == "C":
    ay_deltas.axhline(0, color='red', linestyle='--', alpha=0.5, label = r"límite $\Delta$ inferior")
    ay_deltas.axhline(1, color='green', linestyle='--', alpha=0.5, label = r"límite $\Delta$ superior")
else:
    ay_deltas.axhline(-1, color='red', linestyle='--', alpha=0.5, label = r"límite $\Delta$ inferior")
    ay_deltas.axhline(0, color='green', linestyle='--', alpha=0.5, label = r"límite $\Delta$ superior")

# ajustes
ay_deltas.set_title(rf"Evolución del valor de $\Delta$"                
                    rf"\n Strike K={K}; Tasa r={r}; Volatilidad $\sigma$={sigma}")
ay_deltas.set_xlabel("Tiempo (años)")
ay_deltas.set_ylabel(r"$\Delta (acciones)$")
ay_deltas.grid(True, alpha=0.3)
ay_deltas.legend(loc='best')

plt.tight_layout()# Ajuste automático para que no se solapen los ejes de los dos gráficos


###############-----############### CÁLCULO DE RESIDUOS (como de bien el modelo se acerca a la realidad supuesta) == lo que gana o pierde el vendedor (como un banco)
print("\n" + "="*50)
print("ANÁLISIS DE EFICIENCIA DE LA COBERTURA")
print("="*50)

errores_finales = []

for i in range(n_trayectorias):
    # 1. El valor real que debe pagar el banco al cliente (Payoff)
    S_final = trayectorias[i][-1]
    if tipo_opcion == "C":
        payoff_real = max(0, S_final - K)
    else:
        payoff_real = max(0, K - S_final)
    
    # 2. El valor que tu simulación dice que vale la opción
    valor_simulado = trayectorias_opciones[i][-1] # lo que vale la opción al final 
    
    # 3. El error en esa trayectoria
    error = valor_simulado - payoff_real
    errores_finales.append(error)

# Estadísticas del error
error_medio = np.mean(errores_finales)
error_std = np.std(errores_finales)

print(f"Número de trayectorias: {n_trayectorias}")
print(f"Error medio de cobertura: {error_medio:.4f} €")
print(f"Desviación típica del error: {error_std:.4f} €")
print(f"El error máximo fue de: {np.max(np.abs(errores_finales)):.4f} €")
print("="*50 + "\n") # para seprar con ==============

###############-----############### Gráfica 4 de Residuos
fig4 = plt.figure(figsize=(10, 6))
ax_res = fig4.add_subplot(111)

# Listas para clasificar por colores según el estado final
s_t_final_itm = [] 
errores_itm = []

s_t_final_otm = []
errores_otm = []

for i in range(n_trayectorias):
    S_f = trayectorias[i][-1] #cogemos ultimo precio de cada trayectoria en t = T
    
    # Calculamos el Payoff Real
    if tipo_opcion == "C": # si es call
        payoff_real = max(0, S_f - K)
    else: # si es put
        payoff_real = max(0, K - S_f)
    
    # Calculamos el error (Ganancia/Pérdida)
    error = trayectorias_opciones[i][-1] - payoff_real # es error porque teoricamente debe ser 0 || opción en el mercado en T = ganancia tras (S_final-K)
    
    # Clasificamos para los colores
    if payoff_real > 0: # comprador gana dinero
        s_t_final_itm.append(S_f)
        errores_itm.append(error)
    else: #vendedor gana dinero
        s_t_final_otm.append(S_f)
        errores_otm.append(error)

# Dibujamos los puntos AZULES (ITM - La opción terminó con valor)
ax_res.scatter(s_t_final_itm, errores_itm, color='royalblue', edgecolors='black', s=80, alpha=0.8, label=f"En el Dinero (ITM) \n Nº trayectorias: {len(s_t_final_itm)}") # pinta de color azul los puntos que terminaron con S_final > K

# Dibujamos los puntos AMARILLOS (OTM - La opción terminó en 0)
ax_res.scatter(s_t_final_otm, errores_otm, color='gold', edgecolors='black', s=80, alpha=0.7, label=f"Fuera del Dinero (OTM) \n Nº trayectorias: {len(s_t_final_otm)}") # pinta de color amarillo los puntos que terminaron en S_final < K

# --- LÍNEA ROJA EN EL EJE X (Error = 0) ---
ax_res.axhline(0, color='red', linestyle='--', lw=2.5, label="Objetivo: Cobertura Perfecta")

# Estética
ax_res.set_title("Análisis de los errores de Cobertura (Residuos) en modelo ideal \n"
                 "(Valor Simulado - Payoff Real)")
ax_res.set_xlabel(r"Precio Final del Activo $S_{T}$ (€)")
ax_res.set_ylabel("Payoff neto de la cartera de cobertura ideal(€)")

# Ajustamos los límites de Y para que se vea la línea roja aunque el error sea casi 0
# Si el error es 0.0000, forzamos un zoom pequeño para que no se vea vacío
max_err = max(np.abs(errores_itm + errores_otm)) if (errores_itm + errores_otm) else 0
zoom = max(max_err * 1.5, 0.05) 
ax_res.set_ylim(-zoom, zoom)

ax_res.legend(loc='best', fontsize='small', frameon=True) #frameon=True para que no se vea el borde de la figura
ax_res.grid(True, alpha=0.3)


###############-----############### FIGURA 5: Payoff neto (P&L de Cobertura)
fig5 = plt.figure(figsize=(10, 6))
ax_pay = fig5.add_subplot(111)

# Creamos una línea continua para el Payoff Teórico
s_min_plot = min(min(s_t_final_itm + s_t_final_otm), K) * 0.8
s_max_plot = max(max(s_t_final_itm + s_t_final_otm), K) * 1.2
s_rango = np.linspace(s_min_plot, s_max_plot, n_pasos)

if tipo_opcion == "C":
    payoff_teorico = np.maximum(0, s_rango - K)
else: #si es put P(venta)
    payoff_teorico = np.maximum(0, K - s_rango)

ax_pay.plot(s_rango, payoff_teorico - V0, color='black', lw=2, label="Payoff neto (€)", zorder=1) # line que va----- / de esa manera y es el teórico

# listas con los pagos
pagos_itm = [max(0, s - K) if tipo_opcion=="C" else max(0, K - s) for s in s_t_final_itm] #otra manera de crear bucles mas eficiente || si es call, te hace (s-k) y si no, te hace (k-s), para cada s_t_final
pagos_otm = [0] * len(s_t_final_otm) # si s<k el banco no paga nada porque el cliente no compra

#dibujo los puntos de beneficio neto
if s_t_final_itm:
    ax_pay.scatter(s_t_final_itm, pagos_itm - V0, color='royalblue', s=100, edgecolors='black', label=f"Pago Real (ITM)\n Nº trayectorias: {len(s_t_final_itm)}", zorder=2)

if s_t_final_otm:
    ax_pay.scatter(s_t_final_otm, pagos_otm - V0, color='gold', s=100, edgecolors='black', label=f"Sin Pago (OTM) \n Nº trayectorias: {len(s_t_final_otm)}", zorder=2)
    
# mediana
S_final_mediana = posicion0 * np.exp((mu - 0.5 * sigma**2) * T) #mediana de los precios
if tipo_opcion == "C":
    beneficio_mediana = max(0, S_final_mediana - K) - V0 # mediana de los beneficios netos
else: # si es put
    beneficio_mediana = max(0, K - S_final_mediana) - V0 # mediana de los beneficios netos
ax_pay.scatter(S_final_mediana, beneficio_mediana, color='purple', s=100, edgecolors='black', label="Mediana", zorder=2) #punto que es la mediana en el precio mediana

# Ajustes gráfica
ax_pay.set_title(f"Perfil de Pago al Vencimiento (Payoff)\nStrike K={K}")
ax_pay.set_xlabel("Precio Final del Activo ($S_T$) (€)")
ax_pay.set_ylabel("Payoff neto (€)")
ax_pay.axvline(K, color='red', linestyle='--', alpha=0.5, label=f"Strike K={K}")
ax_pay.grid(True, alpha=0.3)
ax_pay.legend()


###############-----############### Guardo datos + visualizar primeras filas
while True: #calulamos el valor de r anual
    opcion_guardar = input("¿Desea guardar los datos en formato Excel(csv) (y), o no (n): \n").upper().strip()

    if opcion_guardar == "Y" or opcion_guardar == "N":
        break
    else:
        print("Pulse sólo (Y/y) o (N/n) \n")

time_inicio_guardado = time.time()

if opcion_guardar == "Y":
########## Guardamos figuras
    print("guardando figuras y datos en formato Excel (csv)...")
    
    # Guardo la imagen en "plots" :
    directorio_del_script = os.path.dirname(os.path.abspath(__file__)) #nos da la ruta donde esta el .py
    ruta_plots = os.path.join(directorio_del_script, "plots_black_scholes_ideal") #para guardar el archivo en la carpeta donde esta el .py

    if not os.path.exists(ruta_plots): #si no existe la carpeta plots, la creemos
        os.makedirs(ruta_plots) #creamos la carpeta plots
        print(f"Carpeta plots creada en: {ruta_plots} \n")

    # Guardamos imageN de movimiento browniano geometrico (precios en el tiempo)
    ruta_precios = os.path.join(ruta_plots, "mov_browniano_geometrico(png).png")
    fig.savefig(ruta_precios, dpi=200)
    print(f"Figura (mov_browniano_geometrico(png).png) guardada en: {ruta_precios} \n")

    #Guardamos imagen de opciones
    nombre_archivo_opcion = "precio_opciones_con_el_tiempo(png).png"
    ruta_guardado_opcion = os.path.join(ruta_plots, nombre_archivo_opcion)
    fig2.savefig(ruta_guardado_opcion, dpi=200)
    print(f"Figura (precio_opciones_con_el_tiempo(png).png) guardada en: {ruta_guardado_opcion} \n")

    #Guardamos imagen de deltas
    ruta_deltas = os.path.join(ruta_plots, "cobertura_dinamica(png).png")
    fig3.savefig(ruta_deltas, dpi=200)
    print(f"Figura (cobertura_dinamica(png).png) guardada en: {ruta_deltas} \n")

    # Guardamos imagen payoff neto vendedor(residuos) (lo que gana el banco)
    ruta_res = os.path.join(ruta_plots, "payoff_neto_cartera_cobertura(residuos)(png).png")
    fig4.savefig(ruta_res, dpi=200)
    print(f"Figura (payoff_neto_cartera_cobertura(residuos)(png).png) guardada en: {ruta_res} \n")

    # Guardamos imagen de payoff neto
    ruta_payoff = os.path.join(ruta_plots, "payoff_neto_cliente(png).png")
    fig5.savefig(ruta_payoff, dpi=200)
    print(f"Figura (payoff_neto_cliente(png).png) guardada en: {ruta_payoff} \n")


if guardar_csv: #cambiar la linea 20 (False ==> True) para guardar los datos en formato Excel (csv)
########## Guardamos datos en csv
    # Preparamos la matriz (Tiempo + Trayectorias de precios + semilla) y (Tiempo + Trayectorias de popciones + semilla)
    semilla_columna = [semilla]*len(t) # [convierte semilla en una lista de la misma longitud que tiempo]

    matriz_para_guardar = np.column_stack([np.array(t), np.array(trayectorias).T, np.array(semilla_columna)]) # nos junta el vector tiempo con la matriz de trayectorias

    matriz_para_guardar_opciones = np.column_stack([np.array(t), np.array(trayectorias_opciones).T, np.array(semilla_columna)]) 
    #matriz para guardar delta vs precio y delta vs tiempo
    # 1. Base Común (Las columnas de referencia)
    matriz_para_guardar_deltas = np.column_stack([np.array(t), np.array(S_limite).T, np.array(deltas_teoricos), np.array(trayectorias_delta).T, np.array(semilla_columna)]) # suamos S_limite porque esta ordenado [minimo,...81, 82... hata el max]

    todos_los_S_final = s_t_final_itm + s_t_final_otm # creamos lista con precios finales [primero todos los que son ITM y luego todos los que son OTM] || si hiciesemos trayectorias[i][-1] for i in range(n_trayectorias). hacemos [ordenar por orden de trayectorias] mezclas ITM con OTM
    todos_los_errores = errores_itm + errores_otm
    payoff_neto = [(p - V0) for p in (pagos_itm + pagos_otm)] # Calculamos el payoff neto por orden de ITM ... OTM
    estado = ["ITM"] * len(s_t_final_itm) + ["OTM"] * len(s_t_final_otm) #creamos una lista ["ITM", "ITM", ..., "ITM", "OTM", "OTM". ..., "OTM"]
    semilla_res_payoff_neto = [semilla]*len(todos_los_S_final) # creamos una lista de semillas para cada trayectoria
    matriz_para_guardar_res_payoff_neto = np.column_stack([np.array(todos_los_S_final), np.array(todos_los_errores), np.array(payoff_neto), np.array(estado), np.array(semilla_res_payoff_neto)])
    
    # Convertimos a un "DataFrame" de Pandas
    cabecera = ["Tiempo"] + [f"Trayectoria {i+1}" for i in range(n_trayectorias)] + ["Semilla"] # cada [] es una columna
    df = pd.DataFrame(matriz_para_guardar, columns=cabecera) # [convierte matriz en tablas, nombres de columnas] ||df = dataframe
    df["Semilla"] = df["Semilla"].astype(int) # convertimos la columna de semilla a enteros para que no ponga notacion cientifica

    cabecera_opciones = ["Tiempo"] + [f"Trayectoria {i+1}" for i in range(n_trayectorias)] + ["Semilla"] 
    df_opciones = pd.DataFrame(matriz_para_guardar_opciones, columns=cabecera_opciones)
    df_opciones["Semilla"] = df_opciones["Semilla"].astype(int)

    cabecera_deltas = ["Tiempo"] + ["Precios S"]+ [r"$\Delta$ para t=T"] + [rf"$\Delta$ para Trayectoria {i+1}" for i in range(n_trayectorias)] + ["Semilla"] 
    df_deltas = pd.DataFrame(matriz_para_guardar_deltas, columns=cabecera_deltas)
    df_deltas["Semilla"] = df_deltas["Semilla"].astype(int)

    cabecera_res_payoff_neto = [r"Precio final S_{T}"] + ["resíduos"] + ["Payoff neto"] + ["estado"] + ["Semilla"] 
    df_res_payoff_neto = pd.DataFrame(matriz_para_guardar_res_payoff_neto, columns=cabecera_res_payoff_neto)
    df_res_payoff_neto["Semilla"] = df_res_payoff_neto["Semilla"].astype(int)  

    # Nombres de archivos
    nombre_archivo_datos_precios = "datos_mov_browniano_geometrico(csv).csv" #nombre de archivo a guardar como datos  nombre_archivo_datos = "datos_movimiento_browniano_geometrico   (csv).csv" #nombre de archivo a guardar como datos
    ruta_archivo_datos = os.path.join(ruta_plots, nombre_archivo_datos_precios)

    nombre_archivo_datos_opciones = "datos_precio_opciones_con_el_tiempo(csv).csv"
    ruta_archivo_datos_opciones = os.path.join(ruta_plots, nombre_archivo_datos_opciones)

    nombre_archivo_datos_deltas = "datos_cobertura_dinamica(csv).csv"
    ruta_archivo_datos_deltas = os.path.join(ruta_plots, nombre_archivo_datos_deltas)

    nombre_archivo_datos_res_payoff_neto = "Payoff_neto_cartera_cobertura(residuos)_y_cliente(csv).csv"
    ruta_archivo_datos_res_payoff_neto = os.path.join(ruta_plots, nombre_archivo_datos_res_payoff_neto)

    # 1. Guardar CSV (Para leer tú en Excel/Bloc de notas)
    #cabecera = "Tiempo;" + ";".join([f"T{i+1}" for i in range(n_trayectorias)])
    #np.savetxt(ruta_archivo_datos, matriz_para_guardar, delimiter=";", header=cabecera, comments='', fmt="%.4f", decimal=",")
    #Usamos pandas
    # sep=';' separa columnas
    # decimal=',' pone comas en los números (para Excel España)
    # index=False : no guarda el número de fila (0, 1, 2...)
    df.to_csv(ruta_archivo_datos, sep=';', decimal=',', index=False)
    print(df.head()) # mostramos las primeras filas del dataframe para verificar que se ha guardado correctamente
    print(f"Archivos guardados en /plots:\n - {nombre_archivo_datos_precios} (Excel) \n")

    df_opciones.to_csv(ruta_archivo_datos_opciones, sep=';', decimal=',', index=False)
    print(df_opciones.head()) # mostramos las primeras filas del dataframe para verificar que se ha guardado correctamente
    print(f"Archivos guardados en /plots:\n - {nombre_archivo_datos_opciones} (Excel) \n")

    df_deltas.to_csv(ruta_archivo_datos_deltas, sep=';', decimal=',', index=False)
    print(df_deltas.head()) # mostramos las primeras filas del dataframe para verificar que se ha guardado correctamente
    print(f"Archivos guardados en /plots:\n - {nombre_archivo_datos_deltas} (Excel) \n")

    df_res_payoff_neto.to_csv(ruta_archivo_datos_res_payoff_neto, sep=';', decimal=',', index=False)
    print(df_res_payoff_neto.head()) # mostramos las primeras filas del dataframe para verificar que se ha guardado correctamente
    print(f"Archivos guardados en /plots:\n - {nombre_archivo_datos_res_payoff_neto} (Excel) \n")
else:
    print("Datos no guardados \n")

time_fin_guardado = time.time()
duracion_guardado = time_fin_guardado - time_inicio_guardado
print(f"Tiempo total de guardado: {duracion_guardado} segundos")
#mostramos
plt.show()