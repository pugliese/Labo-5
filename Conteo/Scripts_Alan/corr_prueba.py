from matplotlib import pyplot as plt
import numpy as np

#datos = np.ones(2500)
datosss = np.loadtxt('mediciones_continuo_rapido_1ms.txt', delimiter = '\t')
datos=datosss[1,:]

N = len(datos)
temp = np.zeros(N)
for n in range(N):
	print(n)
	prod = datos[n:N]*datos[0:(N-n)]
	temp[n] = 1/(N-n) * np.sum(prod)

acorr = np.zeros(2*N-1)
acorr[0:N] = temp
for i in range(1,N):
	acorr[-i] = temp[i]

tiempo = np.linspace(-0.01,0.01,4999)

acorr2 = np.correlate(datos, datos, mode='same')

tiempo2 = np.linspace(-0.005,0.005,2500)

plt.plot(tiempo,acorr, tiempo2, acorr2/N)
plt.grid(True)
plt.show()