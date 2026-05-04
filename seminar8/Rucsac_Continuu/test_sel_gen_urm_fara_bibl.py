# script pentru testul selectiei generatiei urmatoare - selectia de tip elitist
import numpy as np
import generare_init as gi
import matplotlib.pyplot as grafic
import copy

def elitism(p_curenta,c_p_curenta,copii,c_copii,dim):
    gen_urm=copy.deepcopy(copii)
    c_gen_urm=copy.deepcopy(c_copii)
    if max(c_p_curenta)>max(c_copii):
        indice_max=np.argmax(c_p_curenta)
        inlocuit=np.random.randint(dim)
        gen_urm[inlocuit]=copy.deepcopy(p_curenta[indice_max])
        c_gen_urm[inlocuit]=c_p_curenta[indice_max]
    return gen_urm, c_gen_urm


#generarea aleatoare a doua populatii
dim=12
cmax=30
c=np.genfromtxt("cost.txt")
v=np.genfromtxt("valoare.txt")

L1=gi.gen(c,v,cmax,dim)
L2=gi.gen(c,v,cmax,dim)
pop1=[L1[i][:-1] for i in range(len(L1))]
cal1=[L1[i][-1] for i in range(len(L1))]
pop2=[L2[i][:-1] for i in range(len(L2))]
cal2=[L2[i][-1] for i in range(len(L2))]
genu,valori=elitism(pop1,cal1,pop2,cal2,dim)


# print(pop1)
# print(pop2)
# print(genu)

grafic.plot(cal1,"go",markersize=18,label="Populatia curenta")
grafic.plot(cal2,"bo",markersize=14,label="Populatia de copii mutati")
grafic.plot(valori,"ro",markersize=11,label="Geneartia urmatoare")

grafic.legend()
grafic.show()

