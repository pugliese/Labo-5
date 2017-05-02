# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
from scipy.stats import norm
import matplotlib.patches as mpatches
from scipy.optimize import curve_fit
from matplotlib.mathtext import math_to_image



V=MedicionRuidoFrio
data=np.concatenate((V[0],V[1],V[2],V[3],V[4],V[5],V[6],V[7],V[8],V[9]))

H=np.histogram(data,bins=40,normed=False)
H0=H[0]
H1=H[1]
H2=np.zeros(len(H[0]))
for i in range(0,len(H1)-1):
    H2[i]=H1[i+1]+(H1[i+1]-H1[i])/2
plt.plot(H2,H0,'o')


mu,std=norm.fit(data)
m=max(H0)
def f(x,a,sigma,x0,b):
    return a*np.exp(-((x-x0)**2)/(2*sigma**2)) +b

popt,pcov = curve_fit(f,H2,H0,p0 = [m,std,mu,0])
xmin, xmax = plt.xlim()
n = np.linspace(xmin, xmax, 10000)
plt.plot(n, f(n, *popt), 'r-', label='fit')

perr = np.sqrt(np.diag(pcov))
plt.title('Histograma Ruido Frío')
plt.text(0.05, 8700, r'mu=%.2f $\pm$ %.2f mV' %(popt[2]*1000,perr[2]*1000))
plt.text(0.05, 9200, r'sigma=%.2f $\pm$ %.2f mV' %(popt[1]*1000,perr[1]*1000))
plt.xlabel('Voltaje [V]')
plt.ylabel('Cuentas')
