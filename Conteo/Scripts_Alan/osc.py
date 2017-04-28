# -*- coding: utf-8 -*-
"""
Osciloscopio Tektronix TDS1002B
Manual U (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TDS1002 Manual.pdf
Manual P (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TDS 100-1000-2000_prog.pdf
Manual U (local): \\Srvlabos\manuales\Tektronix\TDS1002 Manual.pdf
Manual P (local): \\Srvlabos\manuales\Tektronix\TDS 200-1000-2000_prog.pdf
"""

# Este script guarda en un txt una matriz con los valores de tension medidos por el osciloscopio
# para n pantallas

from __future__ import division, unicode_literals, print_function, absolute_import
import time
from matplotlib import pyplot as plt
import numpy as np
import visa

print(__doc__)

resource_name = 'USB0::0x0699::0x0363::C108013::INSTR'

rm = visa.ResourceManager()

osci = rm.open_resource(resource_name)

osci.query('*IDN?')

# Le pido algunos parametros de la pantalla, para poder escalear adecuadamente
xze, xin, yze, ymu, yoff = osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')

# Modo de transmision: Binario
osci.write('DAT:ENC RPB')
osci.write('DAT:WID 1')

# Adquiere los datos del canal 1 y los devuelve en un array de numpy


# tiempo = xze + np.arange(len(data)) * xin

# plt.plot(tiempo, data)
# plt.xlabel('Tiempo [s]')
# plt.ylabel('Voltaje [V]')
# plt.grid(True)

def definir_medir(inst, xze, xin, yze, ymu, yoff):

    def _medir():
        data = inst.query_binary_values('CURV?', datatype='B', container=np.array)
        data = -((data-yoff)*ymu + yze)

        #tiempo = xze + np.arange(len(data)) * xin
        #return tiempo, data
        return data
    
    # Devolvemos la funcion auxiliar que "sabe" la escala
    return _medir

data = []
medir = definir_medir(osci, xze, xin, yze, ymu, yoff)
n = 1000
for i in range(n):
    print(i)
    data_aux = medir()
    data.append(data_aux)
    time.sleep(.03)

# data = []
# n = 2
# for i in range(n):
#     print(i)
#     data_aux = [1,2,3]
#     data.append(data_aux)
#     time.sleep(.03)

np.savetxt('mediciones_lento_10us.txt', data, delimiter='\t', newline='\n')

osci.close()