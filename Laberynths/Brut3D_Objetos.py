import random

symbols = {     "player":   "🟦",
                "meta":     "🟩",
                "brick":    "⬛",
                "blank":    "⬜",
                "path":     "🟥"    }

class Laberynth:


    def __init__(self, depth, rows, columns):

        self.depth:int = depth
        self.rows:int = rows
        self.columns:int = columns
        self.grid:list[list[list[int]]] = []

        for z in range(depth):
            self.grid.append([])

            for y in range(rows):
                self.grid[z].append([])

                for x in range(columns):
                    self.grid[z][y].append(Tile(z,y,x))

        self.set_player()
        self.set_goal()


    def set_player(self):

        self.player:Player = Player(0,0,0)
        self.grid[0][0][0] = Tile(0,0,0,"player","")


    def set_goal(self):

        self.goal = Goal(self.depth-2, self.rows-2, self.columns-2)
        self.grid[self.depth-2][self.rows-2][self.columns-2] = Tile(self.depth-2, self.rows-2, self.columns-2,"meta",0)






    def generar_laberinto_chatgpt_ver1(self):
        # 1) Dejar TODO como pared y vaciar pesos
        for z in range(self.depth):
            for y in range(self.rows):
                for x in range(self.columns):
                    self.grid[z][y][x].state = symbols["brick"]
                    self.grid[z][y][x].weight = ""

        # 2) DFS para laberinto "perfecto" en 3D
        #    Ahora usamos TODO el rango [0, dim-1], sin reservar bordes como paredes
        start_z, start_y, start_x = 0, 0, 0
        self.grid[start_z][start_y][start_x].state = symbols["blank"]

        stack = [(start_z, start_y, start_x)]
        # saltos de 2 para dejar una pared entre celdas
        moves = [(2, 0, 0), (-2, 0, 0),
                 (0, 2, 0), (0, -2, 0),
                 (0, 0, 2), (0, 0, -2)]

        random.seed(0)  # quita esto si quieres laberintos distintos cada vez

        while stack:
            z, y, x = stack[-1]

            vecinos = []
            for dz, dy, dx in moves:
                nz, ny, nx = z + dz, y + dy, x + dx
                if (0 <= nz < self.depth and
                    0 <= ny < self.rows and
                    0 <= nx < self.columns):
                    if self.grid[nz][ny][nx].state == symbols["brick"]:
                        vecinos.append((nz, ny, nx, dz, dy, dx))

            if vecinos:
                nz, ny, nx, dz, dy, dx = random.choice(vecinos)
                # abrir el "muro" intermedio
                mz, my, mx = z + dz // 2, y + dy // 2, x + dx // 2
                self.grid[mz][my][mx].state = symbols["blank"]
                # abrir la nueva celda
                self.grid[nz][ny][nx].state = symbols["blank"]
                stack.append((nz, ny, nx))
            else:
                stack.pop()

        # 3) Colocar jugador y meta en celdas abiertas (esquinas opuestas)
        player_pos = (0, 0, 0)
        goal_pos   = (self.depth - 1, self.rows - 1, self.columns - 1)

        pz, py, px = player_pos
        gz, gy, gx = goal_pos

        # Asegurar que jugador y meta caen en celdas transitables
        self.grid[pz][py][px].state = symbols["blank"]
        self.grid[gz][gy][gx].state = symbols["blank"]

        # Actualizar objetos Player y Goal
        self.player = Player(pz, py, px)
        self.goal   = Goal(gz, gy, gx)

        # Pintar sus casillas
        self.grid[pz][py][px].state = symbols["player"]
        self.grid[gz][gy][gx].state = symbols["meta"]

        # 4) Inicializar pesos: paredes = -1, resto = "", meta = 0
        for z in range(self.depth):
            for y in range(self.rows):
                for x in range(self.columns):
                    if self.grid[z][y][x].state == symbols["brick"]:
                        self.grid[z][y][x].weight = -1
                    else:
                        self.grid[z][y][x].weight = ""

        self.grid[gz][gy][gx].weight = 0




    def generar_laberinto_chatgpt_ver2(self):
        # 1) Poner TODO como pared y vaciar pesos
        for z in range(self.depth):
            for y in range(self.rows):
                for x in range(self.columns):
                    self.grid[z][y][x].state = symbols["brick"]
                    self.grid[z][y][x].weight = ""

        # 2) DFS clásico en 3D, moviéndonos de 1 en 1
        start_z, start_y, start_x = 0, 0, 0
        self.grid[start_z][start_y][start_x].state = symbols["blank"]

        stack = [(start_z, start_y, start_x)]
        moves = [
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1)
        ]

        random.seed(0)  # comenta esto si quieres laberintos distintos cada vez

        while stack:
            z, y, x = stack[-1]

            vecinos = []
            for dz, dy, dx in moves:
                nz, ny, nx = z + dz, y + dy, x + dx
                if (
                    0 <= nz < self.depth and
                    0 <= ny < self.rows and
                    0 <= nx < self.columns
                ):
                    if self.grid[nz][ny][nx].state == symbols["brick"]:
                        vecinos.append((nz, ny, nx))

            if vecinos:
                nz, ny, nx = random.choice(vecinos)
                # Abrimos la nueva celda
                self.grid[nz][ny][nx].state = symbols["blank"]
                stack.append((nz, ny, nx))
            else:
                stack.pop()

        # 3) Colocar jugador y meta en esquinas opuestas (asegurándonos de que son transitables)
        player_pos = (0, 0, 0)
        goal_pos = (self.depth - 1, self.rows - 1, self.columns - 1)

        pz, py, px = player_pos
        gz, gy, gx = goal_pos

        self.grid[pz][py][px].state = symbols["blank"]
        self.grid[gz][gy][gx].state = symbols["blank"]

        self.player = Player(pz, py, px)
        self.goal = Goal(gz, gy, gx)

        self.grid[pz][py][px].state = symbols["player"]
        self.grid[gz][gy][gx].state = symbols["meta"]

        # 4) Inicializar pesos: paredes = -1, resto = "", meta = 0
        for z in range(self.depth):
            for y in range(self.rows):
                for x in range(self.columns):
                    if self.grid[z][y][x].state == symbols["brick"]:
                        self.grid[z][y][x].weight = -1
                    else:
                        self.grid[z][y][x].weight = ""

        self.grid[gz][gy][gx].weight = 0




    

    def print_lab(self):

        laberinto_str = ""

        for z in range(self.depth):
            for y in range(self.rows):
                for x in range(self.columns):
                    print(self.grid[z][y][x].state, end="") 

                print()

            print()

        return laberinto_str
    

    def generate_movements(self):

        '''
        # Sin diagonales
        movements = []
        sumas = (-1, 1)
        for i in range(3):
            for j in sumas:
                li = [0,0,0]
                li[i] = j
                movements.append(tuple(li))
        return movements

        '''
        #Con diagonales
        movements = []
        z,y,x = -1,-1,-1
        base = 2
        while z < base:
            while y < base:
                while x < base:
                    movements.append((z,y,x))
                    x += 1
                x = -1
                y += 1
            x,y = -1,-1
            z += 1

        movements.remove((0,0,0))
        return movements
        ''''''
    

    def generate_weights(self, movements:list):

        global max_distancia
        max_distancia = 0
        dist = 0
        acabado = False

        while acabado != True:
            acabado = True

            for z in range(self.depth):
                for y in range(self.rows):
                    for x in range(self.columns):
                        if self.grid[z][y][x].weight == dist:
                            for mov in movements:
                                de = z + mov[0]
                                fi = y + mov[1]
                                col = x + mov[2]

                                if 0 <= de < self.depth and 0 <= fi < self.rows and 0 <= col < self.columns and self.grid[de][fi][col].weight == "":
                                    self.grid[de][fi][col].weight = dist + 1
                                    acabado = False

                                    if dist + 1 > max_distancia:
                                        max_distancia = dist + 1
            dist += 1


    def move(self, position:tuple):

        global max_distancia
        movements = self.generate_movements()
        best_mov = max_distancia + 1

        for mov in movements:
            de = position[0] + mov[0]
            fi = position[1] + mov[1]
            col = position[2] + mov[2]

            if 0 <= de < self.depth and 0 <= fi < self.rows and 0 <= col < self.columns and self.grid[de][fi][col].weight >= 0 and self.grid[de][fi][col].weight < best_mov:
                best_mov = self.grid[de][fi][col].weight
                mejor = (de, fi, col)
    
        self.grid[mejor[0]][mejor[1]][mejor[2]].state = symbols["path"]
        self.player.position = mejor[0], mejor[1], mejor[2]



class Tile:
    def __init__(self, position_z, position_y, position_x, state = "blank", weight = ""):
        global symbols
    
        self.position = (position_z, position_y, position_x)

        self.state = symbols[state]
        self.weight = weight



class Player:
    def __init__(self, position_z, position_y, position_x):    
        self.position = (position_z, position_y, position_x)



class Goal:
    def __init__(self, position_z, position_y, position_x):    
        self.position = (position_z, position_y, position_x)



if __name__ == "__main__":

    lab = Laberynth(1,50,150)

    lab.generar_laberinto_chatgpt_ver1()

    lab.print_lab()

    movements = lab.generate_movements()
    lab.generate_weights(movements)

    while lab.player.position != lab.goal.position:
        lab.move(lab.player.position)

    lab.print_lab()