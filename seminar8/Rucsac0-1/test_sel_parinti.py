# script pentru testul selectiei parintilor - selectia de tip turneu
import numpy as np
from FunctiiSelectii import turneu
import generare_init as gi
import matplotlib.pyplot as grafic
import copy
#pentru legenda - afisare ajustata
#generarea aleatoare a unei populatii
dim=10
cmax=30
k=2
c=np.genfromtxt("cost.txt")
v=np.genfromtxt("valoare.txt")

L=gi.gen(c,v,cmax,dim)
pop_copie=copy.deepcopy([L[i][:-1] for i in range(len(L))])
cal_copie=copy.deepcopy([L[i][-1] for i in range(len(L))])
parinti,valori=turneu(pop_copie,cal_copie,dim,c.size,k)
print([L[i][:-1] for i in range(len(L))])
print(parinti)

grafic.plot([L[i][-1] for i in range(len(L))],"go",markersize=16,label="Populatia curenta")
grafic.plot(valori,"ro",markersize=10,label="Populatia de parinti")
grafic.legend(loc="lower left")
grafic.show()

