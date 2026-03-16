# AICI POPULATIA ESTE O MATRICE CU LINII PERMUTARI, CALITATILE SUNT MEMORATE SEPARAT, INTR-UN VECTOR
import matplotlib.pyplot as grafic
import numpy as np


#f. obiectiv
def foTSP(p,c):
    n=p.size
    val = 0
    for i in range(n - 1):
        val+=c[p[i],p[i+1]]
    val = val+c[p[0]][p[n-1]]
    return 100/val

# figurarea populatiei prin punctele (indice individ, calitate) - pentru a vedea variabilitatea in populatie
def reprezinta_pop(val,dim):
    #fig = grafic.figure()
    x=[i for i in range(dim)]
    y=[val[i] for i in range(dim)]
    grafic.plot(x,y,"ro",markersize=7)
    grafic.title("Calitatile indivizilor generați în populația inițială")
    grafic.xlabel("Index individ")
    grafic.ylabel("Calitate individ")
    grafic.show()

#genereaza populatia initiala
#I:
# fc - numele fisierului costurilor
# dim - numarul de indivizi din populatie
#E: pop,val - populatia initiala si vectorul valorilor
def gen(fc,dim):
    #citeste datele din fisierul nxn al costurilor
    c=np.genfromtxt(fc)
    #n=dimensiunea problemei
    n = c.shape[0]  #len(c)
    pop=np.zeros((dim,n),dtype=int)
    val=np.zeros(dim,dtype=float)
    for i in range(dim):
        #genereaza candidatul permutare cu n elemente
        pop[i] = np.random.permutation(n)
        # evalueaza candidat
        val[i] = foTSP(pop[i,:n],c)
    reprezinta_pop(val,dim)
    return pop, val


if __name__=="__main__":
    p, v = gen("costuri.txt", 30)
    for i in range(p.shape[0]):
        print('Individul ', p[i],' cu valoarea ',v[i])
