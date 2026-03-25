import numpy as np
import matplotlib.pyplot as grafic
from FunctiiCrossoverIndivizi import crossover_OCX, crossover_CX

#f. obiectiv
def foNR(x):
    # functia obiectiv pentru problema reginelor

    # I: x - individul (permutarea) evaluat(a), n-dimensiunea problemei
    # E: c - calitate (numarul de perechi de regine care nu se ataca

    n=x.size
    c=len([(i,j) for i in range(n-1) for j in range(i+1,n) if abs(i-j)!=abs(x[i]-x[j])])

    return c

#genereaza populatia initiala
#I:
# n - dimensiunea prolemei
# dim - numarul de indivizi din populatie
#E: pop - populatia initiala
def gen(n,dim):
    #defineste o variabila ndarray cu toate elementelo nule
    pop=np.zeros((dim,n+1),dtype="int")
    for i in range(dim):
        #genereaza candidatul permutare cu n elemente
        pop[i,:n]=np.random.permutation(n)
        pop[i,n]=foNR(pop[i,:n])
    return pop



#crossover pe populatia de parinti pop, de dimensiune dimx(n+1)
# I: pop,dim,n - ca mai sus
#     pc- probabilitatea de crossover
#E: po - populatia copiilor
# este implementata recombinarea asexuata
def crossover_populatie(pop,pc):
    #initializeaza populatia de copii, po, cu populatia parintilor
    dim=pop.shape[0]
    m=pop.shape[1]
    n=m-1
    po=pop.copy()
    #populatia este parcursa astfel incat sunt selectati indivizii 0,1 apoi 2,3 s.a.m.d
    for i in range(0,dim-1,2):
        #selecteaza parintii
        x = pop[i,:-1]
        y = pop[i+1,:-1]
        r = np.random.uniform(0,1)
        if r<=pc:
            # crossover x cu y - OCX sau CX - potrivit pentru NRegine
            c1,c2 = crossover_OCX(x,y,n)
            val1=foNR(c1)
            val2= foNR(c2)
            po[i][:n]=c1.copy()
            po[i][n]=val1
            po[i+1][:n]=c2.copy()
            po[i+1][n]=val2
    figureaza(pop[:,n],po[:,n],dim)
    return po

def figureaza(valori,val,dim):
    grafic.plot(valori, "go", markersize=12,label='Parinti')
    grafic.plot(val, "ro", markersize=9,label='Copii')
    #includerea unei legende
    grafic.legend(loc="lower left")
    grafic.xlabel('Indivizi')
    grafic.ylabel('Fitness')
    grafic.show()


if __name__=="__main__":
    p=gen(10,8)
    o=crossover_populatie(p,0.8)

