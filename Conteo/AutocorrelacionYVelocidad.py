# -*- coding: utf-8 -*-
"""
Created on Thu May 04 12:36:10 2017

@author: Kufa
"""

Voltajes = data["Mediciones"]
for i in range(len(Voltajes)):
    Voltajes[i] = Voltajes[i]/np.sqrt(sum(Voltajes[i]*Voltajes[i]))
Ideal = (np.zeros((2500))+1)/np.sqrt(2500)
CorrIdeal = np.correlate(Ideal,Ideal,'same')
Corr = np.correlate(Voltajes[0],Voltajes[0],'same')

def Cero(V):
    inf = 0
    sup = len(V)/2
    while(inf+1<sup):
        med = (inf+sup)/2
        if(V[med]>0):
            sup = med
        else:
            inf = med
    if(abs(V[med+1])<abs(V[med])):
        med = med+1
    return med


## Rapaport (V1->0.75; V2->0.5)
Tcs = []
for i in range(len(Voltajes)):
    CorrIdeal = np.correlate(Ideal,Ideal,'same')
    Corr = np.correlate(Voltajes[i],Voltajes[i],'same')
    Tcs.append(2*(1250-Cero(Corr-.75))*.01/2500)
    
    
plt.rc('font', size = 22)
plt.xlabel("Desfasaje [ms]")
plt.ylabel("Autocorrelacion", fontsize=28)
plt.title("Ventana de 10ms con $\omega = (10.82\pm0.04)$Hz", fontsize=28)
T = (np.array(range(0,2500))-1250)*.01/2.5
plt.plot(T, Corr, "b-")
plt.plot(T, CorrIdeal, "r-")
plt.legend(("Medida","Ideal constante"), fontsize=28)
plt.grid()

Cero(Corr-.5)

## Braga
Tcs2 = []
for i in range(10):
    FFT=np.fft.fft(Voltajes[i])   ## Esta en ms
    TFFT = np.fft.fftfreq(2500,.01/2.5)
    Coso = np.fft.ifft(FFT*np.conj(FFT))
    plt.figure(i)
    plt.plot(Coso)
    Tcs2.append(sum(FFT*np.conj(FFT))/sum(TFFT*(FFT*np.conj(FFT))))
    


## Autocorrelacion "constante"
def AutoCorrelacion(datos):
    N = len(datos)
    temp = np.zeros(N)
    for n in range(N):
    	prod = datos[n:N]*datos[0:(N-n)]
    	temp[n] = 1/(N-n) * np.sum(prod)
    
    acorr = np.zeros(2*N-1)
    acorr[0:N] = temp
    for i in range(1,N):
    	acorr[-i] = temp[i]
    return acorr


## Datos de f(T)=w(T)/(2*pi)
# Lo hice en frecuencias porque pintó y así quedó

T = np.array([0.857, .581, .432, .344, .278, .232])
ET = np.array([.005, .002, .004, .005, .001, .001])
V = np.array([1.5, 2, 2.5, 3, 3.6 , 4.2])

plt.rc('font', size = 22)
plt.xlabel("Voltaje [V]")
plt.ylabel("Frecuencia [Hz]", fontsize=28)
plt.plot(V, 1/T, "bo")
plt.plot(V, 1.167*V-.59, "r-")
plt.legend(("Medido","Ajuste lineal"), fontsize=28)
plt.grid()


