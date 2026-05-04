# script pentru testul selectiei generatiei urmatoare - selectia de tip elitist
import numpy as np
from FunctiiSelectii import elitism
import generare_init as gi
import matplotlib.pyplot as grafic


#generarea aleatoare a doua populatii
dim=12
c=np.genfromtxt("costuri.txt")
p1,v1=gi.gen(c,dim)
p2,v2=gi.gen(c,dim)
genu,valori=elitism(p1,v1,p2,v2,dim)
print('populatia1 cu valori')
print(v1)
print('populatia2 cu valori')
print(v2)
print('selectat:')
print(valori)

# print(p1)
# print(p2)
# print(genu)

grafic.plot(v1,"go",markersize=18,label='Populatia curenta')
grafic.plot(v2,"bo",markersize=14,label='Populatia de copii')
grafic.plot(valori,"ro",markersize=10,label='Generatia urmatoare')
grafic.legend()
grafic.show()

