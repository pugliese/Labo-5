#script general para hacer una corrida a un set de parametros,
#beta, tamano de la red,

import numpy as np
from matplotlib import pyplot
from random import randint
import scipy as sc
#############################################################
# estas son las funciones que tienen que escribir ustedes
# calcMagnet ya esta lista

def sumvec (S,i,j):
    n = np.size(S,0)
    m = np.size(S,1)
    return S[(i+1)%n,j]+S[i,(j+1)%m]+S[(i-1)%n,j]+S[i,(j-1)%m]

def calcMagnet(S):
    M = np.sum(S)
    return M

def calcEnergia(S):
    n = np.size(S,0)
    m = np.size(S,1)
    res=0
    for i in range(n):
        for j in range(m):
            res += S[i,j]*sumvec(S,i,j)/2
    return res

def ising2Dpaso(S, beta):
    n = np.size(S,0)
    m = np.size(S,1)
    i = randint(0,n-1)
    j = randint(0,m-1)
    dE = 2*S[i,j]*sumvec(S,i,j)
    p = np.exp(-beta*dE)
    r = np.random.rand(1,1)
    if(r<p):
        S[i,j] = -S[i,j]
        return S, dE, 2*S[i,j]
    else:
        return S, 0, 0
    
#############################################################

#Aca defino los parametros y corro la cadena de markov
#Lado de la red,
#L = 10
# beta = 1/T
#beta = 0.1

#propongo un estado inicial al azar
#S es una matriz de 1 y -1 indicando las dos proyecciones de
#espin
#S = 2*(np.random.rand(L,L)>0.5) -1;

#npre = 100
#npasos = 1000
#energia= np.zeros(npasos)
#magnet = np.zeros(npasos)

#pretermalizo
#ising2Dpaso hace un nuevo elemento de la cadena de Markov
#la tienen que escribir Uds...
#for n in range(npre):
#    S, dE, dM = ising2Dpaso(S,beta)

# muestro el estado inicial
#pyplot.imshow(S,interpolation='none')
#pyplot.show(block=False)

#energia[0] = calcEnergia(S)
#magnet[0] = calcMagnet(S)

#for n in range(npasos-1):
#    S, dE, dM = ising2Dpaso(S,beta);
   # energia[n+1] = energia[n] + dE;
  #  magnet[n+1] = magnet[n] + dM;
    
    #cada 10 pasos muestro el nuevo estado
    #if n%10 == 0:
     #   pyplot.imshow(S,interpolation='none')
      #  pyplot.title("n=%i beta=%.2f mag=%.2f energia=%.2f"%(n,beta,magnet[n],energia[n]))
       # pyplot.draw()
        
        
def Termalizacion(L,N,beta):
    S = 2*(np.random.rand(L,L)>0.5) -1; 
    energia = np.zeros(N)
    magnet = np.zeros(N)
    energia[0] = calcEnergia(S)
    magnet[0] = calcMagnet(S)
    for n in range(N-1):
        S, dE, dM = ising2Dpaso(S,beta);
        energia[n+1] = energia[n] + dE;
        magnet[n+1] = magnet[n] + dM;
    return energia, magnet

def Termalizar (S,T,k):
    for i in range (k):
        beta = 1./T
        S, dE, dM = ising2Dpaso(S,beta)
    return S

def Muestras(S,L,N,beta):
    energia = np.zeros(N)
    magnet = np.zeros(N)
    energia[0] = calcEnergia(S)
    magnet[0] = calcMagnet(S)
    for i in range(N-1):
        S,dE,dM=ising2Dpaso(S,beta)
        energia[i+1]=energia[i]+dE
        magnet[i+1]=magnet[i]+dM
    return energia, magnet    
    
def Critico(L,Ts,N, kv=100):
    k = kv*L*L
    S = 2*(np.random.rand(L,L)>0.5) -1; 
    U = np.zeros(len(Ts))
    M = np.zeros(len(Ts))
    Cv = np.zeros(len(Ts))
    X = np.zeros(len(Ts))
    for j in range (len(Ts)):
        beta = 1.0/Ts[j]
        for i in range(k):
            S,dE,dM = ising2Dpaso(S,beta)            
        E, R = Muestras(S,L,N,1./Ts[j])
        U[j] = np.mean(E)
        M[j] = np.mean(R)
        Cv[j] =np.var(E)*beta**2
        X[j] = np.var(R)*beta
    return U, M ,Cv, X     

def Correlacion (L,T,N,k):
    S = 2*(np.random.rand(L,L)>0.5) -1;
    S = Termalizar (S,T,k)
    Sf = np.zeros(L/2)
#    Sc = np.zeros(L/2)
    S1S2f = np.zeros(L/2)
#    S1S2c = np.zeros(L)
    for i in range(N):
        S, dE, dM = ising2Dpaso(S,1./T);
        for j in range(L/2):
            Sf[j] += float(S[0,j])/N;
#            Sc[j] += float(S[j,0])/N;
            S1S2f[j] += S[0,0]*float(S[0,j])/N;
#            S1S2c[j] += S[0,0]*float(S[j,0])/N;
    return S1S2f-Sf[0]*Sf

def CorrProm(L,T,N,k):
    res = np.zeros(L/2)
    for i in range(100):
        res+=Correlacion(L,T, N,k)
    return res/100

def C(P,L,T,N,k):
    res = np.zeros((len(T),len(P)))
    for i in range(len(T)):
        x = Correlacion(L,T[i],N,k)
        for j in range(len(P)):
            res[i,j] = x[P[j]]
    return res

def integral(C):
    return sum(C[1:]/C[0])

def FuncCorr(x,c,L=32):
    return (1-np.exp(-0.5*L/x))*x-c

def LongCorr(C,L=32):
    c = integral(C)
    G = lambda x: FuncCorr(x,c,L)
    return sc.optimize.brenth(G,0.1,16)


A17=CorrProm(32,1.7,50000,50000)
A20=CorrProm(32,2.2,50000,50000)
A22=CorrProm(32,2.2,50000,50000)
A24=CorrProm(32,2.2,50000,50000)
A27=CorrProm(32,2.7,50000,50000)
A32=CorrProm(32,3.2,50000,50000)
pyplot.plot(range(16),abs(A17)/A17[0], "b^--")
pyplot.plot(range(16),abs(A20)/A20[0], "ro--")
pyplot.plot(range(16),abs(A22)/A22[0], "r--")
pyplot.plot(range(16),abs(A24)/A24[0], "yv--")
pyplot.plot(range(16),abs(A27)/A27[0], "yv--")
pyplot.plot(range(16),abs(A32)/A32[0], "k.--")
pyplot.grid()

plt.figure(1)
plt.plot(np.linspace(1.5,3,16),Crit[0]/1024, "o--")
plt.figure(2)
plt.plot(np.linspace(1.5,3,16),Crit[1]/1024, "o--")
plt.figure(3)
plt.plot(np.linspace(1.5,3,16),Crit[2]/1024, "o--")
plt.figure(4)
plt.plot(np.linspace(1.5,3,16),Crit[3]/1024, "o--")



Term1 = Termalizacion(32,1000000,1/1.2)
Term2 = Termalizacion(32,1000000,1./1.5)
Term3 = Termalizacion(32,1000000,1./1.8)
Term4 = Termalizacion(32,1000000,1./2.1)

plt.plot(Term1, "b-")
plt.plot(Term2, "y-")
plt.plot(Term3, "k-")
plt.plot(Term4, "r-")