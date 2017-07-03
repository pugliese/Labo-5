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
plt.figure(2)
plt.plot(Corr/CorrIdeal)

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
    plt.plot(Coso*np.conj(Coso))
    Tcs2.append(sum(FFT*np.conj(FFT))/sum(TFFT*(FFT*np.conj(FFT))))
    


## Autocorrelacion "constante"
def AutoCorrelacion(datos):
    N = len(datos)
    temp = np.zeros(N)
    for n in range(N):
    	prod = datos[n:N]*datos[0:(N-n)]
    	temp[n] =1./(N-n)*np.sum(prod)
    
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


def Convolucion1(A,B):
    N = len(A)
    res = np.zeros(N)
    for i in range(0,N):
        res[i] = sum([A[j]*beta(0<i-j)*B[i-j] for j in range(0,N)])
    return res

def Convolucion2(A,B):
    N = len(A)
    res = np.zeros(N)
    for i in range(0,N):
        res[i] = sum([A[j]*beta(j+i<N)*B[min(j+i,N-1)] for j in range(0,N)])
    return res

def Convolucion3(A,B):
    N = len(A)
    res = np.zeros(N)
    for i in range(0,N):
        res[i] = sum([A[j]*B[i-j] for j in range(0,N)])
    return res

def Convolucion4(A,B):
    N = len(A)
    res = np.zeros(N)
    for i in range(0,N):
        res[i] = sum([A[j]*B[(i+j)%N] for j in range(0,N)])
    return res

def ConvolucionRePiola(A,B):
    N = len(A)
    res = np.zeros(N)
    for i in range(-N/2,N/2):
        res[i] = sum([A[j]*B[(i+N/2+j)%N] for j in range(0,N)])
    return res


def beta(Q):
    if Q==1:
        return 1
    else:
        return 0

plt.figure(1)
plt.plot(Convolucion1(Voltajes[0],Voltajes[0]))
plt.title("En reversa")
plt.figure(2)
plt.plot(Convolucion2(Voltajes[0],Voltajes[0]))
plt.title("En directa")
plt.figure(3)
plt.plot(Convolucion3(Voltajes[0],Voltajes[0]))
plt.title("Periodica reversa")
plt.figure(4)
plt.plot(Convolucion4(Voltajes[0],Voltajes[0]))
plt.title("Periodica directa")

plt.figure(4)
plt.plot(range(-1250,1250),ConvolucionRePiola(Voltajes[0],Voltajes[0]))
plt.title("Periodica Repiola")


Anchos = []
for i in range(10):
    plt.figure(i)
    C = ConvolucionRePiola(Voltajes[i],Voltajes[i])
    plt.plot(range(-1250,1250),C,".-")
    plt.grid()
    Anchos.append(ancho(C))
    
    
Anchos2 = []
for i in range(10):
    plt.figure(i)
    C = ConvolucionRePiola(Voltajes[i],Voltajes[i])
    Anchos2.append(ancho2(C))
    


def ancho2(data):
    N = len(data)
    i = N/2
    m = min(data)
    M = max(data)
    while (data[i]>(M+m)/2):
        i+=1
    return i-N/2

N=2500
plt.rc('font', size = 22)
plt.xlabel("Desfasaje [ms]", fontsize=28)
plt.ylabel("Autocorrelacion", fontsize=28)
plt.plot(np.arange(-N/2,N/2)*.01/2.5,ConvolucionRePiola(Voltajes[7],Voltajes[7]) , "b-")
#plt.title("Ejemplo de autocorrelacion")
plt.axis([-5, 5, .905, 1.0])
plt.grid()
plt.figure(2)
n = 120
plt.plot(np.arange(-n,n)*.01/2.5,ConvolucionRePiola(Voltajes[7],Voltajes[7])[N/2-n:N/2+n] , "r-")
plt.axis([-0.5, 0.5, .905, 1.0])
plt.title("Ampliacion")
plt.grid()
plt.xlabel("Desfasaje [ms]", fontsize=28)
plt.ylabel("Autocorrelacion", fontsize=28)