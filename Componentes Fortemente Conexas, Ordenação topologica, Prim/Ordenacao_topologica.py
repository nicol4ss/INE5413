import math
from Grafo import Grafo

file = "instancias/dirigidos/manha.net"

def main(file):
    G = Grafo.fromFile(file)

    O = Ordenacao_topologica(G)

    Print_ordem_topologica(O, G)

def Ordenacao_topologica(G: Grafo):
    
    qtdVertices = G.qtdVertices()
    C = [False] * qtdVertices
    T = [math.inf] * qtdVertices
    F = [math.inf] * qtdVertices

    tempo = 0
    O = []

    for u in range(qtdVertices-1, -1, -1):
        if not C[u]:
            DFSVisitOT(G, u, C, T, F, tempo, O)

    return O

def DFSVisitOT(G: Grafo, v: int, C: list[bool], T: list[int], F: list[int], tempo, O: list[int]):
    C[v] = True
    tempo += 1
    T[v] = tempo

    for u in G.vizinhos(v):
        if C[u] == False:
            tempo = DFSVisitOT(G, u, C, T, F, tempo, O)

    tempo += 1
    F[v] = tempo

    O.insert(0, v)
    return tempo

def Print_ordem_topologica(ordemTopologica, G):
    ordemTopologicaStr = ""
    for v in ordemTopologica:
        ordemTopologicaStr = ordemTopologicaStr + str(G.vertices[v]) + ' → '
    print(ordemTopologicaStr[:-3] + '.')

main(file)