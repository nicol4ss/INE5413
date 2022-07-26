from math import inf
from queue import Queue
from GrafoBipartido import GrafoBipartido

file = "instancias/emparelhamento_maximo/pequeno.net"

def main(file):
    G = GrafoBipartido.fromFile(file)

    saida = HopcroftKarp(G)
    mate = []
    for i in range(len(saida[1])):
        mate.append(saida[1][i] + 1)
    print(f"m = {saida[0]}, mate = {mate}")

def HopcroftKarp(G):

    # Distâncias
    D = [inf] * (G.qtdVertices() + 1)
    # Casamentos (Parceiro de v)
    mate = [None] * G.qtdVertices()  
    # Matchings
    m = 0  

    while BFS(G, mate, D):
        for x in G.X:
            # Se x não possui um parceiro
            if mate[x - 1] is None:  
                if DFS(G, mate, x, D):
                    m += 1

    return m, mate, D

# Busca em largura com mais de um ponto de origem
def BFS(G, mate, D):
    Q = Queue()
    for x in G.X:
        # Se o vértice está livre (sem parceiro)
        if mate[x - 1] is None:  
            D[x] = 0
            Q.put(x)
        # Se o vértice não está livre (possui parceiro)
        else:  
            D[x] = inf
    # Vértice artificial
    D[0] = inf  
    while not Q.empty():
        x = Q.get()
        if D[x] < D[0]:
            # Para cada vizinho de x
            for y in G.vizinhos(x):  
                pos = mate[y - 1]
                # Se y possui um parceiro não nulo
                if pos is not None:  
                    if D[pos] == inf:
                        D[pos] = D[x] + 1
                        Q.put(mate[y - 1])
                # Se y possui um parceiro nulo
                else:  
                    D[0] = D[x] + 1
    # Se o vértice artificial permancer inalterado, não foi encontrado um caminho aumentante alternante
    return not D[0] == inf

def DFS(G, mate, x, D):
    # Se x não for nulo
    if x is not None:
        # Para cada vizinho de x
        for y in G.vizinhos(x):  
            pos = mate[y - 1]
            # Se y possui um parceiro não nulo
            if pos is not None:  
                if D[pos] == D[x] + 1:
                    if DFS(G, mate, mate[y - 1], D):
                        # Faz o casamento x com y
                        mate[y - 1] = x
                        mate[x - 1] = y
                        return True
            # Se y possui um parceiro nulo            
            else:  
                # Faz o casamento x com y
                mate[y - 1] = x
                mate[x - 1] = y
                return True
        D[x] = inf
        
        return False
    return True

main(file)