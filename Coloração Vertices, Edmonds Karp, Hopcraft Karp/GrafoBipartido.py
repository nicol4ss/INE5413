import math
import copy

class GrafoBipartido:
    def __init__(self, vertices: list[str], listaAdjacencias: list[list[tuple[int, float]]]):

        self.__vertices = vertices
        self.__qtdVertices = len(vertices)

        self._listaAdjacencias = listaAdjacencias

        # Conta a quantidade de arestas iterando pela lista de adjacencias
        qtdArestas = 0
        for vertice in listaAdjacencias:
            for aresta in vertice:
                qtdArestas += 1

        self.__qtdArestas = qtdArestas

    # Inicializa o grafo a partir vertices e lista de adjacencias já prontos./
    @classmethod
    def fromFile(cls, filePath: str):
        "Instancia um grafo. Recebe o caminho do arquivo do grafo como argumento."
        self = cls.__new__(cls)

        self.__vertices = []
        self.__qtdArestas = 0

        self._listaAdjacencias: list[list[tuple[int, float]]]
        self.__qtdVertices: int

        self.__bipartido = True # colocar false dps

        self.X = []
        self.Y = []

        with open(filePath, 'r') as file:
            self.__qtdVertices = int(file.readline()[10:])
            self._listaAdjacencias = [[] for i in range(self.__qtdVertices)]

            dirigido = False
            for line in file:
                if line.startswith("*edges"):
                    break
                if line.startswith("*arcs"):
                    dirigido = True
                    break

                if line == "\n":
                    continue

                label = line[line.find('"')+1:-2]

                self.__vertices.append(label)
                
            if not dirigido:
                for line in file:
                    info = line.split(" ")
                    x = int(info[0]) - 1
                    y = int(info[1]) - 1
                    w = float(info[2])

                    if (x not in self.X) and (x not in self.Y):
                        self.inserirX(x)  
                    if (y not in self.X) and (y not in self.Y):
                        self.inserirY(y)

                    self._listaAdjacencias[x].append((y, w))

                    self.__qtdArestas += 1
            
        return self

    @property
    def vertices(self):
        return copy.copy(self.__vertices)

    @property
    def listaAdjacencias(self):
        return copy.deepcopy(self._listaAdjacencias)

    def qtdVertices(self):
        return self.__qtdVertices

    def qtdArestas(self):
        return self.__qtdArestas

    def grau(self, v: int):
        return len(self._listaAdjacencias[v])

    def rotulo(self, v: int):
        return self.__vertices[v]

    def vizinhos(self, v: int):
        return [aresta[0] for aresta in self._listaAdjacencias[v]]

    def haAresta(self, u, v):
        for aresta in self._listaAdjacencias[u]:
            if aresta[0] == v:
                return True
        return False

    def peso(self, u, v):
        for aresta in self._listaAdjacencias[u]:
            if aresta[0] == v:
                return aresta[1]
        return math.inf

    def capacidade(self, u, v):
        for aresta in self._listaAdjacencias[u]:
            if aresta[0] == v:
                return aresta[1]
        return 0

    def arestas(self):
        arestas: list[tuple[int, int, float]] = []
        for v, vizinhos in enumerate(self._listaAdjacencias):
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

    def residual(self):
        vertices = self.vertices
        listaAdj = self.listaAdjacencias

        for v, vizinhos in enumerate(listaAdj):
            for vuIndex, V_arco in enumerate(vizinhos):
                u = V_arco[0]
                vuW = V_arco[1]

                uvW = None
                for U_arco in listaAdj[u]:
                    if U_arco[0] == v:
                        uvW = U_arco[1]

                if uvW == None:
                    listaAdj[u].append((v, 0))

                else:
                    index = len(vertices)
                    vertices.append(f"Helper {v}-{u}")

                    listaAdj[vuIndex] = 0

                    #ida
                    listaAdj[v].append(index, vuW)
                    listaAdj[index].append(u, vuW)

                    #Volta
                    listaAdj[u].append(index, 0)
                    listaAdj[index].append(v, 0)

                    #Pog
                    listaAdj[u]
        
        return GrafoBipartido(vertices, listaAdj)

    
    # Insere um vértice v em X -- Hopocraft-Karp Bipartido
    def inserirX(self, v):
        self.X.append(v)

    # Insere um vértice v em Y -- Hopocraft-Karp Bipartido
    def inserirY(self, v):
        self.Y.append(v)

    def getVertice(self, i):
        for vertice in self.vertices:
            if vertice == i:
                return vertice
        return False