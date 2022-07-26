import math

class Grafo:
    def __init__(self, filePath: str):
        "Instancia um grafo. Recebe o caminho do arquivo do grafo como argumento."

        self.__vertices = []
        self.__qtdArestas = 0

        self.__listaAdjacencias: list[list[tuple[int, float]]]
        self.__qtdVertices: int

        with open(filePath, 'r') as file:
            self.__qtdVertices = int(file.readline()[10:])
            self.__listaAdjacencias = [[] for i in range(self.__qtdVertices)]

            for line in file:
                if line.startswith("*edges"):
                    break

                label = line[line.find('"')+1:-2]

                self.__vertices.append(label)

            for line in file:
                info = line.split(" ")
                a = int(info[0]) - 1
                b = int(info[1]) - 1
                w = float(info[2])

                self.__listaAdjacencias[a].append((b, w))
                self.__listaAdjacencias[b].append((a, w))

                self.__qtdArestas += 1

    @property
    def vertices(self):
        return self.__vertices

    @property
    def listaAdjacencias(self):
        return self.__listaAdjacencias

    def qtdVertices(self):
        return self.__qtdVertices

    def qtdArestas(self):
        return self.__qtdArestas

    def grau(self, v: int):
        return len(self.__listaAdjacencias[v])

    def rotulo(self, v: int):
        return self.__vertices[v]

    def vizinhos(self, v: int):
        return [aresta[0] for aresta in self.__listaAdjacencias[v]]

    def haAresta(self, u, v):
        for aresta in self.__listaAdjacencias[u]:
            if aresta[0] == v:
                return True
        return False

    def peso(self, u, v):
        for aresta in self.__listaAdjacencias[u]:
            if aresta[0] == v:
                return aresta[1]
        return math.inf

    def arestas(self):
        arestas: list[tuple[int, int, float]] = []
        for v, vizinhos in enumerate(self.__listaAdjacencias):
            for vizinho in vizinhos:
                if vizinho[0] >= v:
                    arestas.append((v, *vizinho))
        return arestas


    def matrizDistancias(self):

        #Crio uma matrix (lista de listas) com valor inicial infinito para tratar caminhos minimos
        matrizDist = [math.inf] * self.qtdVertices()
        for i in range(self.qtdVertices()):
            matrizDist [i] = [math.inf] * self.qtdVertices()

        # Seto a distancia de si mesmo para zero
        for i in range(self.qtdVertices()):
            for j in range(self.qtdVertices()):
                if i == j:
                    matrizDist[i][j] = 0
        
        #Percorro a matriz e salvou seu peso on tem arestas entre os vertices
        for i in range(self.qtdVertices()):
            for j in range(self.qtdVertices()):
                if self.haAresta(i,j):
                    matrizDist[i][j] = self.peso(i,j)

        #Obtendo uma matriz de caminhos
        return matrizDist