import random

FILAS = 75
COLUMNAS  = 125
laberinto = []
calculos_laberinto = []

vacio = "⬜"
pared = "⬛"
jugador = "🟦"
meta = "🟫"
andado = "🟥"

visible = 0
calculo = 1

max_distancia = 0
f_jugador = 1
c_jugador = 1


def generar_laberinto_chatgpt():
    global laberinto, calculos_laberinto, fila_meta, col_meta

    # Partimos de todo paredes y reseteamos también la matriz de cálculos
    laberinto = [[pared for _ in range(COLUMNAS)] for _ in range(FILAS)]
    calculos_laberinto = [[vacio for _ in range(COLUMNAS)] for _ in range(FILAS)]

    # Para reproducibilidad (mismo laberinto siempre)
    random.seed(0)

    # Celdas “reales” del laberinto: sólo usamos posiciones con índices impares
    # Empezamos en (1, 1)
    inicio_f, inicio_c = 1, 1
    laberinto[inicio_f][inicio_c] = vacio

    # Algoritmo de backtracking (DFS) para laberintos perfectos
    stack = [(inicio_f, inicio_c)]
    movs = [(2, 0), (-2, 0), (0, 2), (0, -2)]  # saltamos de 2 en 2 para dejar paredes entre medias

    while stack:
        f, c = stack[-1]

        # Buscamos vecinos a dos pasos que sigan siendo pared
        vecinos = []
        for df, dc in movs:
            nf, nc = f + df, c + dc
            if 1 <= nf < FILAS-1 and 1 <= nc < COLUMNAS-1:
                if laberinto[nf][nc] == pared:
                    vecinos.append((nf, nc, df, dc))

        if vecinos:
            nf, nc, df, dc = random.choice(vecinos)
            # Abrimos el muro intermedio
            laberinto[f + df // 2][c + dc // 2] = vacio
            # Abrimos la nueva celda
            laberinto[nf][nc] = vacio
            stack.append((nf, nc))
        else:
            stack.pop()

    # Colocamos jugador y meta en celdas abiertas
    jugador_f, jugador_c = 1, 1
    meta_f, meta_c = FILAS - 3, COLUMNAS - 3

    laberinto[jugador_f][jugador_c] = jugador
    laberinto[meta_f][meta_c] = meta

    # Guardamos meta para el bucle principal y para los cálculos
    fila_meta, col_meta = meta_f, meta_c

    # Rellenamos calculos_laberinto: paredes = -1, resto = vacio
    for i in range(FILAS):
        for j in range(COLUMNAS):
            if laberinto[i][j] == pared:
                calculos_laberinto[i][j] = -1
            else:
                calculos_laberinto[i][j] = vacio

    # La meta tiene distancia 0
    calculos_laberinto[meta_f][meta_c] = 0

def generar_laberinto_random():
    # Crear matriz de filas y columnas para tanto el juego visible como la matriz de cálculos
    i = 0
    while i < FILAS:
        laberinto.append(list())
        calculos_laberinto.append(list())
        j = 0
        while j < COLUMNAS:
            laberinto[i].append(vacio)
            calculos_laberinto[i].append(vacio)
            j += 1
        i += 1

    # Incluir paredes
    '''
    i = 1
    while i < FILAS:
        rnd2 = random.randint(0, COLUMNAS - 1)
        for elemento in range(len(laberinto[i])):
            laberinto[i][elemento] = pared
            calculos_laberinto[i][elemento] = -1
        laberinto[i][rnd2] = vacio
        calculos_laberinto[i][rnd2] = vacio

        i += 2
    '''
    # VERSION RANDOM, TIENE EL PROBLEMA DE QUE CREA ESPACIOS CERRADOS
    for i in range(0, round(FILAS*COLUMNAS / 3)):
        rnd = random.randint(1, FILAS*COLUMNAS - 1)
        fila_rnd = rnd // FILAS
        col_rnd = rnd % FILAS
        laberinto[fila_rnd][col_rnd] = pared
        calculos_laberinto[fila_rnd][col_rnd] = -1


    # Incluir el jugador y la meta
    laberinto[0][0] = jugador

    global fila_meta, col_meta
    fila_meta = round(FILAS/2)
    col_meta = round(COLUMNAS/2)

    
    fila_meta = FILAS - 1
    col_meta = COLUMNAS - 1
    

    laberinto[fila_meta][col_meta] = meta
    calculos_laberinto[fila_meta][col_meta] = 0
    

def printear_laberinto(tipo:int) -> str:
    if tipo == visible:
        laberinto_str = ""
        for i in range(FILAS):
            for j in range(COLUMNAS):
                laberinto_str += laberinto[i][j]
            laberinto_str += "\n"
        return laberinto_str

    elif tipo == calculo:
        calculo_str = ""
        for i in range(FILAS):
            for j in range(COLUMNAS):
                string = " " + str(calculos_laberinto[i][j])
                while len(string) <= len(str(max_distancia)):
                    string += " "
                calculo_str += string
            calculo_str += "\n"
        return calculo_str


def generar_movimientos():
    movimientos = [(1,0), (-1,0), (0,1), (0,-1)]
    dist = 0
    acabado = False
    while acabado != True:
        acabado = True
        for i in range(FILAS):
            for j in range(COLUMNAS):
                if calculos_laberinto[i][j] == dist:
                    for mov in movimientos:
                        fi = i + mov[0]
                        col = j + mov[1]
                        if 0 <= fi < FILAS and 0 <= col < COLUMNAS and calculos_laberinto[fi][col] == vacio:
                            calculos_laberinto[fi][col] = dist + 1
                            acabado = False
                            if dist + 1 > max_distancia:
                                max_distancia = dist + 1
        dist += 1


def moverse(f:int, c:int):
    movimientos = [(1,0), (-1,0), (0,1), (0,-1)]
    mejor_movimiento = max_distancia + 1

    for mov in movimientos:
        fi = f + mov[0]
        col = c + mov[1]
        if 0 <= fi < FILAS and 0 <= col < COLUMNAS and calculos_laberinto[fi][col] >= 0 and calculos_laberinto[fi][col] < mejor_movimiento:
            mejor_movimiento = calculos_laberinto[fi][col]
            mejor_fi = fi
            mejor_col = col
    
    f = mejor_fi
    c = mejor_col
    laberinto[f][c] = andado
    return f, c


def restaurar_calculos():
    pass 



generar_laberinto_chatgpt()

print(f"{printear_laberinto(visible)}\n")

generar_movimientos()

while f_jugador != fila_meta or c_jugador != col_meta:
    f_jugador, c_jugador = moverse(f_jugador, c_jugador)

restaurar_calculos()
print(f"{printear_laberinto(visible)}\n")