from hashlib import new
from tkinter import N
from Grafo import Grafo
import math

file = "instancias/caminho_minimo/minimum.net"

def main():
    #insanciar grafo
    grafo = Grafo(file)

    result = floydWarshall(grafo)
    printMatrix(result)
    

def floydWarshall(grafo: Grafo):

    # Pego a matriz de caminhos minimos
    matDist = grafo.matrizDistancias()

    # Algoritmo de floyd warshall
    for k in range(grafo.qtdVertices()):
        for i in range(grafo.qtdVertices()):
            for j in range(grafo.qtdVertices()):
                matDist[i][j] = min(matDist[i][j], matDist[i][k] + matDist[k][j])
        
    return matDist

def printMatrix(matriz):


    for itens in matriz: #Printa a matriz final organizando a leitura
        print("")   
        for item in itens:
            print("%s\t " % item, end="")
    print("\n")
            
main()