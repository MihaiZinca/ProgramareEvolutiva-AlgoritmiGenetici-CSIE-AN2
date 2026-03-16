import numpy as np
from FunctiiMutatieIndivizi import m_neuniforma
import matplotlib.pyplot as grafic
import random
import copy


#verifica fezabilitatea alegerii x si calculeaza si f. obiectiv
def ok(x,c,v,max):
    val=np.dot(x,v)
    cost=np.dot(x,c)
    return cost<=max, val



#genereaza populatia initiala
#I:
# c, v - vectorii cost, valoare
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
            x=[random.uniform(0,1) for _ in range(n)]
            gata,val=ok(x,c,v,max)
        #am gasit o solutie candidat fezabila, in data de tip lista x
        # adauga valoarea
        x.append(val)
        #adauga la populatie noul individ cu valoarea f. obiectiv - adauga inca o lista cu n+1 elemente ca element al listei pop
        pop.append(x)
    vectv=[pop[i][-1] for i in range(dim)]
    grafic.plot(vectv, "gs", markersize=11,label="Initial")
    return pop

#aplica mutatie populatiei pop
#I:
#pop - populatia insotita de calitati - in GA populatia de copii
# c,v - vectorii cost, valoare
# max - capacitatea maxima
# dim - numarul de indivizi din populatie
# pm - probabilitatea de mutatie
# sigma - dimensiunea pasului de mutatie - mutatia neuniforma pentru numere reale
# E:
#mpop - populatia dupa mutatie
def mutatie_populatie(pop,c,v,max,pm,sigma):
    # copiem populatia curenta in rezultatul mpop
    mpop=copy.deepcopy(pop)
    dim=len(pop)
    n=c.size
    for i in range(dim):
        #copiem in x individul i
        x=pop[i][:n].copy()
        mutatie=False
        for j in range(n):
            #genereaza aleator daca se face mutatie in individul i gena j
            r=np.random.uniform(0,1)
            if r<=pm:
                #mutatie neuniforma
                x[j]=m_neuniforma(x[j],sigma,0,1)
                mutatie=True
        #individul rezultat sufera posibil mai multe mutatii
        #daca este fezabil, este pastrat
        if mutatie:
            fez, val = ok(x,c, v, max)
            if fez:
                x.append(val)
                mpop[i]=x.copy()
    grafic.plot([mpop[i][n] for i in range(dim)],"rs",markersize=7,label="Dupa mutatie")
    return mpop


if __name__=="__main__":
    max=50
    dim=12
    c=np.genfromtxt("cost.txt")
    v = np.genfromtxt("valoare.txt")
    p=gen(c,v,max,dim)
    o=mutatie_populatie(p,c,v,max,0.1,0.7)
    grafic.legend()
    grafic.show()


