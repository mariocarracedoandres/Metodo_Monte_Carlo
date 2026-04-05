# CONTENIDO
- README_black_scholes.md
- simulaciones
    - modelo_black_scholes_ideal.py
    - modelo_black_scholes_realista_leland.py
    - modelo_black_scholes_realista_corregido.py
    - plots_black_scholes_ideal
        - mov_browniano_geometrico(png).png
        - precio_opciones_con_el_tiempo(png).png
        - cobertura_dinamica(png).png
        - payoff_neto_vendedor(residuos)(png).png
        - payoff_neto_comprador(png).png
    - plots_black_scholes_realista_lenand
        - mov_browniano_geometrico(png).png
        - precio_opciones_con_el_tiempo(png).png
        - cobertura_dinamica(png).png
        - payoff_neto_cartera_cobertura(residuos)(png).png
        - payoff_neto_cliente(png).png
    - plots_black_scholes_realista_corregido
        - mov_browniano_geometrico(png).png
        - precio_opciones_con_el_tiempo(png).png
        - cobertura_dinamica(png).png
        - payoff_neto_cartera_cobertura(residuos)(png).png
        - payoff_neto_cliente(png).png
- teoría
    - modelo_black_scholes.pdf
    - modelo_black_scholes.pdf


*Si se encuentra algún error en la teoría o en la implementación, no duden contactar o pull request.*


## METAS
- **Comprender el marcado de los derviados de opciones con el modelo de Black-Scholes:**
- **Comprender y visualizar el comportamiento de la cobertura dinámica y sus fluactuaciones a lo largo del tiempo** 
- **Visualización de los payoff netos tanto del vendedor como del comprador** 
- **Guardado de los datos para reproducibilidad:**

## modelo_black_scholes_ideal.py
En este programa solo se simulará el modelo haciendo la suposición de que el mercado se comporta idealmete, de esta manera los resiudos serán 0. Así el vendedor no ganará ni perdera dinero, mientras que el comprador podrá o perder la prima, o ganar dinero. En **modelo_black_scholes_realista.py**, se tendrá en cuenta el caracter no contínuo de la cobertura dinámica así como los intereses debido a la cobertura. Así los resíduos (ganancia/pérdida) del vendedor no tendrán por que ser 0.
### Requisitos 
- `numpy`
- `matplotlib`
- `pandas`
- `scipy`
- `time`
- `random`
- `os`

### Parámetros (se piden al  ejecutar el programa)
- `T`: años
- `n_trayectorias`: (1000 trayectorias en un intel i5 de 6 gen, tiempo total de simulacion + guardado de datos = 40-50 minutos), tomar 100 es ideal para ver el comportamiento.
- `S0`: (euros) precio de la accion inicial al momento del contrato
- `mu`: tendencia del mercado anual
- `sigma`: volatilidad anual
- `K`: (euros) precio de striek: acuerdo para ver a que precio comprar la accion tras el vencimiento
- `r`: tasa libre de riesgo (centrados en españa se puede tomar las letras del tesoro, el tipo de interes medio)
- `tipo_opcion`: c=call || p=put 

##### Ejemplo: los datos guardados en plots_black_scholes_ideal.py son 
- `T`: 1 # años
- `n_trayectorias`: 200
- `S0`: 17.91 # euros
- `mu`: 0.179 # se esperaba un crecimieto en 1 año de 17.91 a 21.12
- `sigma`: 0.28566 #indice VIX = 0.3105, beta = 0,92
- `K`: 17.91
- `r`: 0.02121
- `tipo_opcion`: "C"
Datos S0, mu y sigma tomados de [Yahoo Finance](https://finance.yahoo.com/quote/BBVA.MC/) (Ticker: `BBVA.MC`), r (se tomo el tipo de interes medio anual) tomado de [Letras del Tesoro](https://www.tesoro.es/deuda-publica/subastas/resultado-ultimas-subastas/letras-del-tesoro) a fecha de 29/03/2026 a las 14:32   


### Consideraciones
-El programa preguntará si se desea **guardar las imágenes (png) y los datos en formato Excel (csv)**: si (y) o no (n).
-Se han tomado en cuenta que la **separacion decimal es ","**

## modelo_black_scholes_realista_Lenand.py
### Requisitos
- `numpy`
- `matplotlib`
- `pandas`
- `scipy`
- `time`
- `random`
- `os`

### Parámetros (se piden al  ejecutar el programa)
- `T`: años
- `n_trayectorias`: (1000 trayectorias en un intel i5 de 6 gen, tiempo total de simulacion + guardado de datos = 40-50 minutos), tomar 100 es ideal para ver el comportamiento.
- `S0`: (euros) precio de la accion inicial al momento del contrato
- `mu`: tendencia del mercado anual
- `sigma`: volatilidad anual
- `K`: (euros) precio de striek: acuerdo para ver a que precio comprar la accion tras el vencimiento
- `r`: tasa libre de riesgo (centrados en españa se puede tomar las letras del tesoro, el tipo de interes medio)
- `tipo_opcion`: c=call || p=put 

Parámetros por negociciones (se piden al  ejecutar el programa)
- `frecuencia_rebalanceo`: 40 == 1 dia (252 dias laborales)
- `comision_volumen`: 0.0002 == 0.02% comision por mover dinero
- `coste_fijo`: 0.001 == 0.001€ fijos por cada operación de compra/venta

##### Ejemplo: los datos guardados en plots_black_scholes_leland.py son 
- `T`: 1 # años
- `n_trayectorias`: 200
- `S0`: 17.91 # euros
- `mu`: 0.179 # se esperaba un crecimieto en 1 año de 17.91 a 21.12
- `sigma`: 0.28566 #indice VIX = 0.3105, beta = 0,92
- `K`: 17.91
- `r`: 0.02121
- `tipo_opcion`: "C"
Datos S0, mu y sigma tomados de [Yahoo Finance](https://finance.yahoo.com/quote/BBVA.MC/) (Ticker: `BBVA.MC`), r (se tomo el tipo de interes medio anual) tomado de [Letras del Tesoro](https://www.tesoro.es/deuda-publica/subastas/resultado-ultimas-subastas/letras-del-tesoro) a fecha de 29/03/2026 a las 14:32   

- `frecuencia_rebalanceo`: 40 
- `comision_volumen`: 0.0005 == 0.05% 
- `coste_fijo`: 1.25 == 1.25€
Datos por la comision por volumen y coste fijos tomados de [Interactive Broekrs-Commissions Stock Europe-Spain](https://www.interactivebrokers.ie/en/pricing/commissions-stocks-europe.php?re=europe&p=europe)

### Consideraciones
-El programa preguntará si se desea **guardar las imágenes (png) y los datos en formato Excel (csv)**: si (y) o no (n).
-Se han tomado en cuenta que la **separacion decimal es ","**

## modelo_black_scholes_realista_corregido.py
### Requisitos
- `numpy`
- `matplotlib`
- `pandas`
- `scipy`
- `time`
- `random`
- `os`

### Parámetros (se piden al  ejecutar el programa)
- `T`: años
- `n_trayectorias`: (1000 trayectorias en un intel i5 de 6 gen, tiempo total de simulacion + guardado de datos = 40-50 minutos), tomar 100 es ideal para ver el comportamiento.
- `S0`: (euros) precio de la accion inicial al momento del contrato
- `mu`: tendencia del mercado anual
- `sigma`: volatilidad anual
- `K`: (euros) precio de striek: acuerdo para ver a que precio comprar la accion tras el vencimiento
- `r`: tasa libre de riesgo (centrados en españa se puede tomar las letras del tesoro, el tipo de interes medio)
- `tipo_opcion`: c=call || p=put 

Parámetros por negociciones (se piden al  ejecutar el programa)
- `frecuencia_rebalanceo`: 40 == 1 dia (252 dias laborales)
- `comision_volumen`: 0.0002 == 0.02% comision por mover dinero
- `coste_fijo`: 0.001 == 0.001€ fijos por cada operación de compra/venta

##### Ejemplo: los datos guardados en plots_black_scholes_realista_corregido.py son
- `T`: 1 # años
- `n_trayectorias`: 200
- `S0`: 17.91 # euros
- `mu`: 0.179 # se esperaba un crecimieto en 1 año de 17.91 a 21.12
- `sigma`: 0.28566 #indice VIX = 0.3105, beta = 0,92
- `K`: 17.91
- `r`: 0.02121
- `tipo_opcion`: "C"
Datos S0, mu y sigma tomados de [Yahoo Finance](https://finance.yahoo.com/quote/BBVA.MC/) (Ticker: `BBVA.MC`), r (se tomo el tipo de interes medio anual) tomado de [Letras del Tesoro](https://www.tesoro.es/deuda-publica/subastas/resultado-ultimas-subastas/letras-del-tesoro) a fecha de 29/03/2026 a las 14:32   

- `frecuencia_rebalanceo`: 40 
- `comision_volumen`: 0.0005 == 0.05% 
- `coste_fijo`: 1.25 == 1.25€
Datos por la comision por volumen y coste fijos tomados de [Interactive Broekrs-Commissions Stock Europe-Spain](https://www.interactivebrokers.ie/en/pricing/commissions-stocks-europe.php?re=europe&p=europe)

### Consideraciones
-El programa preguntará si se desea **guardar las imágenes (png) y los datos en formato Excel (csv)**: si (y) o no (n).
-Se han tomado en cuenta que la **separacion decimal es ","**



