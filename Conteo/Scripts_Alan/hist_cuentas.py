# Este script hace un histograma de ????

import numpy as np
from matplotlib import pyplot as plt

datos = np.loadtxt('mediciones_rapido_250us.txt', delimiter = '\t')

umbral = 0.068

# OJO!!!! acordate de poner minimo de tiempo para no repetir un mismo foton

cuentas = np.zeros(len(datos[:,1]))
for i in range(len(cuentas)):
	for j in range(len(datos[0,:])):
		if(datos[i,j] >= umbral):
			cuentas[i] = cuentas[i] + 1

print(np.mean(cuentas))

n,bins,patches = plt.hist(cuentas, bins=200, normed=1, facecolor='green', alpha=0.75)
plt.show()