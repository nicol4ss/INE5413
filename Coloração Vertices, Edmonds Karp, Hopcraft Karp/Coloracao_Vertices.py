from functools import reduce
import math
from webbrowser import get
from Grafo import Grafo
import copy


file = "instancias/coloracao/cor3.net"


def main(file):

    G = Grafo.fromFile(file)

    min_cores = Lawler(G)

    conjuntos_maximais = getAllConjuntosMaximaisIndependentes(
        [x for x in range(G.qtdVertices())], G.arestas())

    conjuntos_maximais_combinations = powerSet(conjuntos_maximais)
    conjuntos_maximais_combinations = list(
        filter(lambda x: len(x) == min_cores, conjuntos_maximais_combinations))

    for combination in conjuntos_maximais_combinations:
        total_vertices = reduce(lambda x, y: x.union(y), combination)
        if len(total_vertices) == G.qtdVertices():
            break

    vertices_colors = []
    for cor, color_group in enumerate(combination):
        for v in color_group:
            vertices_colors.append((G.vertices[v], cor))

    vertices_colors.sort(key=lambda x: x[0])

    print("Coloração mínima:", min_cores)

    for vertice, color in vertices_colors:
        print(int(vertice), ": ", color, sep="")


def Lawler(G: Grafo):
    Szao: list[list[int]] = powerSet([x for x in range(G.qtdVertices())])
    X = [0] * len(Szao)
    Szao.pop(0)

    s = 0
    for S in Szao:
        s += 1
        S = set(S)

        X[s] = math.inf
        arestas = getArestasFromSubset(G, S)
        conjuntos_maximais = getAllConjuntosMaximaisIndependentes(S, arestas)
        for I in conjuntos_maximais:
            i = getVertexSetIndex(S - I)

            if X[i] + 1 < X[s]:
                X[s] = X[i] + 1

    return X[-1]


def getVertexSetIndex(vertex_set: set[int]):
    index = 0
    for v in vertex_set:
        index = index | (1 << v)

    return index


def getAllConjuntosMaximaisIndependentes(V, E):

    S: list[list[int]] = powerSet(V)
    S.sort(key=lambda x: len(x))

    R = []
    for X in S:
        c = True
        for v in X:
            for u in X:
                if (u, v, 1.0) in E or (v, u, 1.0) in E:
                    c = False
                    break

        if c:
            X_set = set(X)
            R = list(filter(lambda x: not x.issubset(X_set), R))

            R.append(X_set)

    return R


def getArestasFromSubset(G: Grafo, vertices_subset: set):
    # vertices_subset_map = set(vertices_subset)

    all_arestas = G.arestas()
    sub_set_arestas = []
    for aresta in all_arestas:
        if aresta[0] in vertices_subset and aresta[1] in vertices_subset:
            sub_set_arestas.append(aresta)

    return sub_set_arestas


def powerSet(set):
    set = list(set)
    set_size = len(set)
    pow_set_size = (int)(math.pow(2, set_size))

    counter = 0
    power_set = []
    for counter in range(0, pow_set_size):
        sub_set = []
        for i in range(0, set_size):
            if((counter & (1 << i)) > 0):
                sub_set.append(set[i])
        power_set.append(sub_set)

    return power_set


main(file)
