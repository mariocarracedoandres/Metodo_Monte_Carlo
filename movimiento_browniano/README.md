# CONTENIDO
- README.md
- simulaciones
    - movimiento_browniano.py
    - plots
        -datos_movimiento_browniano_estandar(csv).csv
        -datos_movimiento_browniano_aritmetico(csv).csv
        -movimiento_browniano_estandar(png).png
        -movimiento_browniano_aritmetico(png).png
- teoría
    - movimiento_browniano.pdf
    - movimiento_browniano.tex


## METAS
- **implemetnar el metodo de monte carlo para simular el movimiento browniano:**
- **Estudiar el comportamiento estocastico para 1 y varias treayectorias:** ver como la variacion de la tendencia y volatilidad afecta al comportamiento estocastico.
- **Guardado de los datos para reproducibilidad:** Exportacion de los datos en formato Excel (csv) así como la semilla utlizidada.

### movimieto_browniano.py
#### Requisitos
- `numpy`
- `matplotlib`
- `pandas`

#### Parámetros
- `tiempo_maximo`: indicar el tiempo maximo de simulación
- `entrada`: indicar el número de trayectorias a simular
- `mu`: indicar la tendencia
- `sigma`: indicar la volatilidad

##### Ejemplo 1: movimeinto browniano estandar.
- `mu`: 0
- `sigma`: 1
Observar **plots\movimiento_browniano_estandar(png).png** y **plots\datos_movimiento_browniano_estandar(csv).csv**

##### Ejemplo 2: movimeinto browniano aritmetico.
- `mu`: 1
- `sigma`: 3
Observar **plots\movimiento_browniano_aritmetico(png).png** y **plots\datos_movimiento_browniano_aritmetico(csv).csv**

#### Consideraciones
-El programa preguntará si se desea **visualziar** los resurados en consola: si (y) o no (n). Además, si se desea **guardar los datos en formato Excel (csv)**: si (y) o no (n).
-Se han tomado en cuenta que la **separacion decimal es ","**

## movimiento_browniano_geometrico.py
Aún en desarrollo.