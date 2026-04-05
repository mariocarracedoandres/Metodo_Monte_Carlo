####################################################
# modelo_black_scholes_realista_leland.py
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
    # Usamos np.where para que funcione con matrices de golpe
    # Evitamos división por cero asegurando un T mínimo muy pequeño para el cálculo
    T_seguro = np.maximum(T, 1e-9) #nos da el maximo de cada elemento de T y lo comparamos con 1e-9 (es decir, si es menor que 1e-9, lo ponemos igual a 1e-9)
    
    # Cálculo de d1 y d2 (esto ya funciona con matrices gracias a NumPy)
    numerador_d1 = np.log(S0 / K) + (r + (sigma**2) / 2) * T_seguro
    denominador = sigma * np.sqrt(T_seguro)
    d1 = numerador_d1 / denominador
    d2 = d1 - sigma * np.sqrt(T_seguro)

    delta = scipy.stats.norm.cdf(d1)

    if tipo_opcion == "C":
        V = S0 * delta - K * np.exp(-r * T_seguro) * scipy.stats.norm.cdf(d2)
    else:
        V = K * np.exp(-r * T_seguro) * scipy.stats.norm.cdf(-d2) - S0 * scipy.stats.norm.cdf(-d1)
        delta = delta - 1

    # --- CORRECCIÓN PARA EL VENCIMIENTO (T=0) ---
    # Si T es muy pequeño, forzamos el valor intrínseco para evitar errores numéricos
    if tipo_opcion == "C":
        payoff_final = np.maximum(0.0, S0 - K)
        delta_final = np.where(S0 > K, 1.0, 0.0) #np.where(condicion, valor si es verdadero, valor si es falso)
    else:
        payoff_final = np.maximum(0.0, K - S0)
        delta_final = np.where(S0 < K, -1.0, 0.0)

    # Si T es menor que el umbral, aplicamos el payoff final, si no, el valor de la fórmula
    V = np.where(T <= 1e-7, payoff_final, V) #antes lo poniamos al principio de la funcion || si es T(matriz) alguno menor que 1e-7, lo ponemos igual a payoff_final, si no, es como el else que no poniamos, que te calculaba todo,es decir, V
    delta = np.where(T <= 1e-7, delta_final, delta)

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

############### Parámetros para pasar de cartera ideal a real
while True: #calulamos el valor de r anual
    try:
        entrada = input("Indica la frecuencia de rebalanceo (40 == 1 dia (252 diuas laborales)): \n")# nº de trayectorias a simular
        frecuencia_rebalanceo = float(entrada)

        if frecuencia_rebalanceo == float(entrada) and r > 0:
            break
        else:
            print("la frencuenca de rebalanceo debe ser un número positivo \n")
    except ValueError: #se ejecuta si no es float
        print("La frecuencia de rebalanceo debe ser un número real positivo \n")

while True: #calulamos el valor de r anual
    try:
        entrada = input(f"Indica la comisión por volumen (0.0002 == 0.02% comision): \n")# nº de trayectorias a simular
        comision_volumen = float(entrada)

        if comision_volumen == float(entrada) and r > 0:
            break
        else:
            print("Indica la comisión por volumen debe ser un número positivo \n")
    except ValueError: #se ejecuta si no es float
        print("Indica la comisión por volumen debe ser un número real positivo \n")

while True: #calulamos el valor de r anual
    try:
        entrada = input("Indica el coste fijo por operación (0.001 == 0.001€ fijos por cada operación de compra/venta): \n")# nº de trayectorias a simular
        coste_fijo = float(entrada)

        if coste_fijo == float(entrada) and r > 0:
            break
        else:
            print("El coste fijo por operación debe ser un número positivo \n")
    except ValueError: #se ejecuta si no es float
        print("El coste fijo por operación debe ser un número real positivo \n")

#frecuencia_rebalanceo = 40 #tomamos T=1 == 252 dias (laborales diarios) == rebalenceo cada dia || Rebalanceamos cada 10 pasos (simula tiempo discreto)(antes considerabamos que cada paso dt, rebalanceabamos, como en ese mundo los pasos dt es como "continuo", entonces ir cada paso dt era ir continuo)
#comision_volumen = 0.0002   # 0.02% de comisión por mover dinero
#coste_fijo = 0.001 # 0.001€ fijos por cada operación de compra/venta (es como un peaje por cada accion que hagas)

# cáluclo del precio de la opción "V" dependiendo si es compra = C (call), o venta = P (put)
while True:
    tipo_opcion = input("Indica el tipo de opción (C para call, P para put): \n").upper().strip() # pedimos al usuario que indique el tipo de opción, y convertimos la respuesta a mayúsculas para facilitar la comparación || .strip() por si hay error al pomner espacios
    if tipo_opcion == "C" or tipo_opcion == "P":
        break
    else: 
        print("Debe ser C o P \n")

#sigma corregido para la cartera real con las comisiones
factor = 2.2
sigma_corregida = sigma * np.sqrt(1 + factor * np.sqrt(2/np.pi)*comision_volumen/(sigma*np.sqrt(dt*frecuencia_rebalanceo)))
print(f"Sigma corregida: {sigma_corregida:.5f} \n")

# precio de la prima
V0, delta0 = black_scholes(S0, K, T, r, sigma, tipo_opcion)
V0_ajustado, _ = black_scholes(S0, K, T, r, sigma_corregida, tipo_opcion) # luego veremos que diferencia hay entre la prima ajustada y sin ajustar

###############-----############### Lista para almacenar las trayectorias
t = np.linspace(0, T, n_pasos) # la lista comienza con el valor inicial

S = [posicion0] # la lista comienza con el valor inicial || seria S_t
V = [V0_ajustado] # la lista comienza con el valor inicial || Contiene el valor de la prima y los demas V hata el vencimiento son el valor de la opcion en el mercado (puedes vender tu opcion antes del vencimiento )
delta = [delta0] # la lista comienza con el valor inicial || Contiene el valor de la prima y los demas V hata el vencimiento son el valor de la opcion en el mercado
delta_realista = [delta0] # la lista comienza con el valor inicial || contiene lo que debemos tener de acciones pero cada x pasos (realista)

trayectorias = [] # comienza sin nada porque vamos a ir meteiendo trayectorias en la lisa || sería cada trayectoriad de S para diferentes S_t
trayectorias_opciones = [] # comienza sin nada porque vamos a ir meteiendo trayectorias en la lisa || sería cada trayectoria de opciones para diferentes S_t
trayectorias_delta = [] # comienza sin nada porque vamos a ir meteiendo trayectorias en la lisa || sería cada trayectoria de delta para diferentes S_t
trayectorias_delta_realista = [] # simula nuestra varacion de acciones real
trayectorias_cartera = [] # simula nuestra cartera real

print("Calculando trayectorias... por favor espere.")
tiempo_inicio = time.time() #inizializo el tiempo

# Generacion matricial de precios (S)
# En lugar de ir uno a uno, creamos una tabla de (pasos x trayectorias)
Z = np.random.normal(0, 1, (n_pasos - 1, n_trayectorias)) #cada fila es un paso y cada columna es una trayectoria || Z es matriz de nº aleotrios que contienen todos los z para cada trayectoria y cada paso, antes usabamos z = np.random.normal(0,1)
exponente = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z # Z es matriz que contien
camino_log = np.vstack([np.zeros(n_trayectorias), np.cumsum(exponente, axis=0)]) # Concatenamos el inicio (0) y sumamos todos los pasos de golpe
                                                                                 #como epezamos en t = 0, exponente es 0, por ende e^0 = 1. S = S0, por eso el np.zeroes() , np,cumsum() == suma fila 2 con fila 1 y la pega en la 2, suma fila 2 y 3 y la pega en la 3... es decir, suma los pasos 
S_matriz = posicion0 * np.exp(camino_log) # Matriz de Precios #como Sfinal = S0*e^(eponente_0 (paso 0 de todas las tray) + exponente_1(paso 1 de todas las tray) + exponente_2 + ...), por eso hizimos cumsum en el exponente, sino, usar cumprod() 

# Calculo matricial de black-scholes (V y Delta)
# t es tu array de tiempo. Lo ponemos en vertical para que NumPy lo entienda
t_vencimiento = np.maximum(T - t, 0).reshape(-1, 1) #np.maximum() == creamos lista de t_hasta el vencimiento y toma el maximo entre cada elemento y el 0 (es para que si llega a 0.32,.... 0.0001, que no se pete y ponga de repente -0.0000001, de esta manera el 0 es el tope)
                                                    #reshape() == nos pone t_vencimiento de fila a columna (n_pasos x 1 columna)
# Llamamos a tu función enviándole TODA la matriz de precios a la vez
V_matriz, Delta_matriz = black_scholes(S_matriz, K, t_vencimiento, r, sigma, tipo_opcion)

# Cobertura realista (Bucle optimizado) || como ahora 
cartera_real_matriz = np.zeros_like(S_matriz)
cartera_real_matriz_sin_coste_fijo = np.zeros_like(S_matriz)
delta_realista_matriz = np.zeros_like(S_matriz)

# Inicialización t=0 para todas las trayectorias a la vez
acciones_poseidas = np.full(n_trayectorias, delta0) # np.full(forma, valor) te da uuna lista de n_trayectorias elementos con el valor de delta0(es el mismo para todos)
coste_inicial = (np.abs(delta0) * posicion0 * comision_volumen) + coste_fijo
efectivo = V0_ajustado - (delta0 * posicion0) - coste_inicial
efectivo_sin_coste_fijo = V0_ajustado - (delta0 * posicion0) - (np.abs(delta0) * posicion0 * comision_volumen) 

cartera_real_matriz[0] = V0_ajustado
cartera_real_matriz_sin_coste_fijo[0] = V0_ajustado
delta_realista_matriz[0] = delta0

for i in range(1, n_pasos): # ahora delta_teorico_t, ajsute_delta, coste_tx, efectivo, acciones_poseidas, son listas con las 100 trayectorias (ahorramos tiempo)
    S_t = S_matriz[i]
    efectivo = efectivo * np.exp(r * dt) # Interés del efectivo
    efectivo_sin_coste_fijo = efectivo_sin_coste_fijo * np.exp(r * dt) # Interés del efectivo
    
    if i % frecuencia_rebalanceo == 0 or i == n_pasos - 1: #acutualizamos cada x pasos + el ultimo paso
        delta_teorico_t = Delta_matriz[i] #cada fila son el paso i para las 100 trayectorias
        ajuste_delta = delta_teorico_t - acciones_poseidas # te dice ==> hace x pasos yo tenia acciones_poseidas, pero tras esos x pasos el modelo me dice que debo tener delta_t, asique compro/vendo ajuste_delta
        
        # si alguna trayectoria del ajuste necesita comprar/vender acciones, entonces hay comisiones
        tolerancia = 1e-6
        operaciones_comisiones = (np.abs(ajuste_delta) > tolerancia).astype(int) # si el ajuste es mayor a la tolerancia, te devuelve true, si no, da false || .astype(int) convierte False a 0 y True a 1

        coste_tx = (np.abs(ajuste_delta) * S_t * comision_volumen) + coste_fijo*operaciones_comisiones # coste total de las transacciones de compra/venta de acciones || coste fijo solo se aplica si ha habido compra/venta
        coste_tx_sin_coste_fijo = (np.abs(ajuste_delta) * S_t * comision_volumen) # coste total de las transacciones de compra/venta de acciones 
        efectivo = efectivo - (ajuste_delta * S_t + coste_tx)
        efectivo_sin_coste_fijo = efectivo_sin_coste_fijo - (ajuste_delta * S_t + coste_tx_sin_coste_fijo)

        acciones_poseidas = delta_teorico_t # al hacer el ajuste (comprar/vender acciones), ajora tengo lo que el modelo ideal dice que deberia tener
        
    cartera_real_matriz[i] = (acciones_poseidas * S_t) + efectivo
    cartera_real_matriz_sin_coste_fijo[i] = (acciones_poseidas * S_t) + efectivo_sin_coste_fijo # nos serivirá para ver la diferencia entre poner y no poner costes fijos en los plots
    delta_realista_matriz[i] = acciones_poseidas
    #print(cartera_real_matriz[i])


# CONVERSIÓN A TUS LISTAS ORIGINALES
# .T.tolist() convierte la matriz en la lista de trayectorias que tus gráficas esperan
trayectorias = S_matriz.T.tolist()
trayectorias_opciones = V_matriz.T.tolist()
trayectorias_delta = Delta_matriz.T.tolist()
trayectorias_cartera = cartera_real_matriz.T.tolist()
trayectorias_cartera_sin_coste_fijo = cartera_real_matriz_sin_coste_fijo.T.tolist()
trayectorias_delta_realista = delta_realista_matriz.T.tolist()

print(f"Simulacion desde t=0 hasta t={T}\n")

tiempo_fin = time.time()
duracion = tiempo_fin - tiempo_inicio
print(f"Tiempo total de simulación: {duracion} segundos")

###############-----############### Graficamos figura 1 (movimiento browniano geometrico)
tiempo_inicio_graficas = time.time()

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
opcion_inicial, = ax_opciones.plot(t, np.full_like(t, V0), color='purple', lw=2, zorder=10, label = f"Precio de la prima{V0:.4f}")   
for i in range(len(trayectorias_opciones)): 
    ax_opciones.plot(t, trayectorias_opciones[i], lw=1, alpha=0.5)

# Calculamos la mediana para cada paso de tiempo (eje de las trayectorias)
mediana_opciones, = ax_opciones.plot(t, np.median(trayectorias_opciones, axis=0), color='blue', lw=2, label='Mediana de la Opción', zorder=10)

ax_opciones.set_title(f"Evolución del valor de la Opción ({tipo_opcion})\n"
                      rf"Strike K={K}; Tasa r={r}; Volatilidad $\sigma$={sigma}; V_{{0}}={V0:.4f}; V_{{ajustado}}={V0_ajustado:.4f}")
ax_opciones.set_xlabel("Tiempo (años)")
ax_opciones.set_ylabel("Precio de la Opción (€)")
ax_opciones.grid(True, alpha=0.3)

# Añadimos una línea en el 0 para ver claramente cuáles expiran sin valor
ax_opciones.axhline(0, color='black', lw=1, zorder=10)

# legenda1
ax_opciones.legend(handles=[opcion_inicial, mediana_opciones]) 

time_inicio_prueba = time.time()
###############-----############### Graficamos FIGURA 3 (Delta vs precio) y (Delta vs tiempo)
fig3 = plt.figure(figsize=(14, 10))
plt.suptitle(r"Evolución de $\Delta$")
############### Delta vs precio(ideal)
ax_deltas = fig3.add_subplot(221)

# Plot de todas las trayectorias de las opciones
if tipo_opcion == "C":
    delta_inferior = ax_deltas.axhline(0, color='red', linestyle='--', alpha=0.5, label = r"límite $\Delta$ inferior")
    delta_superior = ax_deltas.axhline(1, color='green', linestyle='--', alpha=0.5, label = r"límite $\Delta$ superior")
else:
    delta_inferior = ax_deltas.axhline(-1, color='red', linestyle='--', alpha=0.5, label = r"límite $\Delta$ inferior")
    delta_superior = ax_deltas.axhline(0, color='green', linestyle='--', alpha=0.5, label = r"límite $\Delta$ superior")

cmap = plt.get_cmap('viridis') #viridis , winter, plasma, inferno, magma, cividis, Greys, Purples, Blues, Greens, Oranges, Reds, YlOrBr, YlOrRd, OrRd, PuRd, RdPu, BuPu, GnBu, PuBu, YlGnBu, PuBuGn, BuGn, YlGn
norm = colors.Normalize(vmin=t.min(), vmax=t.max())

paso_muestreo = 1 # 10 puntos por trayectoria
Todas_trayectorias = []
todos_los_tiempos = []

for i in range(len(trayectorias_delta)):
    S_i = trayectorias[i][::paso_muestreo]
    D_i = trayectorias_delta[i][::paso_muestreo]
    t_i = t[::paso_muestreo]
    
    # Creamos los puntos y segmentos para esta trayectoria
    puntos = np.array([S_i, D_i]).T.reshape(-1, 1, 2)
    segmentos = np.concatenate([puntos[:-1], puntos[1:]], axis=1)
    
    Todas_trayectorias.append(segmentos)
    todos_los_tiempos.append(t_i[:-1])

# Esto es lo que hace que sea instantáneo
trayectorias_finales = np.concatenate(Todas_trayectorias)
tiempos_finales = np.concatenate(todos_los_tiempos)

# Crea 1 coleccion (En lugar de 1 para cada trayectoria)
lc = LineCollection(trayectorias_finales, cmap='viridis', norm=norm, rasterized=False)
lc.set_array(tiempos_finales)
lc.set_linewidth(0.5)
lc.set_alpha(0.4)

# 4. Añadimos al gráfico una sola vez
ax_deltas.add_collection(lc)

# Calculamos la curva teórica de delta
S_min = np.min(trayectorias)
S_max = np.max(trayectorias)
S_limite = np.linspace(S_min, S_max, n_pasos) # al igual que para tiempos lo teniamos ordenado, para S igual

deltas_teoricos = [black_scholes(s, K, T, r, sigma, tipo_opcion)[1] for s in S_limite]

# Graficamos curva teórica
curva_teorica, = ax_deltas.plot(S_limite, deltas_teoricos, color='purple', alpha = 0.9, lw=2.5, label=r"$\Delta$ Teórico (Black-Scholes) para $t_v$ = T", zorder=100)# zorder=10 para que la curva teórica no se superponga sobre la curva de la cobertura

ax_deltas.set_title(rf"$\Delta$ en modelo ideal"                
                    f"\n Strike K={K}; Tasa r={r}; Volatilidad $\sigma$={sigma}")
ax_deltas.set_xlabel("Precio (€)")
ax_deltas.set_ylabel(r"$\Delta (acciones)$")
ax_deltas.grid(True, alpha=0.3)

# legenda1
ax_deltas.legend(handles=[delta_inferior, delta_superior, curva_teorica]) 

#mapa con colores 
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([]) # Esto es necesario para matplotlib

cbar = fig3.colorbar(sm, ax=ax_deltas, pad=0.05) 
cbar.set_label('Tiempo transcurrido (años)')

############### Delta vs tiempo (ideal)
ay_deltas = fig3.add_subplot(222)

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
ay_deltas.set_title(rf"$\Delta$ en modelo ideal"            
                    f"\n Strike K={K}; Tasa r={r}; Volatilidad $\sigma$={sigma}")
ay_deltas.set_xlabel("Tiempo (años)")
ay_deltas.set_ylabel(r"$\Delta (acciones)$")
ay_deltas.grid(True, alpha=0.3)
ay_deltas.legend(loc='best')

############### Delta vs precio(realista)
ax_deltas_realista = fig3.add_subplot(223)

# Plot de todas las trayectorias de las opciones
if tipo_opcion == "C":
    delta_inferior = ax_deltas_realista.axhline(0, color='red', linestyle='--', alpha=0.5, label = r"límite $\Delta$ inferior")
    delta_superior = ax_deltas_realista.axhline(1, color='green', linestyle='--', alpha=0.5, label = r"límite $\Delta$ superior")
else:
    delta_inferior = ax_deltas_realista.axhline(-1, color='red', linestyle='--', alpha=0.5, label = r"límite $\Delta$ inferior")
    delta_superior = ax_deltas_realista.axhline(0, color='green', linestyle='--', alpha=0.5, label = r"límite $\Delta$ superior")

cmap = plt.get_cmap('viridis') #viridis , winter, plasma, inferno, magma, cividis, Greys, Purples, Blues, Greens, Oranges, Reds, YlOrBr, YlOrRd, OrRd, PuRd, RdPu, BuPu, GnBu, PuBu, YlGnBu, PuBuGn, BuGn, YlGn
norm = colors.Normalize(vmin=t.min(), vmax=t.max())

todos_los_segmentos_real = []
todos_los_tiempos_real = []
paso_muestreo = 1 # Mantén el mismo que en el ideal para que sean comparables

for i in range(len(trayectorias_delta)):
    # TRUCO: Muestreo para no saturar la memoria
    S_i = trayectorias[i][::paso_muestreo]
    Delta_r_i = trayectorias_delta_realista[i][::paso_muestreo]
    t_i = t[::paso_muestreo]
    
    # Creamos puntos y segmentos para esta trayectoria específica
    puntos = np.array([S_i, Delta_r_i]).T.reshape(-1, 1, 2)
    segmentos = np.concatenate([puntos[:-1], puntos[1:]], axis=1)
    
    todos_los_segmentos_real.append(segmentos)
    todos_los_tiempos_real.append(t_i[:-1])

# Esto convierte 100 listas en un solo bloque gigante de datos
final_segments_real = np.concatenate(todos_los_segmentos_real)
final_tiempos_real = np.concatenate(todos_los_tiempos_real)

# Colección única con todas las trayectorias
lc_real = LineCollection(final_segments_real, cmap='viridis', norm=norm, rasterized=False) #rasterized=True para que al cargar el png y moverte en el sea mucho mas rapido
lc_real.set_array(final_tiempos_real)
lc_real.set_linewidth(0.5)
lc_real.set_alpha(0.4)

# Añado solo una operación e dibujado
ax_deltas_realista.add_collection(lc_real)

# Calculamos la curva teórica de delta
S_min = np.min(trayectorias)
S_max = np.max(trayectorias)
S_limite = np.linspace(S_min, S_max, n_pasos) # al igual que para tiempos lo teniamos ordenado, para S igual

deltas_teoricos = [black_scholes(s, K, T, r, sigma, tipo_opcion)[1] for s in S_limite]

# Graficamos curva teórica
curva_teorica, = ax_deltas_realista.plot(S_limite, deltas_teoricos, color='purple', alpha = 0.9, lw=2.5, label=r"$\Delta$ Teórico (Black-Scholes) para $t_v$ = T", zorder=100)# zorder=10 para que la curva teórica no se superponga sobre la curva de la cobertura

ax_deltas_realista.set_title(rf"$\Delta$ en modelo realsita"                
                    f"\n Strike K={K}; Tasa r={r}; Volatilidad $\sigma$={sigma}")
ax_deltas_realista.set_xlabel("Precio (€)")
ax_deltas_realista.set_ylabel(r"$\Delta (acciones)$")
ax_deltas_realista.grid(True, alpha=0.3)

# legenda1
ax_deltas_realista.legend(handles=[delta_inferior, delta_superior, curva_teorica]) 

#mapa con colores 
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([]) # Esto es necesario para matplotlib

cbar = fig3.colorbar(sm, ax=ax_deltas_realista, pad=0.05)
cbar.set_label('Tiempo transcurrido (años)')

############### Delta vs tiempo (realista)
ay_deltas_realista = fig3.add_subplot(224)

for i in range(len(trayectorias_delta)): 
    ay_deltas_realista.plot(t, trayectorias_delta_realista[i], lw=0.5)

# mediana
mediana_delta_realista = np.median(trayectorias_delta_realista, axis=0)
ay_deltas_realista.plot(t, mediana_delta_realista, color='black', lw=1, zorder=10, label = r"Mediana $\Delta$") # zorder=10 para que la linea de media no se superponga sobre la curva

# Añadimos líneas de referencia en 0 y 1 (límites de la Delta para Call)
if tipo_opcion == "C":
    ay_deltas_realista.axhline(0, color='red', linestyle='--', alpha=0.5, label = r"límite $\Delta$ inferior")
    ay_deltas_realista.axhline(1, color='green', linestyle='--', alpha=0.5, label = r"límite $\Delta$ superior")
else:
    ay_deltas_realista.axhline(-1, color='red', linestyle='--', alpha=0.5, label = r"límite $\Delta$ inferior")
    ay_deltas_realista.axhline(0, color='green', linestyle='--', alpha=0.5, label = r"límite $\Delta$ superior")

# ajustes
ay_deltas_realista.set_title(rf"$\Delta$ en modelo realsita"                
                    f"\n Strike K={K}; Tasa r={r}; Volatilidad $\sigma$={sigma}")
ay_deltas_realista.set_xlabel("Tiempo (años)")
ay_deltas_realista.set_ylabel(r"$\Delta (acciones)$")
ay_deltas_realista.grid(True, alpha=0.3)
ay_deltas_realista.legend(loc='best')

plt.tight_layout()# Ajuste automático para que no se solapen los ejes de los dos gráficos

time_fin_prueba = time.time()
duracion_prueba = time_fin_prueba - time_inicio_prueba
print(f"Tiempo total de cálculos de delta: {duracion_prueba} segundos")
###############-----############### CÁLCULO DE RESIDUOS (como de bien el modelo se acerca a la realidad supuesta) == lo que gana o pierde el lanzador (como un banco)
##### Modelo ideal
print("\n" + "="*50)
print("ANÁLISIS DE EFICIENCIA DE LA COBERTURA IDEAL")
print("="*50)

errores_ideales = []
S_finales = S_matriz[-1] #precios finales de cada trayectoria
V_finales = V_matriz[-1] #valores de cobertura finales de cada trayectoria

if tipo_opcion == "C":
    payoff_real = np.maximum(0, S_finales - K)
else:
    payoff_real = np.maximum(0, K - S_finales) 

errores_ideales = V_finales - payoff_real

# Estadísticas del error
error_medio = np.mean(errores_ideales)
error_std = np.std(errores_ideales)
error_mediana = np.median(errores_ideales)

print(f"Número de trayectorias: {n_trayectorias}")
print(f"Error medio de cobertura: {error_medio:.4f} €")
print(f"Desviación típica del error: {error_std:.4f} €")
print(f"Mediana del error: {error_mediana:.4f} €")
print(f"El error máximo fue de: {np.max(np.abs(errores_ideales)):.4f} €")
print("="*50 + "\n") # para seprar con ==============

##### Modelo realista(costes totales)
print("\n" + "="*50)
print("ANÁLISIS DE EFICIENCIA DE LA COBERTURA REALISTA")
print("="*50)

errores_realista = []
cartera_real = cartera_real_matriz[-1] #valores de cartera real de cada trayectoria

if tipo_opcion == "C":
    payoff_real = np.maximum(0, S_finales - K)
else:
    payoff_real = np.maximum(0, K - S_finales) 

errores_realista = cartera_real - payoff_real

# Estadísticas del error
error_mediana_realista = np.median(errores_realista)
error_medio_realista = np.mean(errores_realista)
error_std_realista = np.std(errores_realista)

print(f"Número de trayectorias: {n_trayectorias}")
print(f"Error medio de cobertura: {error_medio_realista:.4f} €")
print(f"Desviación típica del error: {error_std_realista:.4f} €")
print(f"Mediana del error: {error_mediana_realista:.4f} €")
print(f"El error máximo fue de: {np.max(np.abs(errores_realista)):.4f} €")
print("="*50 + "\n") # para seprar con ==============

##### Modelo realista(solo costes por volumen, soin costes fijos)
print("\n" + "="*50)
print("ANÁLISIS DE EFICIENCIA DE LA COBERTURA REALISTA (sin coste fijo)")
print("="*50)

errores_realista_sin_coste_fijo = []
cartera_real_matriz_sin_coste_fijo = cartera_real_matriz_sin_coste_fijo[-1] #valores de cartera real sin coste fijo de cada trayectoria

if tipo_opcion == "C":
    payoff_real = np.maximum(0, S_finales - K)
else:
    payoff_real = np.maximum(0, K - S_finales) 

errores_realista_sin_coste_fijo = cartera_real_matriz_sin_coste_fijo - payoff_real

# Estadísticas del error
error_mediana_realista_sin_coste_fijo = np.median(errores_realista_sin_coste_fijo)
error_medio_realista_sin_coste_fijo = np.mean(errores_realista_sin_coste_fijo)
error_std_realista_sin_coste_fijo = np.std(errores_realista_sin_coste_fijo)

print(f"Número de trayectorias: {n_trayectorias}")
print(f"Error medio de cobertura: {error_medio_realista_sin_coste_fijo:.4f} €")
print(f"Desviación típica del error: {error_std_realista_sin_coste_fijo:.4f} €")
print(f"Mediana del error: {error_mediana_realista_sin_coste_fijo:.4f} €")
print(f"El error máximo fue de: {np.max(np.abs(errores_realista_sin_coste_fijo)):.4f} €")
print("="*50 + "\n") # para seprar con ==============

###############-----############### Gráfica 4 de Residuos
fig4 = plt.figure(figsize=(20, 6))
plt.suptitle("Análisis de los errores de Cobertura (Residuos) \n"
             rf"$\sigma_{{corregido}}$: {sigma_corregida:.5f} ; $V_{{corregido}}$: {V0_ajustado:.4f}")

##### Para el ideal
ax_res = fig4.add_subplot(131)
mask_itm = payoff_real > 0
mask_otm = ~mask_itm

ax_res.scatter(S_finales[mask_itm], errores_ideales[mask_itm], color='royalblue', edgecolors='black', label='ITM')
ax_res.scatter(S_finales[mask_otm], errores_ideales[mask_otm], color='gold', edgecolors='black', label='OTM')
ax_res.axhline(0, color='red', linestyle='--', lw=2)
ax_res.set_title("Modelo Ideal")
ax_res.set_xlabel("Precio final del activo (€)")
ax_res.set_ylabel("Payoff neto de la cartera de cobertura (€)")
ax_res.legend()

##### Para el realista (sin csotes fijos)
ax_res_realista_sin_coste_fijo = fig4.add_subplot(132)
ax_res_realista_sin_coste_fijo.scatter(S_finales[mask_itm], errores_realista_sin_coste_fijo[mask_itm], color='royalblue', edgecolors='black', label='ITM')
ax_res_realista_sin_coste_fijo.scatter(S_finales[mask_otm], errores_realista_sin_coste_fijo[mask_otm], color='gold', edgecolors='black', label='OTM')
ax_res_realista_sin_coste_fijo.axhline(0, color='red', linestyle='--', lw=2)
ax_res_realista_sin_coste_fijo.axhline(error_mediana_realista_sin_coste_fijo, color='purple', linestyle=':', label=f'Mediana: {error_mediana_realista_sin_coste_fijo:.2f}')
ax_res_realista_sin_coste_fijo.set_title("Modelo Realista con costes por volumen (sin costes fijos)")
ax_res_realista_sin_coste_fijo.set_xlabel("Precio final del activo (€)")
ax_res_realista_sin_coste_fijo.set_ylabel("Payoff neto de la cartera de cobertura (€)")
ax_res_realista_sin_coste_fijo.legend()

##### Para el realista
ax_res_realista = fig4.add_subplot(133)
ax_res_realista.scatter(S_finales[mask_itm], errores_realista[mask_itm], color='royalblue', edgecolors='black', label='ITM')
ax_res_realista.scatter(S_finales[mask_otm], errores_realista[mask_otm], color='gold', edgecolors='black', label='OTM')
ax_res_realista.axhline(0, color='red', linestyle='--', lw=2)
ax_res_realista.axhline(error_mediana_realista, color='purple', linestyle=':', label=f'Mediana: {error_mediana_realista:.2f}')
ax_res_realista.set_title("Modelo Realista con costes por volumen y costes fijos")
ax_res_realista.set_xlabel("Precio final del activo (€)")
ax_res_realista.set_ylabel("Payoff neto de la cartera de cobertura (€)")
ax_res_realista.legend()

plt.tight_layout()
###############-----############### FIGURA 5: Payoff neto (P&L de Cobertura)
fig5 = plt.figure(figsize=(10, 6))
ax_pay = fig5.add_subplot(111)

# Creamos una línea continua para el Payoff Teórico
s_min_plot = np.min(S_finales) * 0.8
s_max_plot = np.max(S_finales) * 1.2
s_rango = np.linspace(s_min_plot, s_max_plot, n_pasos)

# Calculamos el payoff teórico
if tipo_opcion == "C":
    payoff_teorico = np.maximum(0, s_rango - K)
else: #si es put P(venta)
    payoff_teorico = np.maximum(0, K - s_rango)

ax_pay.plot(s_rango, payoff_teorico - V0, color='black', lw=2, label="Payoff neto (€)", zorder=1) # line que va----- / de esa manera y es el teórico

# Calculamos los pagos
payoff_neto = payoff_real - V0

# Puntos ITM (Azules)
ax_pay.scatter(S_finales[mask_itm], payoff_neto[mask_itm], #S_finales[mask_itm] lista de precios finales de cada trayectoria que es ITM
               color='royalblue', s=100, edgecolors='black', 
               label=f"Pago Real (ITM) - {np.sum(mask_itm)} tray.", zorder=2) #np.sum(mask_itm) nos suma los trues=1 y los falses=0 de cada trayectoria 1+1+0+1 = 3 (por ej)

# Puntos OTM (Amarillos)
ax_pay.scatter(S_finales[mask_otm], payoff_neto[mask_otm], 
               color='gold', s=80, edgecolors='black', 
               label=f"Sin Pago (OTM) - {np.sum(mask_otm)} tray.", zorder=2)

# mediana
S_final_mediana = posicion0 * np.exp((mu - 0.5 * sigma**2) * T) #mediana de los precios
if tipo_opcion == "C":
    beneficio_mediana = max(0, S_final_mediana - K) - V0 # mediana de los beneficios netos
else: # si es put
    beneficio_mediana = max(0, K - S_final_mediana) - V0 # mediana de los beneficios netos
ax_pay.scatter(S_final_mediana, beneficio_mediana, color='purple', s=100, edgecolors='black', label="Mediana", zorder=2) #punto que es la mediana en el precio mediana

# Ajustes gráfica
ax_pay.set_title(f"Payoff neto del cliente al vencimiento \nStrike K={K}")
ax_pay.set_xlabel("Precio Final del Activo ($S_T$) (€)")
ax_pay.set_ylabel("Payoff neto (€)")
ax_pay.axvline(K, color='red', linestyle='--', alpha=0.5, label=f"Strike K={K}")
ax_pay.grid(True, alpha=0.3)
ax_pay.legend()

##### vemos duracione de calculos de datos para las graficas
tiempo_fin_graficas = time.time()
duracion_graficas = tiempo_fin_graficas - tiempo_inicio_graficas
print(f"Tiempo total de cálucos de graficas: {duracion_graficas} segundos")


###############-----############### Guardo datos + visualizar primeras filas
while True: #calulamos el valor de r anual
    opcion_guardar = input("¿Desea guardar las figuras en formaro png? (y), o no (n): \n").upper().strip()

    if opcion_guardar == "Y" or opcion_guardar == "N":
        break
    else:
        print("Pulse sólo (Y/y) o (N/n) \n")

time_inicio_guardado = time.time()

if opcion_guardar == "Y":
########## Guardamos figuras
    print("guardando figuras, y datos en formato Excel (csv)...")
    
    # Guardo la imagen en "plots" :
    directorio_del_script = os.path.dirname(os.path.abspath(__file__)) #nos da la ruta donde esta el .py
    ruta_plots = os.path.join(directorio_del_script, "plots_black_scholes_realista_corregido") #para guardar el archivo en la carpeta donde esta el .py

    if not os.path.exists(ruta_plots): #si no existe la carpeta plots, la creemos
        os.makedirs(ruta_plots) #creamos la carpeta plots
        print(f"Carpeta plots creada en: {ruta_plots} \n")

    # Guardamos imageN de movimiento browniano geometrico (precios en el tiempo)
    ruta_precios = os.path.join(ruta_plots, "mov_browniano_geometrico(png).png")
    fig.savefig(ruta_precios, dpi=100)
    print(f"Figura (mov_browniano_geometrico(png).png) guardada en: {ruta_precios} \n")

    #Guardamos imagen de opciones
    nombre_archivo_opcion = "precio_opciones_con_el_tiempo(png).png"
    ruta_guardado_opcion = os.path.join(ruta_plots, nombre_archivo_opcion)
    fig2.savefig(ruta_guardado_opcion, dpi=100)
    print(f"Figura (precio_opciones_con_el_tiempo(png).png) guardada en: {ruta_guardado_opcion} \n")

    #Guardamos imagen de deltas
    ruta_deltas = os.path.join(ruta_plots, "cobertura_dinamica(png).png")
    fig3.savefig(ruta_deltas, dpi=100)
    print(f"Figura (cobertura_dinamica(png).png) guardada en: {ruta_deltas} \n")

    # Guardamos imagen payoff neto vendedor(residuos) (lo que gana el banco)
    ruta_res = os.path.join(ruta_plots, "payoff_neto_cartera_cobertura(residuos)(png).png")
    fig4.savefig(ruta_res, dpi=100)
    print(f"Figura (payoff_neto_cartera_cobertura(residuos)(png).png) guardada en: {ruta_res} \n")

    # Guardamos imagen de payoff neto
    ruta_payoff = os.path.join(ruta_plots, "payoff_neto_cliente(png).png")
    fig5.savefig(ruta_payoff, dpi=100)
    print(f"Figura (payoff_neto_cliente(png).png) guardada en: {ruta_payoff} \n")

else:
    print("Datos no guardados \n")

if guardar_csv: #cambiar la linea 20 (False ==> True) para guardar los datos en formato Excel (csv) || falta alguna cosa que añadir como lo no idea, pero como ya se sabe la semilla, no seria necesario pues el nº de trayectorias podria hacer los excels muy pesados
########## Guardamos datos en csv
    # Preparamos la matriz (Tiempo + Trayectorias de precios + semilla) y (Tiempo + Trayectorias de popciones + semilla)
    semilla_columna = [semilla]*len(t) # [convierte semilla en una lista de la misma longitud que tiempo]

    matriz_para_guardar = np.column_stack([np.array(t), np.array(trayectorias).T, np.array(semilla_columna)]) # nos junta el vector tiempo con la matriz de trayectorias

    matriz_para_guardar_opciones = np.column_stack([np.array(t), np.array(trayectorias_opciones).T, np.array(semilla_columna)]) 
    #matriz para guardar delta vs precio y delta vs tiempo
    # 1. Base Común (Las columnas de referencia)
    matriz_para_guardar_deltas = np.column_stack([np.array(t), np.array(S_limite).T, np.array(deltas_teoricos), np.array(trayectorias_delta).T, np.array(semilla_columna)]) # suamos S_limite porque esta ordenado [minimo,...81, 82... hata el max]

    s_t_final_itm = S_finales[mask_itm] 
    s_t_final_otm = S_finales[mask_otm]
    todos_los_S_final = np.concatenate([s_t_final_itm, s_t_final_otm]) # creamos lista con precios finales [primero todos los que son ITM y luego todos los que son OTM] || si hiciesemos trayectorias[i][-1] for i in range(n_trayectorias). hacemos [ordenar por orden de trayectorias] mezclas ITM con OTM
    errores_itm = errores_ideales[mask_itm]
    errores_otm = errores_ideales[mask_otm]
    todos_los_errores = np.concatenate([errores_itm, errores_otm])
    pagos_itm = payoff_neto[mask_itm]
    pagos_otm = payoff_neto[mask_otm]
    payoff_neto_final = np.concatenate([pagos_itm, pagos_otm])
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

    ##### Vemos tiempo total de guardado
    time_fin_guardado = time.time()
    duracion_guardado = time_fin_guardado - time_inicio_guardado
    print(f"Tiempo total de guardado: {duracion_guardado} segundos")


#mostramos
plt.show()