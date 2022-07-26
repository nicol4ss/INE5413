import math
from Grafo import Grafo

file = "instancias/dirigidos/dirigido2.net"


def main(file):
    G = Grafo.fromFile(file)

    A = componentesFortementeConexas(G)

    forest = getForest(A)

    printForest(forest)


def componentesFortementeConexas(G):

    C, T, A, F = DFS(G)

    Gt = transporGrafo(G)

    Ct, Tt, At, Ft = DFS_adaptado(Gt, F)

    return At


def DFS(G: Grafo):
    qtdVertices = G.qtdVertices()
    C = [False] * qtdVertices
    T = [math.inf] * qtdVertices
    F = [math.inf] * qtdVertices
    A = [None] * qtdVertices

    tempo = 0

    for u in range(qtdVertices):
        if (C[u] == False):
            tempo = DFSVisit(G, u, C, T, A, F, tempo)

    return (C, T, A, F)


def DFS_adaptado(G: Grafo, F1: list[int]):
    qtdVertices = G.qtdVertices()
    C = [False] * qtdVertices
    T = [math.inf] * qtdVertices
    F = [math.inf] * qtdVertices
    A = [None] * qtdVertices

    tempo = 0

    # Cria uma lista dos vértices em ordem descrencente perante seu valor em F
    vertices_ordenados = [x for x in range(qtdVertices)]
    vertices_ordenados.sort(reverse=True, key=lambda x: F1[x])

    for u in vertices_ordenados:
        if (C[u] == False):
            tempo = DFSVisit(G, u, C, T, A, F, tempo)

    return (C, T, A, F)


def DFSVisit(G: Grafo, v: int, C: list[bool], T: list[int], A: list[int], F: list[int], tempo):
    C[v] = True
    tempo += 1
    T[v] = tempo

    for u in G.vizinhos(v):
        if C[u] == False:
            A[u] = v
            tempo = DFSVisit(G, u, C, T, A, F, tempo)

    tempo += 1
    F[v] = tempo

    return tempo


def transporGrafo(G: Grafo):
    # Inicializa uma lista de adjacências com a quantidade de vértices
    listaAdjacencias = [[] for i in range(G.qtdVertices())]

    # Insere arcos invertendo a direção. Se a = (v, u), a' = (u, v)
    for i, vertice in enumerate(G.listaAdjacencias):
        for j, aresta in enumerate(vertice):
            listaAdjacencias[aresta[0]].append((i, aresta[1]))

    GTransposto = Grafo(G.vertices, listaAdjacencias)

    return GTransposto


def getForest(A: list[int]):
    qtdVertices = len(A)

    # Inicializa um array para guardar os indexes das árvores
    tree_index = [None] * qtdVertices

    # Salva o valor do maior index da lista
    maxIndex = 0
    forest = []

    for v in range(qtdVertices):

        # Verifica se o vértice já pertence a uma árvore
        if tree_index[v] == None:
            predecessor = A[v]
            tree = [v]

            while True:
                # Verifica se o vértice tem antecessor. Se não tiver, ele faz parte de uma árvore recém descoberta
                if predecessor == None:
                    # Atualiza o index de cada vertice pertencente à arvore
                    for u in tree:
                        tree_index[u] = maxIndex
                    forest.append(tree)
                    maxIndex += 1
                    break

                # Verifica se o antecessor já está em uma árvore
                predecessor_tree_index = tree_index[predecessor]
                if predecessor_tree_index != None:
                    # Adiciona todos os vértices da árvore em construção na árvore do vértice antecessor
                    for u in tree:
                        tree_index[u] = predecessor_tree_index
                    forest[predecessor_tree_index] += tree
                    break

                # A árvore em construção não chegou a uma raiz. O loop é repetido com o antecessor do atual antecessor
                tree.append(predecessor)
                predecessor = A[predecessor]

    return forest


def printForest(forest):
    for tree in forest:
        treeStr = ""
        for v in tree:
            treeStr = treeStr + str(v+1) + ','
        print(treeStr[:-1])


main(file)
