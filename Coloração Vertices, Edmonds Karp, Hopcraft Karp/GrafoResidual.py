from Grafo import Grafo
import math

class GrafoResidual(Grafo):
    def __init__(self, vertices: list[str], listaAdjacencias: list[list[tuple[int, float]]]):
        super().__init__(vertices, listaAdjacencias)

    # Inicializa o grafo a partir vertices e lista de adjacencias já prontos./
    @classmethod
    def fromNonResidualGraph(cls, graph: Grafo):
        "Recebe um grafo como argumento e constroi o grafo de sua rede residual. É inicializado com fluxo 0"
        self = cls.__new__(cls)

        vertices = graph.vertices
        listaAdj = graph.listaAdjacencias

        residualListaAdj = graph.listaAdjacencias
        doubleArcs = set()
        
        qtdVertices = graph.qtdVertices()
        # Itera pela lista de adjacencias
        for v in range(qtdVertices):
            vizinhos = listaAdj[v]
            qtdVizinhos = len(vizinhos)
            # Itera pelos vizinhos u do vértice v
            for vuIndex in range(qtdVizinhos):
                V_arco = vizinhos[vuIndex]
                u = V_arco[0]
                vuW = V_arco[1]

                uvW = None
                for U_arco in listaAdj[u]:
                    if U_arco[0] == v:
                        uvW = U_arco[1]

                if uvW == None:
                    residualListaAdj[u].append((v, 0))

                else:
                    arc = tuple()
                    if v < u:
                        arc = (v, u)
                    else:
                        arc = (u, v)

                    doubleArcs.add(arc)

        for v, u in doubleArcs:

            x = len(vertices)
            vertices.append(f"Helper {v}-{u}")
            residualListaAdj.append([])

            vuIndex = 0
            for index, aresta in enumerate(listaAdj[v]):
                if aresta[0] == u:
                    vuIndex = index
                    break

            residualListaAdj[v][vuIndex] = (u, 0)
            V_arco = listaAdj[v][vuIndex]
            u = V_arco[0]
            vuW = V_arco[1]

            # ida
            residualListaAdj[v].append((x, vuW))
            residualListaAdj[x].append((u, vuW))

            # Volta
            residualListaAdj[u].append((x, 0))
            residualListaAdj[x].append((v, 0))


        self.__init__(vertices, residualListaAdj)
        return self

    def getFluxo(self, u: int, v: int):
        return super().peso(v, u)

    def addFluxo(self, u: int, v: int, fluxo: float):
        "Pode receber tanto um valor positov quanto negativo"

        for index, arco in enumerate(self._listaAdjacencias[v]):
            if arco[0] == u:
                self._listaAdjacencias[v][index] = (u, arco[1] + fluxo)

        for index, arco in enumerate(self._listaAdjacencias[u]):
            if arco[0] == v:
                self._listaAdjacencias[u][index] = (v, arco[1] - fluxo)        

    def getCapacidade(self, u, v):
        return super().peso(u, v)
