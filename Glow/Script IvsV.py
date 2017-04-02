# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:35:14 2017

@author: Publico
"""
from __future__ import division, unicode_literals, print_function, absolute_import

import time

import numpy as np
import visa
rm = visa.ResourceManager()

duracion = 120      # Duracion en segundos de la medicion
intervalo = 0.1     # Duracion de cada valor de voltaje (tiempo entre saltos)
rango = [0, 1]      # Rango en Volts entre los que se mueve la rampa, el voltaje real será ~ x5000

intervalo = float(intervalo)

instrumentos = ['USB::0x0699::0x0346::C034166::INSTR','GPIB0::22::INSTR','GPIB0::23::INSTR','GPIB0::24::INSTR']

def QueEsQue():
    mide = [" controla el generador", " mide Voltaje A", " mide Voltaje B", " mide Presion"]
    for n in range(0,len(instrumentos)):
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
VP = []
for offset in np.linspace(rango[0], rango[1], int(duracion/intervalo)):
    fungen.write('VOLT:OFFS %f' % offset)
    time.sleep(intervalo/2)       # Espero a que el sistema estabilice
    Va.append(float(mult1.query('MEASURE:VOLTAGE:DC?')))       # Mido multimetro 1
    Vb.append(float(mult2.query('MEASURE:VOLTAGE:DC?')))       # Mido multimetro 2
    VP.append(float(barometro.query('MEASURE:VOLTAGE:DC?')))     # Mido presion
    time.sleep(intervalo/2)       # Termino de esperar lo que me falta

presion = lambda x: exp(3.4*x-27)

P = [presion(p) for p in VP]

fungen.close()
barometro.close()
mult1.close()
mult2.close()