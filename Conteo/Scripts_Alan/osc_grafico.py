# -*- coding: utf-8 -*-
"""
Osciloscopio Tektronix TDS1002B
Manual U (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TDS1002 Manual.pdf
Manual P (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TDS 100-1000-2000_prog.pdf
Manual U (local): \\Srvlabos\manuales\Tektronix\TDS1002 Manual.pdf
Manual P (local): \\Srvlabos\manuales\Tektronix\TDS 200-1000-2000_prog.pdf
"""

# Este script grafica UNA pantalla del osciloscopio y guarda datoas de tiempo y tension en txt

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

xze, xin, yze, ymu, yoff = osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')

osci.write('DAT:ENC RPB')
osci.write('DAT:WID 1')

data = osci.query_binary_values('CURV?', datatype='B', container=np.array)
data = -((data-yoff)*ymu + yze)

tiempo = xze + np.arange(len(data)) * xin

np.savetxt('grafico_de_prueba.txt', np.c_[tiempo,data], delimiter='\t', newline='\n')

plt.plot(tiempo, data)
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
plt.grid(True)
plt.show()

osci.close()