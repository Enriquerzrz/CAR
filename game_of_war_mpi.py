import numpy as np # Se importa numpuy
import matplotlib.pyplot as plt # Se importa matplotlib
from matplotlib import colors # Se importa colors
import random # Se importa random
import time # Se importa time
from mpi4py import MPI # Se importa MPI

# Variables MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Variables globales
AZUL = (27, 167, 249) # Color Azul
ROJO = (237, 70, 70) # Color Rojo
NEGRO = (0, 0, 0) # Color Negro

TAM_TABLERO = (10, 10) # Tamaño tablero

# Funciones
'''
Definición: Se genera una matriz que representará el tablero de juego
Entradas: El tamaño del tablero (matriz)
Salidas: El tablero terminado y relleno (matriz inicializada)
'''
def generar_tablero(TAM_TABLERO):
    tablero = np.zeros(TAM_TABLERO) # Se hace el tablero entero de 0
    
    # Se rellena de 1 la mitad
    for i in range(TAM_TABLERO[0]//2):
        for j in range(TAM_TABLERO[1]):
            tablero[i][j] = 1

    return tablero # Se devuelve tablero


'''
Definición: Función que permite ver el tablero para conocer su funcionamiento
Entradas: Tablero
Salidas: Visualización del tablero
'''
def ver_tablero(tablero):
    plt.figure(figsize=(10,10)) # Tamaño figura
    plt.title("Game of War",size=28) # Título de la tabla
    colormap = colors.ListedColormap(["firebrick","cornflowerblue"]) # Colores
    plt.imshow(tablero, cmap=colormap) # Se elije que ver
    plt.show() # Ver tabla


'''
Definición: Función que encuentra el conflicto y da paso a la función conflicto
Entradas: tablero
Salidas: lugar de conflicto, si no hay conflicto devuelve fin
'''
def detectar_conflicto(tablero):
    aux = tablero
    for i in range((TAM_TABLERO[0]-1)):
            for j in range(TAM_TABLERO[1]-1):
                # Si encuentra un enemigo a su alrededor (arriba, abajo, derecha e izquierda)
                if(tablero[i][j] != tablero[i+1][j] or tablero[i][j] != tablero[i][j-1] or tablero[i][j] != tablero[i][j+1] or tablero[i][j] != tablero[i-1][j]):
                    # Si hay un conflicto se realiza
                    aux = conflicto(tablero, i, j)
    return aux


'''
Definición: Función que calcula quien gana y quien pierde
Entradas: lugar de conflicto
Salidas: perdedor
'''
def calculo_ganador(tablero, i, j):
    perdedor = (0, 0)
    # contador de enemigos colindantes
    enemigo = 0
    
    # calculo probabilidades
    if(tablero[i][j] != tablero[i+1][j]):
        # si se suma 1 es que i+1 es enemigo
        enemigo = enemigo + 1
    if(tablero[i][j] != tablero[i][j-1]):
        # si se suma 10 es que j-1 es enemigo
        enemigo = enemigo + 10
    if(tablero[i][j] != tablero[i][j+1]):
        # si se suma 100 es que j+1 es enemigo
        enemigo = enemigo + 100
    if(tablero[i][j] != tablero[i-1][j]):
        # si se suma 1000 es que i-1 es enemigo
        enemigo = enemigo + 1000
    
    # si solo hay un enemigo, 50%
    if(enemigo == 1 or enemigo == 10 or enemigo == 100 or enemigo == 1000):
        # valor random entre 0 y 1
        valor = random.randint(0, 1)
        # 0 pierde [i, j]
        if(valor == 0):
            perdedor = (i, j)
        # 1 pierde el cuadrado enemigo a [i, j]
        else:
            if(enemigo == 1):
                perdedor = (i+1, j)
            elif(enemigo == 10):
                perdedor = (i, j-1)
            elif(enemigo == 100):
                perdedor = (i, j+1)
            else:
                perdedor = (i-1, j)

    # si hay dos enemigos, 66% contra 33%
    elif(enemigo == 11 or enemigo == 101 or enemigo == 1001 or enemigo == 110 or enemigo == 1010 or enemigo == 1100):
        #valor random entre 1 y 17
        valor = random.randint(1, 17)
        # valor >= 7 pierde [i, j]
        if(valor >= 7):
            perdedor = (i, j)
        # 4 >= valor <= 6 pierde el cuadrado enemigo a [i, j]
        elif(valor >= 4 and valor <= 6):
            if(enemigo == 11):
                perdedor = (i+1, j)
            elif(enemigo == 101):
                perdedor = (i+1, j)
            elif(enemigo == 1001):
                perdedor = (i+1, j)
            elif(enemigo == 110):
                perdedor = (i, j-1)
            elif(enemigo == 1010):
                perdedor = (i, j-1)
            else:
                perdedor = (i, j+1)
        # valor <= 4 pierde el cuadrado enemigo a [i, j]
        else:
            if(enemigo == 11):
                perdedor = (i, j-1)
            elif(enemigo == 101):
                perdedor = (i, j+1)
            elif(enemigo == 1001):
                perdedor = (i-1, j)
            elif(enemigo == 110):
                perdedor = (i, j+1)
            elif(enemigo == 1010):
                perdedor = (i-1, j)
            else:
                perdedor = (i-1, j)

    # si hay tres enemigos, 75% contra 25%
    elif(enemigo == 111 or enemigo == 1011 or enemigo == 1101 or enemigo == 1110):
        #valor random entre 1 y 48
        valor = random.randint(0, 48)
        # valor >= 13 pierde [i, j]
        if(valor >= 13):
            perdedor = (i, j)
        # 9 >= valor <= 12 pierde el cuadrado enemigo a [i, j]
        elif(valor >= 9 and valor <= 12):
            if(enemigo == 111):
                perdedor = (i+1, j)
            if(enemigo == 1011):
                perdedor = (i+1, j)
            if(enemigo == 1101):
                perdedor = (i+1, j)
            else:
                perdedor = (i, j+1)
        # 5 >= valor <= 8 pierde el cuadrado enemigo a [i, j]
        elif(valor >= 5 and valor <= 8):
            if(enemigo == 111):
                perdedor = (i, j+1)
            if(enemigo == 1011):
                perdedor = (i, j+1)
            if(enemigo == 1101):
                perdedor = (i, j-1)
            else:
                perdedor = (i, j-1)
        # 1 >= valor <= 4 pierde el cuadrado enemigo a [i, j]
        elif(valor >= 1 and valor <= 4):
            if(enemigo == 111):
                perdedor = (i, j-1)
            if(enemigo == 1011):
                perdedor = (i-1, j)
            if(enemigo == 1101):
                perdedor = (i-1, j)
            else:
                perdedor = (i-1, j)

    # si hay cuatro enemigos, 80% contra 20%
    else:
        #valor random entre 1 y 48
        valor = random.randint(0, 48)
        # valor >= 13 pierde [i, j]
        if(valor >= 13):
            perdedor = (i, j)
        # 10 >= valor <= 12 pierde el cuadrado enemigo a [i, j]
        elif(valor >= 10 and valor <= 12):
            perdedor = (i+1, j)
        # 10 >= valor <= 12 pierde el cuadrado enemigo a [i, j]
        elif(valor >= 10 and valor <= 12):
            perdedor = (i, j+1)
        # 10 >= valor <= 12 pierde el cuadrado enemigo a [i, j]
        elif(valor >= 10 and valor <= 12):
            perdedor = (i, j-1)
        else:
            perdedor = (i-1, j)

    return perdedor


'''
Definición: Función que realiza el conflicto mediante probabilidades
Entradas: lugar de conflicto
Salidas: 
'''
def conflicto(tablero, i, j):
    # Se actualiza el tablero tras un conflicto
    perd = calculo_ganador(tablero, i, j)
    new_tab = cambio_color(tablero, perd)
    
    return new_tab


'''
Definición: Función que cambia de color al perdedor
Entradas: Tablero y perdedor
Salidas: Tablero actualizado
'''
def cambio_color(tablero, perdedor):
    # Se cambia el color de una posición concreta

    if (tablero[perdedor[0], perdedor[1]] == 1):
        tablero[perdedor[0], perdedor[1]] = 0
    else:
        tablero[perdedor[0], perdedor[1]] = 1
    
    return tablero


'''
Definición: Función que comprueba si toda la matriz es de un color
Entradas: Lugar de conflicto
Salidas: condición de terminación
'''
def comprobar_final(tablero):
    # Se comprueba si no hay más conflictos en el tablero
    for i in range(TAM_TABLERO[0]-1):
        for j in range(TAM_TABLERO[1]-1):
            if(tablero[i][j] != tablero[i+1][j] or tablero[i][j] != tablero[i][j-1] or tablero[i][j] != tablero[i][j+1] or tablero[i][j] != tablero[i-1][j]):
                return False
            
    return True


'''
Definición: Función que comprueba que equipo ha ganado
Entradas: Tablero
Salidas: 1 o 0
'''
def quien_gana(tablero):
    aux = np.zeros(TAM_TABLERO)

    # Se comrueba quien gana o pierde
    if ((aux + tablero).any()):
        return 0
    else:
        return 1


'''
Definición: Función que contiene todo el programa principal
Entradas: -
Salidas: Gandor de la batalla
'''
def batalla(TAM_TABLERO):
    tam_t = TAM_TABLERO
    tablero = generar_tablero(tam_t) # Se genera tablero
    terminado = False # Se inicializa la condición de terminación
    ver = 0 # Variable para elegir cada cuanto ver el tablero

    while (terminado == False):
        tablero = detectar_conflicto(tablero) # Actualización del tablero
        
        # Si han pasado 10 iteracicones
        if ver == 10:
            # ver_tablero(tablero) # Visualización del tablero
            ver = 0 # Se resetea
        else:
            ver = ver + 1 # Se suma una vuelta

        terminado = comprobar_final(tablero) # Se comprueba si se finaliza

    return quien_gana(tablero) # Devolución de ganador

'''
Definición: Calcular el tiempo de una batalla
Entradas: tamaño del tablero 
Salidas: tiempo de ejecución
'''
def calcular_tiempo_ejecucion(tam):
    inicio = time.time() # Se inicializa el tiempo
    
    for i in range(10):
        if rank == 0 and ( i==0 or i==1) :
            batalla(tam) # Ocurre la batalla
        if rank == 1 and ( i==2 or i==3) :
            batalla(tam) # Ocurre la batalla
        if rank == 2 and ( i==4 or i==5) :
            batalla(tam) # Ocurre la batalla
        if rank == 3 and ( i==6 or i==7) :
            batalla(tam) # Ocurre la batalla
        if rank == 4 and ( i==8 or i==9) :
            batalla(tam) # Ocurre la batalla

    fin = time.time() # Sefinaliza el tiempo

    return fin-inicio # Se calcula la didferencia de tiempo


# Ejecución
t = []

# Se ejecuta con tablero 10x10
TAM_TABLERO = (10, 10)
t.append(calcular_tiempo_ejecucion((10, 10)))

# Se ejeucta con tablero 20x20
TAM_TABLERO = (20, 20)
t.append(calcular_tiempo_ejecucion((20, 20)))

# Se ejecuta con tablero 30x30
TAM_TABLERO = (30, 30)
t.append(calcular_tiempo_ejecucion((30, 30)))

# Se ejecuta con tablero 40x40
TAM_TABLERO = (40, 40)
t.append(calcular_tiempo_ejecucion((40, 40)))

print("Tiempos usando", str(rank), ": ")
print(t)

