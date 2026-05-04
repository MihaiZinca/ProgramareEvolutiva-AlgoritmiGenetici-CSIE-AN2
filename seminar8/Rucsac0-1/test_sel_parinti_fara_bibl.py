# script pentru testul selectiei parintilor - selectia de tip turneu
import numpy as np
import generare_init as gi
import matplotlib.pyplot as grafic
#pentru legenda - afisare ajustata
#generarea aleatoare a unei populatii
def turneu(pop,cal,dim,k):
    parinti=[]
    calitati=[]
    for i in range(dim):
        pozitii=np.random.randint(0,dim,k)
        multime_cal=[cal[pozitii[t]] for t in range(k)]
        indice_individ=np.argmax(multime_cal)
        parinti.append(pop[pozitii[indice_individ]])
        calitati.append(cal[pozitii[indice_individ]])
    return parinti, calitati


dim=10
cmax=30
k=2
c=np.genfromtxt("cost.txt")
v=np.genfromtxt("valoare.txt")

L=gi.gen(c,v,cmax,dim)
pop=[L[i][:-1] for i in range(len(L))]
cal=[L[i][-1] for i in range(len(L))]

parinti,valori=turneu(pop,cal,dim,k)

# print(pop)
# print(parinti)
grafic.plot(cal,"go",markersize=16,label="Populatia curenta")
grafic.plot(valori,"ro",markersize=10,label="Populatia de parinti")
grafic.legend()
grafic.show()

