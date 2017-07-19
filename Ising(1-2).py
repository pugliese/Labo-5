#script general para hacer una corrida a un set de parametros,
#beta, tamano de la red,

import numpy as np
import matplotlib.pyplot as plt
from random import randint
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
            res += -S[i,j]*sumvec(S,i,j)/2
    return res

def ising2Dpaso(S, T):
    n = np.size(S,0)
    m = np.size(S,1)
    i = randint(0,n-1)
    j = randint(0,m-1)
    dE = float(2*S[i,j]*sumvec(S,i,j))
    p = np.exp(-dE/T)
    r = np.random.rand(1,1)
    if(r<p):
        S[i,j] = -S[i,j]
        return S, dE, 2*S[i,j]
    else:
        return S, 0, 0
    
def Termalizacion(L,N,T):
    S = 2*(np.random.rand(L,L)>0.5) -1; 
    energia = np.zeros(N)
    magnet = np.zeros(N)
    energia[0] = calcEnergia(S)
    magnet[0] = calcMagnet(S)
    for n in range(N-1):
        S, dE, dM = ising2Dpaso(S,T);
        energia[n+1] = energia[n] + dE;
        magnet[n+1] = magnet[n] + dM;
    return energia, magnet

def Termalizar (S,T,k):
    for i in range (k):
        S, dE, dM = ising2Dpaso(S,T)
    return S

def Muestras(S,L,N,T):
    energia = np.zeros(N)
    magnet = np.zeros(N)
    energia[0] = calcEnergia(S)
    magnet[0] = calcMagnet(S)
    for i in range(N-1):
        S,dE,dM=ising2Dpaso(S,T)
        energia[i+1]=energia[i]+dE
        magnet[i+1]=magnet[i]+dM
    return energia, magnet    
    
def Critico(L,Ts,N, kv):
    k = kv*L*L
    S = 2*(np.random.rand(L,L)>0.5) -1; 
    U = np.zeros(len(Ts))
    M = np.zeros(len(Ts))
    Cv = np.zeros(len(Ts))
    X = np.zeros(len(Ts))
    for j in range (len(Ts)):
        S = Termalizar(S,Ts[j],k)            
        E, R = Muestras(S,L,N,Ts[j])
        #print np.mean(E), np.mean(R)
        U[j] = np.mean(E)
        M[j] = np.mean(R)
        Cv[j] =np.var(E)/Ts[j]**2
        X[j] = np.var(R)/Ts[j]
    return U, M ,Cv, X     

def Correlacion (L,T,N,k):
    S = 2*(np.random.rand(L,L)>0.5) -1;
    S,dE,dM = Termalizar (S,T,k)
    Sf = np.zeros(L/2)
    Sc = np.zeros(L/2)
    S1S2f = np.zeros(L/2)
#    S1S2c = np.zeros(L)
    for i in range(N):
        S, dE, dM = ising2Dpaso(S,T);
        for j in range(L/2):
#            Sf[j] += float(S[0,j])/N;
            Sc[j] += float(S[j,0])/N;
            S1S2f[j] += S[0,0]*float(S[0,j])/N;
#            S1S2c[j] += S[0,0]*float(S[j,0])/N;
    return S1S2f-Sf[0]*Sf

def CorrProm(L,T,N,k):
    res = np.zeros(L/2)
    for i in range(25):
        res+=Correlacion(L,T, N,k)
    return res/25

def C(P,L,T,N,k):
    res = np.zeros((len(T),len(P)))
    for i in range(len(T)):
        x = Correlacion(L,T[i],N,k)
        for j in range(len(P)):
            res[i,j] = x[P[j]]
    return res

##############ejercicio1##############
def aux1_1(T,L,N): #T vector de temperatura, L fijo--- Usar eso para el item a
    P = [i for i in range(N)]
    d = int(len(T))
    x = np.zeros((d,N))
    y = np.zeros((d,N))
    Leg = ["T = %1.3f" %T[i] for i in range(len(T))]
    Lin = ['s','^','--']
    for i in range(d):
        S = 2*(np.random.rand(L,L)>0.5) -1
        y[i,:] , x[i,:] = Muestras(S,L,N,T[i])
        plt.figure(1)
        plt.subplot(211)
        plt.plot(P,np.abs(x[i,:])/(L*L),Lin[i])
        plt.subplot(212)
        plt.plot(P,y[i,:]/(L*L),Lin[i])
    plt.figure(1)
    plt.subplot(211)
    plt.legend(Leg)
    plt.title('L = 16', fontsize = 14)
    plt.xlabel('Iteración', fontsize = 14)
    plt.ylabel('Magnetizacion por spin',fontsize = 14)
    plt.subplot(212)
    plt.legend(Leg)
    plt.xlabel('Iteración', fontsize = 14)
    plt.ylabel('Energia por spin', fontsize = 14)
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,wspace=0.35)
  
def aux1_2(T,L,N): #T fijo,L vector de dimensiones--- Usar esto para el item b
    P = [i for i in range(N)]
    d = int(len(L))
    x = np.zeros((d,N))
    y = np.zeros((d,N))
    Leg = np.zeros(d)
    for i in range(d):
        Leg[i] = str(int(L[i]))
    for i in range(d):
        a = int(L[i])
        S = 2*(np.random.rand(a,a)>0.5) -1
        y[i,:] , x[i,:] = Muestras(S,a,N,T)
    for i in range(d):
        plt.figure(1)
        plt.subplot(211)
        plt.plot(P,np.abs(x[i,:])/(L[i]*L[i]),'--')
        plt.subplot(212)
        plt.plot(P,y[i,:]/(L[i]*L[i]),'--')
    plt.figure(1)
    plt.subplot(211)
    plt.legend(Leg)
    plt.title('T = '+str(T), fontsize = 14)
    plt.xlabel('Iteración', fontsize = 14)
    plt.ylabel('Magnetizacion por spin',fontsize = 14)
    plt.subplot(212)
    plt.legend(Leg)
    plt.xlabel('Iteración', fontsize = 14)
    plt.ylabel('Energia por spin', fontsize = 14)
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,wspace=0.35)
    
############ ejercicio2 ##############
# Parametros copados (a ojo)
# kv = 100
# 50*L*L < N < 100*L*L

def aux2(L,Ts,N, kv):
    k = kv*L*L
    U = np.zeros(len(Ts))
    M = np.zeros(len(Ts))
    Cv = np.zeros(len(Ts))
    X = np.zeros(len(Ts))
    S = 2*(np.random.rand(L,L)>0.5) -1;
    for j in range (1,len(Ts)+1):
        S = Termalizar(S,Ts[-j],k)      
        E, R = Muestras(S,L,N,Ts[-j])
        if (Ts[-j]<2):
            W = np.abs(R)
        else:
            W = R
        U[-j] = np.mean(E)
        M[-j] = np.mean(R)
        Cv[-j] = np.var(E)/(Ts[-j]**2)
        X[-j] = np.var(R)/(Ts[-j])
        #Ver(S,j+3)
    plt.figure(1)
    plt.subplot(211)
    plt.plot(Ts,U,'o--')
    plt.xlabel('Temperatura', fontsize = 14)
    plt.ylabel('Energia media',fontsize = 14)
    plt.subplot(212)
    plt.plot(Ts,np.abs(M),'o--')
    plt.xlabel('Temperatura', fontsize = 14)
    plt.ylabel('Magnetizacion media',fontsize = 14)
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,wspace=0.35)
    plt.figure(2)
    plt.subplot(211)
    plt.plot(Ts,Cv,'o--')
    plt.xlabel('Temperatura', fontsize = 14)
    plt.ylabel('Calor especifico',fontsize = 14)
    plt.subplot(212)
    plt.plot(Ts,X,'o--')
    plt.xlabel('Temperatura', fontsize = 14)
    plt.ylabel('Suceptibilidad magnetica',fontsize = 14)
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,wspace=0.35)
    
    
    
    
######### Visualizar #########

def Ver(S,j=10):
    plt.figure(j)
    plt.imshow(S,interpolation='none')
    #plt.title("n=%i beta=%.2f mag=%.2f energia=%.2f"%(n,beta,magnet[n],energia[n]))
    plt.draw()
    