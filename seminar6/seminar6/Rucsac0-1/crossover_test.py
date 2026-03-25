import matplotlib.pyplot as grafic
import numpy as np
from FunctiiCrossoverIndivizi import crossover_uniform
import copy
import random


#verifica fezabilitatea alegerii x si calculeaza si f. obiectiv
def ok(x,c,v,max):
    val=np.dot(x,v)
    cost=np.dot(x,c)
    return cost<=max, val


#genereaza populatia initiala
#I:
# c,v - vectorii cost, valoare
# max - capacitatea maxima
# dim - numarul de indivizi din populatie
# E:
#pop - populatia insotita de calitati

def gen(c,v,max,dim):
    #n=dimensiunea problemei
    n=v.size
    #lucreaza cu populatia ca lista de dim elemente - liste cu cate n+1 indivizi
    pop=[]
    for i in range(dim):
        gata=False
        while gata == False:
            #genereaza candidatul x cu elemente 0,1
            #x=[random.choice([0,1]) for _ in range(n)]
            x=random.choices([0,1],k=n)
            gata,val=ok(x,c,v,max)
        #am gasit o solutie candidat fezabila, in data de tip lista x
        # adauga valoarea
        x.append(val)
        #adauga la populatie noul individ cu valoarea f. obiectiv - adauga inca o lista cu n+1 elemente ca element al listei pop
        pop.append(x)
    vectv=[pop[i][-1] for i in range(dim)]
    grafic.plot(vectv, "gs", markersize=11,label="Initial")
    return pop



#crossover pe populatia de parinti pop, de dimensiune dimx(n+1)
# I: pop - ca mai sus
#     c, v, max - datele problemei
#     pc- probabilitatea de crossover
#E: po - populatia copiilor, calitatile copiilor
# este implementata recombinarea asexuata
def crossover_populatie(pop,c,v,max,pc):
    dim=len(pop)
    n=c.size
    po=copy.deepcopy(pop)
    #populatia este parcursa astfel incat sunt selectati indivizii 0,1 apoi 2,3 s.a.m.d
    for i in range(0,dim-1,2):
        #selecteaza parintii
        x = pop[i][:-1].copy()
        y = pop[i+1][:-1].copy()
        r = np.random.uniform(0,1)
        if r<=pc:
            # crossover x cu y - uniform: mai potrivit aici
            c1,c2=crossover_uniform(x ,y ,n)
            fez, val = ok(c1, c, v, max)
            if fez:
                po[i][:-1]=c1.copy()
                po[i][-1]=val
            fez, val = ok(c2, c, v, max)
            if fez:
               po[i+1][:-1]=c2.copy()
               po[i+1][-1]=val
    vectv = [po[i][-1] for i in range(dim)]
    grafic.plot( vectv, "rs", markersize=9, label="Dupa recombinare")
    return po




if __name__=="__main__":
    DMax=50
    c=np.genfromtxt("cost.txt")
    v=np.genfromtxt("valoare.txt")
    pop=gen(c,v,DMax,10)
    po=crossover_populatie(pop,c,v,DMax,0.8)
    grafic.legend()
    grafic.xlabel('Indivizi')
    grafic.ylabel('Fitness')
    grafic.show()

