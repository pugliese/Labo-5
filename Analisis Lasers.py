# -*- coding: utf-8 -*-
"""
Created on Mon May  1 19:15:08 2017

@author: Gonzalo
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import factorial
from scipy.optimize import curve_fit


umbral = 3*3.8E-3 ##Depende de
anchoTemp = 4E-6    ##la resistecia

Intervalo = 1E-4 ## Depende del osciloscopio
ancho = anchoTemp*2500/Intervalo
data=Mediciones

Cuentas=np.zeros(len(data))
global umbral, ancho
for j in range (0,len(data)):
    i=0
    res=0
    while (i< len(data[j])):
        if (data[j,i]>umbral):
            i += int(ancho)
            res+=1
        else:
            i+=1
    
    Cuentas[j]=res

max(Cuentas)
H=np.histogram(Cuentas,bins=20,normed=True)
H0=H[0]
H1=H[1]
H2=np.zeros(len(H[0]))
for i in range(0,len(H1)-1):
    H2[i]=H1[i+1]+(H1[i+1]-H1[i])/2
plt.plot(H2,H0,'o')


mu=sum(H0*H2)/sum(H0)
# poisson function, parameter lamb is the fit parameter
def poisson(k, lamb):
    return (lamb**k/factorial(k)) * np.exp(-lamb)


# fit with curve_fit
popt, pcov = curve_fit(poisson, H2, H0, p0=mu) 



# plot poisson-deviation with fitted parameter
xmin, xmax = plt.xlim()
n = np.linspace(xmin, xmax, 1000)
plt.plot(n, poisson(n, *popt), 'r-', label='fit')



#esto es para poner las cosas en el grafico
perr = np.sqrt(np.diag(pcov))
#tituto
#plt.title('Histograma Ruido R = 0 $\Omega$',fontsize=18)

#esto es para poner letenda plt.text(posicion en x, posicion en y, texto)
plt.text(14, 0.1, r'$\mu$ = %.0f $\pm$ %.0f' %(popt,perr), fontsize=12)
#plt.text(-0.01, 3300, r'$\sigma$ = %.2f $\pm$ %.2f mV' %(popt[1]*1000,perr[1]*1000), fontsize=12)
#plt.text(0.010, 90, r'$R_square$ = %.5f ' %(stats[2]**2), fontsize=20)
#labels...
plt.xlabel('Cuentas', fontsize=14)
plt.ylabel('Probabilidad', fontsize=14)

#tamaño de los numeritos de los ejes
plt.tick_params(labelsize=12)
plt.grid()





















plt.plot(n, poisson(n, mu), 'r-', label='fit')

perr = np.sqrt(np.diag(pcov))
plt.title(r'Histograma Laser - R= 0 $\Omega$')
plt.text(12, 0.15, r'$\lambda$=%.2f $\pm$ %.2f' %(popt,perr))

plt.xlabel('Cuentas')
plt.ylabel('Probabilidad')
