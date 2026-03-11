import pyfiglet
import random
import time
import os
import saludos
import funciones
import tableros
import barcos

saludos.bienvenida()
time.sleep(3)
saludos.instrucciones()
time.sleep(3)

funciones.hundir_la_flota(tableros.yo_tablero_juego, tableros.maquina_tablero_juego, tableros.yo_tablero_barcos, tableros.maquina_tablero_barcos)