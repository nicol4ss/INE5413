from Grafo import Grafo
from GrafoResidual import GrafoResidual

file = "instancias/fluxo_maximo/teste.net"

def main():
    G = Grafo.fromFile(file)
    Gr = GrafoResidual.fromNonResidualGraph(G)

    s = 0
    t = 6

    FordFulkerson(G, s, t, Gr)

    fluxo_total = 0
    for index, vizinho in enumerate(Gr.vizinhos(s)):
        fluxo = Gr.getFluxo(s, vizinho)
        if fluxo > 0:
            fluxo_total += fluxo

    print(fluxo_total)

def FordFulkerson(G: Grafo, s: int, t: int, Gr: GrafoResidual):

    while True:
        p = Edmonds_Karp(s, t, Gr)
        if not p:
            break

        p_arcos = []
        for index, v in enumerate(p):
            if index != len(p) - 1:
                u = p[index + 1]
                p_arcos.append((v, u))
            
        c_min: float = min([Gr.capacidade(u, v) for u, v in p_arcos])

        for u, v in p_arcos:
                Gr.addFluxo(u, v, c_min)


def Edmonds_Karp(s: int, t: int, Gr: GrafoResidual):
    C = [False] * Gr.qtdVertices()
    A = [None] * Gr.qtdVertices()

    C[s] = True

    Q = [s]

    while Q:
        u = Q.pop(0)
        for v in Gr.vizinhos(u):
            if (not C[v]) and (Gr.capacidade(u, v) > 0):
                C[v] = True
                A[v] = u

                if v == t:
                    p = [t]
                    w = t 
                    while w != s:
                        w = A[w]
                        p.insert(0, w)
                    return p
                Q.append(v)

    return None

main()