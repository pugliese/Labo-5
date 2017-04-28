# Este script hace un histograma de cada valor de tension medido.
# Usamos el txt donde se guardo la matriz de tensiones del script osc.py.
# De aca obtenemos el umbral de decision entre ruido y cuenta.

import numpy as np
from matplotlib import pyplot as plt

datos = np.loadtxt('mediciones_rapido_250us.txt', delimiter = '\t')

data = datos.flatten()

n,bins,patches = plt.hist(data, bins=1000, normed=1, facecolor='green', alpha=0.75)
plt.show()