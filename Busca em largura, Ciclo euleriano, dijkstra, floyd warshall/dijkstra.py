from Grafo import Grafo
import math

file = "instancias/caminho_minimo/fln_pequena.net"

def main():
    grafo = Grafo(file)

    D, A = dijkstra(grafo, 2)
    printPaths(D, A)

def dijkstra(grafo: Grafo, s: int):
    s = s - 1
    D: list[float] = [math.inf] * grafo.qtdVertices()
    A: list[int] = [-1] * grafo.qtdVertices()
    C: list[bool] = [False] * grafo.qtdVertices()

    D[s] = 0

    while not all(C):
        u = -1
        for i in range(grafo.qtdVertices()):
            if (C[i] == False) and (D[i] < D[u] or u == -1):
                u = i
        C[u] = True

        for v in [x for x in grafo.vizinhos(u) if C[x] == False]:
            if D[v] > D[u] + grafo.peso(u, v):
                D[v] = D[u] + grafo.peso(u, v)
                A[v] = u

    return D, A

def printPaths(D, A):
    for v in range(len(D)):
        print(v+1, ": ", sep="", end="")

        path = [v]
        a = A[v]
        while a != -1:
            path.append(a)
            a = A[a]

        pathLen = len(path)
        for index, i in enumerate(path[::-1]):
            print(i+1, end='')
            if index != pathLen-1:
                print(",", end="")

        print("; d=", D[v], sep="")

main()
            




# print("Distancias:")
# for v, distancia in enumerate(D):
#     print(v+1, ": ", distancia, sep="")

# print("Ancestrais:")
# for v, ancestral in enumerate(A):
#     print(v+1, ": ", ancestral+1, sep="")