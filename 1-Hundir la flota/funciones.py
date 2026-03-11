import random
import time
import os
import saludos

def crear_tablero():
    """ Función para crear un nuevo tablero de 10x10. Devuelve el tablero; se puede guardar en una nueva variable. """
    tablero = [[" " for fila in range(10)] for i in range(10)]
    # Fila es una lista completa del tablero
    # i es el contenido de cada celda (la "columna" de la fila)
    return tablero

def imprimir_tablero(tablero):
    """ Función para imprimir un determinado tablero. """
    for fila in tablero:
        for i in fila:
            print(f"[{i}]",end=" ")
        print("")

def yo_coordenadas():
    fila = int(input("Introduce la coordenada i (del 0 al 9):")) # No he logrado parar el juego en caso de que se introduzca una coordenada inválida
    columna = int(input("Introduce la coordenada j (del 0 al 9):"))
    return fila, columna

def maquina_coordenadas():
    fila = random.randint(0, 9)
    columna = random.randint(0, 9)
    return fila, columna

def yo_disparar(tablero_barcos, tablero_juego): # Así llamo al tablero donde están los barcos (B), y al tablero donde juega el/la jugador/a
    while any("B" in fila for fila in tablero_barcos): # Como es lista de listas, poniendo "while 'B'" asume que toda la fila tiene que ser B; de esta forma, busca dentro de cada lista
        fila, columna = yo_coordenadas()     
    
        if tablero_barcos[fila][columna] == "B":
            tablero_barcos[fila][columna] = "X" # Si no cambio también la "B" del tablero original, el juego nunca termina porque el while siempre es True
            tablero_juego[fila][columna] = "X"    
            print(f"Tocado en posición {fila}, {columna}.")
            imprimir_tablero(tablero_juego)
            time.sleep(3)

        elif tablero_barcos[fila][columna] == " ":        
            tablero_barcos[fila][columna] = "O"
            tablero_juego[fila][columna] = "O"    
            print("Agua.")
            imprimir_tablero(tablero_juego)
            print("Turno de la máquina.")
            break
        
        else:
            print("La coordenada ya ha sido introducida.")

def maquina_disparar(tablero_barcos, tablero_juego):
    while any("B" in fila for fila in tablero_barcos):
        fila, columna = maquina_coordenadas()
        
        if tablero_barcos[fila][columna] == "B":
            tablero_barcos[fila][columna] = "X"
            tablero_juego[fila][columna] = "X"    
            print(f"Tocado en posición {fila}, {columna}.")
            imprimir_tablero(tablero_juego)
            time.sleep(3)

        elif tablero_barcos[fila][columna] == " ":        
            tablero_barcos[fila][columna] = "O"
            tablero_juego[fila][columna] = "O"    
            print("Agua.")
            imprimir_tablero(tablero_juego)
            print("Tu turno.")
            break
        
        else:
            print("La coordenada ya ha sido introducida.")

def todos_barcos_hundidos(tablero_barcos): # Para comprobar si se han hundido todos los barcos de alguien y poder terminar el juego en el bucle 
    if any("B" in fila for fila in tablero_barcos) == False:
        return True

def hundir_la_flota(yo_tablero_juego, maquina_tablero_juego, yo_tablero_barcos, maquina_tablero_barcos):
    while True:
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear') # Para borrar la pantalla en la terminal
        saludos.yo_turno()
        time.sleep(2)
        print("Así vas tú:") # Para que se imprima los que yo he hundido y los que me han hundido, y que se vea bien
        imprimir_tablero(yo_tablero_juego) 
        print("Así va la máquina:") 
        imprimir_tablero(yo_tablero_barcos) 
        time.sleep(2)
        yo_disparar(maquina_tablero_barcos, yo_tablero_juego)
        time.sleep(2)
        
        if todos_barcos_hundidos(maquina_tablero_barcos):
            saludos.despedida_ganador()
            break
        
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear') 
        saludos.maquina_turno()
        time.sleep(2)
        
        time.sleep(2)
        maquina_disparar(yo_tablero_barcos, maquina_tablero_juego)
        time.sleep(2)
        
        if todos_barcos_hundidos(yo_tablero_barcos):
            saludos.despedida_perdedor()
            break