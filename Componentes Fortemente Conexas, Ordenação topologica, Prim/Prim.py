import math
from unittest import result
from Grafo import Grafo

file = "instancias/arvore_geradora_minima/agm_tiny.net"

def main(file):
    grafo = Grafo.fromFile(file)
    result = prim(grafo)
    printPrim(result)

def printPrim(resultados: tuple):
    ancestraisList = resultados[0]
    caminhosList = resultados[1]
    ancestralEfilho = ""
    caminhoMinimo = 0
    
    #Soma pesos do caminho minimo
    for item in caminhosList:
        caminhoMinimo += item

    #Configuração ancestral e filho
    for index, v in enumerate(ancestraisList):
        if v == None:
            v = -1
        ancestralEfilho += f"{v+1}-{index+1}, "

    print(caminhoMinimo)
    print(ancestralEfilho)
    


def prim(grafo: Grafo):

    #L;ista de ancestrais baseado no index (vertice)
    A = []
    for i in range(grafo.qtdVertices()):
        A.append(None)
    
    #Chave minima de cada vertice equivalente a seu respectivo index, setada para infinito
    K = []
    for i in range(grafo.qtdVertices()):
        K.append(math.inf)

    # Vertice zero setada para chave minima zero
    K[0] = 0

    #Salvando para print do valor do caminho minimo
    chaves = []
    for i in range(grafo.qtdVertices()):
        chaves.append(math.inf)
    
    chaves[0] = 0

    #Vetor de vertices ultilizado na logica do loop principal
    q = [*range(0, grafo.qtdVertices(), 1)]

    while len(q) != 0:

        #Remove o menor valor da lista Keys
        u = min(K)

        #Obtem o index de K que é o vertice que estamos olhando
        vertice = K.index(u)

        #Remove o vertice da lista
        q.remove(vertice)

        #logica do algortimo de prim
        #Para todo vertice pertencente a lista de adjacencias do vertice faça
        for v in grafo.listaAdjacencias[vertice]:
            #Se o vertice esta na lista de vertices q, e o peso é menor que sua chave faça
            if v[0] in q and grafo.peso(vertice, v[0]) < chaves[v[0]]:
                #Armazena o peso como a nova chave do seu vertice e salva o ancestral na lista de ancestrais
                K[v[0]] = grafo.peso(vertice, v[0])
                A[v[0]] = vertice
                #Salva a configuração final dos pesos
                chaves[v[0]] = grafo.peso(vertice, v[0])
                
        #Adaptado para não perder o index dos vertices na lista K e obter um novo valor minimo na linha 38
        K[vertice] = math.inf
                
        
    return A, chaves


main(file)
