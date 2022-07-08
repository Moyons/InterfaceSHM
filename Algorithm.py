from math import sqrt
import numpy as np
import h5py
import matplotlib.pyplot as plt

fs = 40000000
vp = 5400

f = open("distancias.txt", 'w')


def calcularMuestra(distancia):
    tiempoMuestra = distancia/(vp*100)
    muestraBuscada = tiempoMuestra*fs
    f.write("Muestra: " + str(round(muestraBuscada)) + "\n")


Piezos = []

Piezo0 = [0, 0]
Piezo1 = [1, 0]
Piezo2 = [2, 0]
Piezo3 = [3, 0]
Piezo4 = [4, 0]
Piezo5 = [5, 0]
Piezo6 = [6, 0]
Piezo7 = [7, 0]

MatrizPuntos = [100, 100]
NumeroPiezos = 8

Piezos.append(Piezo0)
Piezos.append(Piezo1)
Piezos.append(Piezo2)
Piezos.append(Piezo3)
Piezos.append(Piezo4)
Piezos.append(Piezo5)
Piezos.append(Piezo6)
Piezos.append(Piezo7)

MatrizDistancias = np.zeros((NumeroPiezos, NumeroPiezos, MatrizPuntos[0], MatrizPuntos[1]))
# Emisor, Receptor, Punto X, Punto Y

cuentaPiezoEmisor = 0
cuentaTotal = 1

for emisor in Piezos:
    f.write("Emisor: " + str(cuentaPiezoEmisor) + "\n")
    cuentaPiezoEmisor += 1
    cuentaPiezoReceptor = 0
    for receptor in Piezos:
        f.write("\tReceptor: " + str(cuentaPiezoReceptor) + "\n")
        cuentaPiezoReceptor += 1
        for x in range(MatrizPuntos[0]):
            for y in range(MatrizPuntos[1]):
                distancia = round(sqrt(pow(x - emisor[0], 2) + pow(y - emisor[1], 2)) + sqrt(pow(x - receptor[0], 2) + pow(y - receptor[1], 2)), 2)
                MatrizDistancias[Piezos.index(emisor)][Piezos.index(receptor)][x][y] = distancia
                f.write("\t\tDistancia recorrida a x = " + str(x) + " , y = " + str(y) + " : " + str(distancia) + " \t\t")
                calcularMuestra(distancia)

print(cuentaTotal)
# Una vez obtenidas las muestras se lee un punto en concreto
# Ese punto corresponde a una muestra en cada gráfica
# Se coge el valor en V en cada gráfica y se hace una media

f.close()



