# -*- coding: utf-8 -*-
"""
Created on Mon Jul 03 11:17:15 2017

@author: Kufa
"""

nombre = "332nm-ruido.csv"   ## Nombre del archivo que quieren cargar

file = open(nombre, "r")  ## Abro el archivo en modo de lectura

lineas = file.readlines()
cols = len(lineas[0].split(','))
data = [[] for i in range(cols-1)]  ## Creo la "matriz" con la data, 
## data[i,:] (o data [i] directamente) tiene la i-esima columna

for i in range(2,len(lineas)-1):  ## Ignoro las 2 primeras y la ultima fila
    palabras = lineas[i].split(",")
    for j in range(0,cols-1):  ## Ignoro la primera columna
        data[j].append(float(palabras[j+1]))

data = np.array(data)
file.close()