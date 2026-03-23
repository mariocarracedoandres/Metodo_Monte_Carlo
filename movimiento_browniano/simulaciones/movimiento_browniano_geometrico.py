####################################################
# movimiento_browniano_geométrico.py
# Author: Mario Carracedo Andres
# Year: 2026
# License: MIT
# Description: Muestra el comportamiento aleatorio del movimiento browniano geometrico para varias trayectorias
####################################################

import numpy as np # para cálculos numéricos
import matplotlib.pyplot as plt # para gráficos
import pandas as pd # para manejar datos en formato de tablas (dataframes)
import time # para tiempos
import random # para números aleatorios
import os # para obtener el directorio de trabajo

####################################################################### FUNCIONES AUXILIARES
###############-----############### Semilla aleatoria
def seed():
    """
    Nos da un numero entero muy grande dependeiendo de la hora local, como nunca podremos repetir esa msima hora pues el timepo avanza,
    Se considera al seed como una fomra de generar numeros aleatorios.
    """
    ns = time.monotonic() * 1e9 # obtenemos el tiempo local en nanosegundos
    return int(ns % (2**32)) # devolvemos el tiempo como un entero, modulo 2^32 para asegurarnos de que el número no sea demasiado grande para el generador de números aleatorios, que suele aceptar semillas de hasta 32 bits (0 a 2^32-1)

################-----############### Escala de numeros aleatorios
def scalerandom(rn, a, b):
    """
    Scales a random number from [0,1] to [a,b].
    rn: random number in [0,1]
    a: lower bound
    b: upper bound
    Returns: scaled number in [a,b]
    """
    return a + (b-a)*rn # (b-a) distancia de a a b, al multiplcar por rn, nos da una distancia aletoira de a á b, asi pasamos de [0,1] a [a,b] 
    
####################################################################### PROGRAMA PRICIPAL
###############-----############### Inicializamos la semilla
semilla = seed() # generamos una semilla aleatoria
#random.seed(40) # random.seed() inizializa el generador de numeros con una semilla especifica, como dentro va nuestra funcion seed(), esa es aletoria y nunca se repite || se puede poner radnom.seed(numero que quieras) para generar el mismo movimiento
np.random.seed(semilla) # np.random.seed() hace lo mismo que justo el de la linea de arriba, pero usa esa semilla para todo lo aleatorio de numpy, es decir todo lo de np.cosas. si no se pone, no habrá reproducibilidad en los resultados.

###############-----############### Parámetros

# Tamaño del paso temporal / dt = desviación tipica 
dt = 0.01  #segundos
tiempo_maximo =float(input("Indica timepo máximo: \n")) # tiempo maximo de simulación
n_pasos = int(tiempo_maximo/dt + 1) #+1 es porqu el range acabe en n_pasos-1
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
        entrada = input("Indica posición inicial: \n")# posición inicial
        posicion0 = float(entrada)

        if posicion0 == float(entrada) and posicion0 > 0:
            break
        else:
            print("La posición inicial debe ser un número real > 0 \n")

    except ValueError: #se ejecuta si no es float > 0
            print("La posición inicial debe ser un número real > 0 \n")


# Parametros para contolar tendencia en el movimiento
mu = float(input("Indica la tendencia (mu=valor esperado/unidad de tiempo): \n")) # tendencia del movimiento, si es positiva, la partícula tiende a moverse hacia arriba, si es negativa, tiende a moverse hacia abajo, si es 0, no hay tendencia y el movimiento es completamente aleatorio
sigma = float(input("Indica la volatilidad (sigma=desviación típica): \n")) # volatilidad del movimiento, si es alta, la partícula se mueve más lejos de su posición actual, si es baja, se mueve menos lejos
# se puede interpertar con que si tu te esperas un valor de mu, lo normal es que si se desvia, se desvie +-sigma

###############-----############### Lista para almacenar la trayectoria
posiciones = [posicion0] # la lista comienza con el valor inicial
t = np.linspace(0, tiempo_maximo, n_pasos) # la lista comienza con el valor inicial
trayectorias = [] # comienza sin nada porque vamos a ir meteiendo trayectorias en la lista

for j in range(1, n_trayectorias+1):
    posiciones = [posicion0] # la lista comienza con el valor inicial
    for i in range(1, n_pasos): # tiempo_maximo + 1 porque el tiempo 0 no se incluye en la lista
        tiempo_actual = i*dt

        z = np.random.normal(0, 1) # generamos un numero aleatorio de la distribución normal

        posicion_nueva = posiciones[-1]*np.exp((mu-sigma**2/2)*dt + sigma*np.sqrt(dt)*z) # posicion ultima + salto aleatorio
        posiciones.append(posicion_nueva) # guardamos la nueva posicion en la lista de posiciones

    trayectorias.append(posiciones) # guardamos una trayectroia en una lista de treyectorias
    #guardamos los resultados de la primer iteración

print(f"Simulacion desde t=0 hasta t={tiempo_maximo}\n")

###############-----############### Graficamos
fig = plt.figure()
fig_ax = fig.add_subplot(111)

# plot de todas las trayectorias
for i in range(len(trayectorias)): #listas van de 0 a n_trayectorias-1 == trayectorias[0] = trayectorias 1 ..... trayectorias[49] = trayectorias 50, por eso el +1 en el label, pero el 1 en el plot interno
        fig_ax.plot(t, trayectorias[i],lw = 1, alpha = 0.5)


fig_ax.set_title(f"Movimiento Browniano (Monte Carlo) para {n_trayectorias} trayectorias\n"
                 f"Tendencia: mu={mu}; Volatilidad: sigma={sigma}; Semilla: {semilla}")
fig_ax.set_xlabel("Tiempo (años)")
fig_ax.set_ylabel("Precios (€)")
fig_ax.grid(True)

# lo que se va a plotear
t = np.array(t) # convertimos la lista de tiempos a un array de numpy para facilitar el manejo

#eje_x = fig_ax.axhline(0, color='black', alpha = 0.5, label = "y=0") # línea horizontal en y=0 para referencia || ya devuelve un unico objeto

eje_inicial, = fig_ax.plot(t, np.full_like(t, posicion0), color = "black", alpha = 0.5,label = "Posición inicial") # graficamos la posición inicial
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

###############-----############### Guardo la imagen en "plots" : quitar el # a lo de abajo si quiero guardar la animacion en la carpeta donde esta el .py
directorio_del_script = os.path.dirname(os.path.abspath(__file__)) #nos da la ruta donde esta el .py
ruta_plots = os.path.join(directorio_del_script, "plots") #para guardar el archivo en la carpeta donde esta el .py

if not os.path.exists(ruta_plots): #si no existe la carpeta plots, la creemos
    os.makedirs(ruta_plots) #creamos la carpeta plots
    print(f"Carpeta plots creada en: {ruta_plots} \n")
    
#Guardamos imagen (no quitar este #)
nombre_archivo_imagen = "movimiento_browniano_geometrico(png).png" #nombre de archivo a guardar como imagen
ruta_guardado_imagen = os.path.join(ruta_plots, nombre_archivo_imagen) #(carpeta, cosa que metes en carpeta) para obtener la ruta completa del archivo

fig.savefig(ruta_guardado_imagen, dpi=200) #esto es para guardar la imagen, con el nombre y la ruta que hemos definido antes, y con el dpi(pixeles por pulgada)
print(f"Imagen guardada como: {nombre_archivo_imagen}\n")
print(f"Archivo guardado en: {ruta_guardado_imagen}\n")


#vemos datos en consola
Y = input("Desea ver los datos en consola (y), o no (n)? \n")
if Y == "y" or Y == "Y":
    # Imprimimos cabecera
    print(f"{'Paso':<8} | {'Tiempo (s)':<12} |", end="") # ponmos paso y tiempo y espacio para poner ytayect 1, 2 ...
    for j in range(n_trayectorias): # para poner trayectorias 1, 2, 3 ... n_trayectorias
        print(f" | {'Trayect. ' + str(j+1):<12}", end="") # end="" para que no haga salto de línea después de imprimir cada trayectoria
                                                          # str(j+1) convierte el número a string, asi podemos sumarlo a trayect, :<12 es para que el texto se ajuste a 12 caracteres alineado a la izq (<)
    print(f" | Semilla ", end="")

    print("\n" + "-" * (25 + 15 * n_trayectorias + 15))  #te pone mini lineas horizontales para separarlo de los datos                                                                        

    # Recorremos cada paso de tiempo
    for i in range(n_pasos):
        print(f"{i:<8} | {t[i]:<12.2f} |", end="") # end="" para que no haga salto de línea después de imprimir el tiempo
                                                   # f":[alineacion (<,^,>)][ancho(12; 8...)].[decimales(2)][tipo()]""
        # Para cada paso, imprimimos el valor de cada trayectoria para 
        for j in range(n_trayectorias):
            valor = trayectorias[j][i]
            print(f" | {valor:<12.4f}", end="") # end="" para que no haga salto de línea después de cada valor
        
        print(f" | {semilla:<12.0f}", end="")

        print() # Salto de línea para el siguiente paso

# Guardar datos + visualizar primeras filas
opcion_guardar = input("¿Desea guardar los datos en formato Excel(csv) (y), o no (n): \n")

if opcion_guardar == "y" or opcion_guardar == "Y":
    # Preparamos la matriz (Tiempo + Trayectorias + semilla)
    semilla_columna = [semilla]*len(t) # [convierte semilla en una lista de la misma longitud que tiempo]
    matriz_para_guardar = np.column_stack([np.array(t), np.array(trayectorias).T, np.array(semilla_columna)]) # nos junta el cector tiempo con la matriz de trayectorias
    
    # 3. Convertimos a un "DataFrame" de Pandas
    cabecera = ["Tiempo"] + [f"Trayectoria {i+1}" for i in range(n_trayectorias)] + ["Semilla"] # cada [] es una columna
    df = pd.DataFrame(matriz_para_guardar, columns=cabecera) # [convierte matriz en tablas, nombres de columnas] ||df = dataframe
    df["Semilla"] = df["Semilla"].astype(int) # convertimos la columna de semilla a enteros para que no ponga notacion cientifica

    # Nombres de archivos
    nombre_archivo_datos = "datos_movimiento_browniano_geometrico(csv).csv" #nombre de archivo a guardar como datos  nombre_archivo_datos = "datos_movimiento_browniano_geometrico   (csv).csv" #nombre de archivo a guardar como datos

    ruta_archivo_datos = os.path.join(ruta_plots, nombre_archivo_datos)

    # 1. Guardar CSV (Para leer tú en Excel/Bloc de notas)
    #cabecera = "Tiempo;" + ";".join([f"T{i+1}" for i in range(n_trayectorias)])
    #np.savetxt(ruta_archivo_datos, matriz_para_guardar, delimiter=";", header=cabecera, comments='', fmt="%.4f", decimal=",")
    #Usamos pandas
    # sep=';' separa columnas
    # decimal=',' pone comas en los números (para Excel España)
    # index=False : no guarda el número de fila (0, 1, 2...)
    df.to_csv(ruta_archivo_datos, sep=';', decimal=',', index=False)
    print(df.head()) # mostramos las primeras filas del dataframe para verificar que se ha guardado correctamente
    
    print(f"Archivos guardados en /plots:\n - {nombre_archivo_datos} (Excel) \n")
else:
    print("Datos no guardados \n")
#mostramos
plt.show()