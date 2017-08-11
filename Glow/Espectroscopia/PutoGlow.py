# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sc

def cargar(x):
    file = open(x, "r")  ## Abro el archivo en modo de lectura
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
    return data

##Bajada
Ib = [0.30, 0.43, 0.59, 0.66, 0.74, 0.82, 0.92, 1.01, 1.13] ## Los de la derecha en el nombre del archivo
Vb = [0.56, 0.628, 0.695,0.727,0.761,0.791,0.822,0.851,0.876] ## Los de la izquierda en el nombre del archivo

##Subida
Is = [0.31, 0.45, 0.60, 0.77, 0.95, 1.14, 1.23] ##Los de la derecha
Vs = [0.557, 0.625, 0.69, 0.753, 0.814, 0.875, 0.90] ##Los de la izquierda

LdO = [391, 427, 777] ##Longitudes de onda

"""
[0,:] = 'Time[s]'
[1,:] = 'Mean Value[Intensity]'
[2,:] = 'Variance[-]'
[3,:] = 'Standard Deviation[Intensity]'
[4,:] = 'Weighted Average[nm(vac)]'
[5,:] = 'Max Value[Intensity]'      
 """     

#x = "27-06/777nm/bajada/0.56V-0.30V.csv"
#data = cargar(x)
res1 = np.zeros((len(LdO),len(Ib)))
for j in range(len(LdO)):
    for i in range(len(Ib)):
        #x = '27-06/'+str(LdO[j])+'nm/Bajada/'+str(Vb[i])+'V-'+str(Ib[i])+'V'+'.csv'
        x = 'NombresCorregidos/'+str(LdO[j])+'nm/Bajada/'+str(Vb[i])+'V-'+str(Ib[i])+'V'+'.csv'
        data = cargar(x)
        res1[j,i] = np.mean(data[5,:])

res2 = np.zeros((len(LdO),len(Is)))
for j in range(len(LdO)):
    for i in range(len(Is)):
        #x = '27-06/'+str(LdO[j])+'nm/Subida/'+str(Vs[i])+'V-'+str(Is[i])+'V'+'.csv'
        x = 'NombresCorregidos/'+str(LdO[j])+'nm/Subida/'+str(Vs[i])+'V-'+str(Is[i])+'V'+'.csv'
        data = cargar(x)
        res2[j,i] = np.mean(data[5,:])
col = ['k','b','r']

Ib = [Ib[i]/150 for i in range(len(Ib))]
Is = [Is[i]/150 for i in range(len(Is))]
Vb = [1000*Vb[i] for i in range(len(Vb))]
Vs = [1000*Vs[i] for i in range(len(Vs))]

Leg = ['391nm(bajada)','391nm(subida)','427nm(bajada)','427nm(subida)','777nm(bajada)','777nm(subida)']
for j in range(len(LdO)):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(Ib,res1[j,:],str(col[j])+'o--')
    plt.plot(Is,res2[j,:],str(col[j])+'s--')
    plt.subplot(212)
    plt.plot(Vb,res1[j,:],str(col[j])+'o--')
    plt.plot(Vs,res2[j,:],str(col[j])+'s--')
plt.figure(1)
plt.subplot(211)
plt.legend(Leg)
plt.ylabel('Intensidad')
plt.xlabel('Corriente[mA]')
plt.subplot(212)
plt.legend(Leg)
plt.ylabel('Intensidad')
plt.xlabel('Tension[V]')
plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,wspace=0.35)
plt.show()

Aj_s = np.zeros((len(LdO),5))
Aj_b = np.zeros((len(LdO),5))
for j in range(len(LdO)):
    Aj_b[j,:] = sc.linregress(Ib,res1[j,:])
    Aj_s[j,:] = sc.linregress(Is,res2[j,:])

# Ajustes de las rectas

plt.figure(2)
plt.plot(LdO,Aj_s[:,0],"ro")
plt.plot(LdO,Aj_b[:,0],"k^")
plt.grid()
plt.xlabel("Longitud de onda")
plt.ylabel("Pendiente")
plt.legend(["Subida","Bajada"])


plt.figure(3)
plt.plot(LdO,Aj_s[:,1],"ro")
plt.plot(LdO,Aj_b[:,1],"k^")
plt.grid()
plt.xlabel("Longitud de onda")
plt.ylabel("Ordenada")
plt.legend(["Subida","Bajada"])


# Caracterizacion de la emision

def Lambda(Z,k): # Z es el numero atomico y k es el nivel del que esta decayendo (decae de k a k-1)
    Lambda_o = 90.11  # Acumulacion turbia de constantes que googlie
    return Lambda_o/(2*k-1)*(k*(k-1)/Z)**2

X_N = np.linspace(1,10,10)
X_O = np.linspace(1,10,10)
X_Ar = np.linspace(1,18,18)

plt.plot(Lambda(7,X_N),X_N, "ro")
plt.plot(Lambda(8,X_O),X_O, "bo")
plt.plot(Lambda(18,X_Ar),X_Ar, "ko")
plt.grid()
plt.xlabel("Longitud de onda")
plt.ylabel("Nivel")
plt.plot([391, 391],[0,18])
plt.plot([427, 427],[0,18])
plt.plot([777, 777],[0,18])
plt.axis([0,800,0,18])
plt.legend(["Nitrogeno", "Oxigeno","Argon"])


I_N_b = res1[0,:]+res1[2,:] ## Intensidad emitida por el nitrogeno
I_N_s = res2[0,:]+res2[2,:]
I_O_b = res1[1,:]  ## Intensidad emitida por el oxigeno
I_O_s = res2[1,:]

plt.plot(Is,I_N_s/(I_N_s+I_O_s), "ro")
plt.plot(Ib,I_N_b/(I_N_b+I_O_b), "bo")

C_N_s = (np.mean(I_N_s/(I_N_s+I_O_s)),np.std(I_N_s/(I_N_s+I_O_s)))
C_N_b = (np.mean(I_N_b/(I_N_b+I_O_b)),np.std(I_N_b/(I_N_b+I_O_b)))

C_O_s = (np.mean(I_O_s/(I_N_s+I_O_s)),np.std(I_O_s/(I_N_s+I_O_s)))
C_O_b = (np.mean(I_O_b/(I_N_b+I_O_b)),np.std(I_O_b/(I_N_b+I_O_b)))



### GRAFICOS PARA LA PRESENTACION

#Intensidades Nitrogeno 
#Bajada y bajda
plt.plot([],[], "ko--")
plt.plot([],[], "ks--")
plt.plot(np.array(Ib)/.15,100*res1[0,:]/(I_N_b+I_O_b), "bo--")
plt.plot(np.array(Ib)/.15,100*res1[2,:]/(I_N_b+I_O_b), "bs--")
plt.plot(np.array(Is)/.15,100*res2[0,:]/(I_N_s+I_O_s), "ro--")
plt.plot(np.array(Is)/.15,100*res2[2,:]/(I_N_s+I_O_s), "rs--")
plt.xlabel("Corriente [mA]",fontsize=16)
plt.ylabel("Intensidad relativa [%]",fontsize=16)
plt.legend(["391nm", "777nm"],fontsize=16)
plt.savefig("Dist_Nit.png")
plt.close()
#Total
plt.tick_params(axis='both', which='major', labelsize=12)
plt.plot(np.array(Ib)/.15,100*I_N_b/(I_N_b+I_O_b), "bo--")
plt.plot(np.array(Is)/.15,100*I_N_s/(I_N_s+I_O_s), "ro--")
plt.xlabel("Corriente [mA]",fontsize=16)
plt.ylabel("Intensidad relativa[%]",fontsize=16)
plt.title("Nitrogeno")
plt.savefig("Int_Nit.png")
plt.close()