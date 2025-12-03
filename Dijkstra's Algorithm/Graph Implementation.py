class Graph:
    def __init__(self):
        self.adj = {}

    def add_vertex(self, name:str) -> None:
        if name not in self.adj:
            self.adj[name] = []
    
    def add_edge(self, u:str, v:str, weight:int, undirected:bool=False) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append(Vertex(v, weight))

        # If undirected add the opposite edge
        if undirected:
            self.adj[v].append(Vertex(u, weight))

    # Better to print using repr
    def print_graph(self):
        print("Points in the graph:")
        for vertex in self.adj.keys():
            print(f" · {vertex}: ", end="")
            for i in range(len(self.adj[vertex])):
                print(f"({self.adj[vertex][i].neighbor}, {self.adj[vertex][i].weight})", end=" ")
            print()


class Vertex:
    def __init__(self, neighbor:str, weight:int) -> None:
        self.neighbor = neighbor
        self.weight = weight

    def __repr__(self):
        return f"({self.neighbor}, {self.weight})"




if __name__ == "__main__":
    g = Graph()

    g.add_edge("A", "B", 3)
    g.add_edge("A", "C", 5)
    g.add_edge("B", "C", 1)
    g.add_edge("B", "D", 7)
    g.add_edge("C", "D", 2)
    g.add_edge("E", "F", 4)
    g.add_edge("F", "C", 6)

    print(g.adj)
    g.print_graph()