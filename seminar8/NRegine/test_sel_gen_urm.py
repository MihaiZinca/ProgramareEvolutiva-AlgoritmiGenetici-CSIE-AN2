# script pentru testul selectiei generatiei urmatoare - selectia de tip elitist
import numpy as np
from FunctiiSelectii import elitism
import generare_init as gi
import matplotlib.pyplot as grafic


#generarea aleatoare a doua populatii
dim=6
n=16
p1=gi.gen(n,dim)
p2=gi.gen(n,dim)
genu,valori=elitism(p1[:,:n],p1[:,n],p2[:,:n],p2[:,n],dim)
#constituirea populatiei rezultate
rez=np.zeros([dim,n+1],dtype='int')
rez[:,:n]=genu.copy()
rez[:,n]=valori.copy()
print('populatia1')
print(p1)
print('populatia2')
print(p2)
print('selectat:')
print(rez)

grafic.plot(p1[:,n],"go",markersize=18,label='Populatia curenta')
grafic.plot(p2[:,n],"bo",markersize=14,label='Copiii eventual mutati')
grafic.plot(rez[:,n],"ro",markersize=10,label='Generatia urmatoare')
grafic.legend()
grafic.show()
