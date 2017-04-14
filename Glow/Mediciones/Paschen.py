# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from __future__ import division, unicode_literals, print_function, absolute_import

import time

import numpy as np
import matplotlib.pylab as ppt
from math import exp, log
from scipy.optimize import curve_fit

def Corriente(Vb):
    return Vb/149.2

def Voltaje(Va):
    return Va*1000
    
    
def Ruptura(V,I):
    i = 0
    while I[i+1]-I[i]<0.1:
        i+=1
    return (V[i]+V[i])/2
    

def Presion(V):
    res = []
    np.array(res)
    for i in range(0,len(V)):
        res.append(exp(3.46*V[i]-27.96))
    return res

def Presiones(Ps):
    return [Presion(p) for p in Ps]

def grafica(V):
    for v in V:
        ppt.plot(v)

Archivos = ["VvsI_fino240_8.3_2017-4-11-15-24","VvsI_fino240_8.3_2017-4-11-15-34","VvsI_fino240_13.5_2017-4-11-15-56","VvsI_fino240_19.8_2017-4-11-15-47","VvsI_bien_fino120_21.6_2017-4-4-16-20","VvsI_fino240_24.1_2017-4-11-15-11","VvsI_fino240_29.7_2017-4-4-15-34"]
Ps = []
Vas = []
Vbs = []
for i in range(0,len(Archivos)):
    data = np.load(str(Archivos[i]+".npz"))
    Ps.append(data["PresionEnV"])
    Vas.append(data["Va"])
    Vbs.append(data["Vb"])
    
Pprom = [sum(Presion(p))/len(p) for p in Ps]
Pinit = [exp(p[i]*3.46-27.96) for p in Ps]
d = [8.3,8.3, 13.5, 19.8, 21.6, 24.1, 29.7]
Pprom = np.array(Pprom)
Pinit = np.array(Pinit)
d = np.array(d)
PD = Pinit*d
print("Los valored de Pd son: ")
for i in range(0,len(d)):
    print(PD[i], "+-", PD[i]*.15)
    
Vd = []
for i in range(0,len(Vas)):
    Vd.append(1000*Ruptura(Vas[i],Vbs[i]))
ppt.plot(PD,Vd,"ro")


Paschen = lambda x,a,b: a*x/(np.log(x)+b)
curve_fit(Paschen, PD, Vd)

PD2 = [PD[0],PD[1], (PD[2]+PD[5]+PD[6])/3, PD[4],PD[2]]
Vd2 = [Vd[0],Vd[1], (Vd[2]+Vd[5]+Vd[6])/3, Vd[4],Vd[2]]

Param = curve_fit(Paschen, PD2, Vd2)
pd = np.linspace(min(PD2),max(PD2),1000)
vd = []
for p in pd:
    vd.append(Paschen(p,Param[0][0],Param[0][1]))
ppt.plot(pd,vd)
ppt.plot(PD2,Vd2,"ro")
show()

R-square = .8*np.cov(Vd2,vd2)[0][1]/sqrt(np.var(Vd2)*np.var(vd2))
