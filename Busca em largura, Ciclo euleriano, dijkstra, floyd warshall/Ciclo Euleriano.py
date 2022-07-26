import math
from Grafo import Grafo

file = "instancias/ciclo_euleriano/SemCicloEuleriano.net"
s = 1


def main():
    r, ciclo = hierholzer(file, s)

    # Exibe o resultado no terminal
    print(int(r))
    if r:
        for i in ciclo:
            print(i+1, end=' ')
        print()

def hierholzer(file, s: int):
    s = s - 1
    G = Grafo(file)

    E = G.arestas()
    C: set[tuple[int, int]] = set()

    # Seleciona, arbitrariamente, um vertice conectado a uma aresta
    v = 0
    for vertice, vizinhos in enumerate(G.listaAdjacencias):
        if vizinhos:
            v = vertice
            break

    r, ciclo = buscarSubsicloEuleriano(G, v, C)

    if not r:
        return (False, None)

    # Verifica se o ciclo é, de fato, euleriano
    for i in range(G.qtdVertices()):
        vizinhos = G.vizinhos(i)
        for vizinho in vizinhos:
            if ((i, vizinho) not in C) and ((vizinho, i) not in C):
                return (False, None)

    return (True, ciclo)


def buscarSubsicloEuleriano(G: Grafo, v: int, C: set[tuple[int, int]]):
    ciclo = [v]
    t = v

    aresta = set()
    while True:

        # Verifica de existe alguma aresta não visitada conectada a v
        vizinhos = G.vizinhos(v)
        arestaEncontrada = False
        for vizinho in vizinhos:
            if not (((v, vizinho) in C) or ((vizinho, v) in C)):
                arestaEncontrada = True
                aresta = (v, vizinho)

        # Se não houver, retorna (False, None)
        if not arestaEncontrada:
            return (False, None)

        # Adiciona a aresta ao conjunto de arestas vizitadas
        C.add(aresta)

        # v <- u
        for u in aresta:
            if u != v:
                v = u

        ciclo.append(v)

        if v == t:
            break

    for index, x in enumerate(ciclo):
        vizinhos = G.vizinhos(x)
        for vizinho in vizinhos:
            if ((x, vizinho) not in C) and ((vizinho, x) not in C):
                r, subCiclo = buscarSubsicloEuleriano(G, x, C)
                if not r:
                    return (False, None)

                ciclo[index:index] = subCiclo

    return (True, ciclo)

main()
