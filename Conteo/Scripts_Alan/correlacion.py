from matplotlib import pyplot as plt
import numpy as np

datos = np.loadtxt('mediciones_continuo_rapido_1ms.txt', delimiter = '\t')

#for i in range(len(datos[:,1])):

acorr = np.correlate(datos[1,:], datos[1,:], mode='same')

print(len(datos[1,:]))
print(len(acorr))
tiempo = np.linspace(0,0.01,2500)
print(len(tiempo))

plt.plot(tiempo,acorr)
plt.grid(True)
plt.show()