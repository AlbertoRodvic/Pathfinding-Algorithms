'''
EXAMPLES OF COMMON WAYS TO REPRESENT GRAPHS

graph = {'A': ['B', 'C'], 'B': ['C', 'D'], 'C': ['D'], 'D': ['C'], 'E': ['F'], 'F': ['C']}


DIRECTED GRAPH 
graph = {
    "A": [("B", 3), ("C", 5)],
    "B": [("C", 1), ("D", 7)],
    "C": [("D", 2)],
    "D": [("C", 1)],
    "E": [("F", 4)],
    "F": [("C", 6)]
}

SAME GRAPH BUT UNDIRECTED
graph = {
    "A": [("B", 3), ("C", 5)],
    "B": [("A", 3), ("C", 1), ("D", 7)],
    "C": [("A", 5), ("B", 1), ("D", 2)],
    "D": [("B", 7), ("C", 2)],
    "E": [("F", 4)],
    "F": [("E", 4), ("C", 6)]
}


1. update estimates
2. choose next vertex
'''

'''
IMPORTANT TERMINOLOGY:
    u: vertex you come from
    v: vertex you go to
    w: weight of the edge uv
'''

import numpy as np

explored = True
unexplored = False

class Graph:
    def __init__(self):
        self.adj = {}

    def add_vertex(self, name:str) -> None:
        if name not in self.adj:
            self.adj[name] = []
    
    def add_edge(self, u:str, v:str, w:int, undirected:bool=True) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append(Vertex(v, w))

        # If undirected add the opposite edge
        if undirected:
            self.adj[v].append(Vertex(u, w))

    # Better to print using repr
    def print_graph(self):
        print("Points in the graph:")
        for v in self.adj.keys():
            print(f" · {v}: ", end="")
            for i in range(len(self.adj[v])):
                print(f"({self.adj[v][i].neighbor}, {self.adj[v][i].weight})", end=" ")
            print()


    def update_estimates(self, u:str):
        for v in self.adj[u]:
            old_dist = self.dist[v.neighbor][0]
            new_dist = self.dist[u][0] + v.weight
            if new_dist < old_dist:
                self.dist[v.neighbor][0] = self.dist[u][0] + v.weight
                self.dist[v.neighbor][2] = u

    def choose_next_vertex(self, u:str) -> str:
        min_distance = np.inf
        
        for vertex in self.adj.keys():
            if self.dist[vertex][1] == unexplored:
                dist = self.dist[vertex][0]
                if dist < min_distance:
                    min_distance = dist
                    min_vertex = vertex
        self.dist[min_vertex][1] = explored

        return min_vertex

    def run_dijkstra(self, start:str, end:str) -> list:
        self.dist = {}
        best_path = []

        # Defining the distances initially. All set to infinity except for the starting point.
        for vertex in self.adj.keys():
            self.dist[vertex] = [np.inf, unexplored, None]
        self.dist[start] = [0, unexplored, None]

        # Running Dijkstra as a whole
        u = start
        while self.dist[end][1] == unexplored:
            self.update_estimates(u)
            u = self.choose_next_vertex(u)
        
        # Making the best_path list
        v = end
        while v != None:
            best_path.append(v)
            v = self.dist[v][2]
        best_path = best_path[::-1]

        return best_path


class Vertex:
    def __init__(self, neighbor:str, w:int) -> None:
        self.neighbor = neighbor
        self.weight = w

    def __repr__(self):
        return f"({self.neighbor}, {self.weight})"





if __name__ == "__main__":
    start = "A"
    end = "F"

    g = Graph()

    g.add_edge("A", "B", 3)
    g.add_edge("A", "C", 5)
    g.add_edge("B", "C", 1)
    g.add_edge("B", "E", 7)
    g.add_edge("C", "D", 2)
    g.add_edge("E", "F", 4)
    g.add_edge("F", "C", 6)

    print(g.adj)
    g.print_graph()

    best_path = g.run_dijkstra(start, end)
    print(f"Best path from {start} to {end}: {best_path}")