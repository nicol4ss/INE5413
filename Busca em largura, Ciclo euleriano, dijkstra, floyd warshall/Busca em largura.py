import math
from Grafo import Grafo

file = "instancias/caminho_minimo/fln_pequena.net"
s = 1

def main(file, s: int):
    s = s - 1
    grafo = Grafo(file)

    # Vertice i já visitado
    C: list[bool] = [False] * grafo.qtdVertices()
    # Distância, em vértices, até o vértice i
    D: list[int] = [math.inf] * grafo.qtdVertices()
    # Vertice antecessor ao vertice i
    A: list[int] = [None] * grafo.qtdVertices()

    # Marca o vertice de origem como já visitado...
    C[s] = True
    # ... e seta sua distância para 0
    D[s] = 0
    
    # Fila de visitas - inicia com S
    Q:list[int] = [s]

    while Q:
        u = Q.pop(0)

        for v in grafo.vizinhos(u):
            if not C[v]:
                C[v] = True
                D[v] = D[u] + 1
                A[v] = u
                Q.append(v)

    printD(D)

def printD(D):
    for i in range(max(D)+1):
        print(f"{i}: ", end='')
        for vertice, distancia in enumerate(D):
            if distancia == i:
                print(vertice + 1, end=' ')
        print()

main(file, s)