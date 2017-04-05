# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:35:14 2017

@author: Publico
"""
from __future__ import division, unicode_literals, print_function, absolute_import

import time

import numpy as np
import visa
import matplotlib.pylab as ppt
rm = visa.ResourceManager()
## rm.list_resources()

t = time.gmtime()

d = 9.9  # Distancia entre anodo y catodo
duracion = 240      # Duracion en segundos de la medicion
intervalo = 1.5     # Duracion de cada valor de voltaje (tiempo entre saltos)
## intervalo > n*0.5  con n la cantidad de multimetros
rango = [0.6, 1.3]      # Rango en Volts entre los que se mueve la rampa, el voltaje real será ~ x5000

intervalo = float(intervalo)

instrumentos = ['USB::0x0699::0x0346::C034166::INSTR','GPIB0::22::INSTR','GPIB0::23::INSTR','GPIB0::24::INSTR']

def QueEsQue():
    mide = [" controla el generador", " mide Voltaje A", " mide Voltaje B", " mide Presion"]
    for n in range(1,len(instrumentos)):
        print(instrumentos[n]+" --> "+mide[n])
        a = rm.open_resource(instrumentos[n])
        print(a.query('*IDN?'))
        a.close()

fungen = rm.open_resource(instrumentos[0])    # Generador de funciones
mult1 = rm.open_resource(instrumentos[1])     # Multimetro 1 (Voltaje A)
mult2 = rm.open_resource(instrumentos[2])     # Multimetro 2 (Voltaje B)
barometro = rm.open_resource(instrumentos[3]) # Barometro (Multimetro)

# Rampa lineal de offset (DC voltage)
Va = []
Vb = []
P = []
##Voltajes = np.linspace(rango[0], rango[1], int(duracion/intervalo))

Voltajes = np.concatenate(((np.linspace(rango[0], rango[1], int(.5*duracion/intervalo)), np.linspace(rango[1], rango[0], int(.5*duracion/intervalo)))))
for offset in Voltajes:
    fungen.write('VOLT:OFFS %f' % offset)
    time.sleep(max(0,intervalo-1.5))       # Espero a que el sistema estabilice
    Va.append(float(mult1.query('MEASURE:VOLTAGE:DC?')))       # Mido multimetro 1, tarda 0.5s
    Vb.append(float(mult2.query('MEASURE:VOLTAGE:DC?')))       # Mido multimetro 2, tarda 0.5s
    P.append(float(barometro.query('MEASURE:VOLTAGE:DC?')))     # Mido presion, tarda 0.5s



fungen.close()
barometro.close()
mult1.close()
mult2.close()

exp = "VvsI_fino240"+str(duracion)
fecha = "%d-%d-%d-%d-%d" %(t[0:5])
archivo = exp+"_"+str(d)+"_"+fecha

VF = [500*v for v in Voltajes]

np.savez(archivo, PresionEnV=P, Va=Va, Vb=Vb, VoltajeFuente=VF)



## np.savetxt('ej.dat',(Va, Vb))
## xx = np.loadtxt('ej.dat')
## Ejemplo de carga
## 
## outfile = TemporaryFile()
## np.savez(outfile, x=x, y=y)
## outfile.seek(0)
## npzfile = np.load(outfile)
## npzfile.files
## ['y', 'x']
## npzfile['x']
## array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
