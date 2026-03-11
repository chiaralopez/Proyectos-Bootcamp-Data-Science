import pyfiglet # Para las letras originales

def bienvenida ():
    titulo_bienvenida = pyfiglet.figlet_format('HUNDIR LA FLOTA', font = "doom", width = 100)
    print(titulo_bienvenida)
    
def instrucciones():
    instrucciones = """¿Cómo funciona el juego?
    1. Hay dos jugadorxs: tú y la máquina.
    2. Cada unx tiene un tablero de 10 x 10 posiciones donde irán los barcos a hundir.
    3. Los barcos ya están colocados y se componen de: 4 barcos de 1 posición de eslora, 3 barcos de 2 posiciones de eslora, 
    2 barcos de 3 posiciones de eslora y 1 barco de 4 posiciones de eslora.
    4. Se trata de ir disparando y hundiendo los barcos del/la adversarix hasta que alguien se queda sin barcos y, por tanto, pierde.
    5. Funciona por turnos y empiezas tú. En cada turno disparas a una coordenada (X, Y) del tablero adversario. Si aciertas, te vuelve 
    a tocar; en caso contrario, le toca a la máquina. En los turnos de la máquina, si acerta también le vuelve a tocar. 
    ¿Dónde dispara la maquina? A un punto aleatorio en tu tablero.
    6. Si se hunden todos los barcos de algunx, el juego acaba y gana la otra persona."""
    print(instrucciones)

def yo_turno():
    yo_turno = pyfiglet.figlet_format('Tu turno', font = "banner", width = 150)
    print(yo_turno)

def maquina_turno():
    maquina_turno = pyfiglet.figlet_format('Turno de la maquina', font = "banner", width = 150)
    print(maquina_turno)
    
def despedida_ganador():
    despedida_ganador = pyfiglet.figlet_format('HAS GANADO', font = "doom", width = 100)
    print(despedida_ganador)
    
def despedida_perdedor():
    despedida_perdedor = pyfiglet.figlet_format('HAS PERDIDO', font = "doom", width = 100)
    print(despedida_perdedor)