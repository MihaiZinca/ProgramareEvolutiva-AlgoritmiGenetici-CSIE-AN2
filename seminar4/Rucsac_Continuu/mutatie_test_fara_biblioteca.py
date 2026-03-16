import numpy as np
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

# mutatie neuniforma pentru numarul real x din (a,b)

def mutatie_neuniforma(x,sigma,a,b):
    perturbare=random.gauss(0,sigma)
    #perturbare=np.random.normal(0,sigma)
    y=x+perturbare
    if y<a:
        y=a
    elif y>b:
        y=b
    return y

#aplica mutatie populatiei copii
#I:
#copii - populatia insotita de calitati - in GA populatia de copii
# c,v - vectorii cost, valoare
# max - capacitatea maxima
# dim - numarul de indivizi din populatie
# pm - probabilitatea de mutatie
# sigma - dimensiunea pasului de mutatie - mutatia neuniforma pentru numere reale
# E:
#copii_m - populatia dupa mutatie
def mutatie_populatie(copii,c,v,cmax,pm,sigma):
    copii_m=copy.deepcopy(copii)
    dimensiune=len(copii)
    n=c.size
    for i in range(dimensiune):
        # selecteaza individul i, dar fara calitatea asociata
        x=copii_m[i][:-1].copy()
        mutatie=False
        for j in range(n):
            # verifica daca se face mutatie in individul i, gena j
            raspuns=random.uniform(0,1)
            if raspuns<=pm:
                #aplica mutatia
                x[j]=mutatie_neuniforma(x[j],sigma,0,1)
                mutatie=True
        #verifica daca s-a aplicat mutatia
        if mutatie:
            fezabil,val=ok(x,c,v,max)
            # pastram individul mutat doar daca este fezabil
            if fezabil:
                x.append(val)
                copii_m[i]=x.copy()
    # figurare calitati
    grafic.plot([copii_m[i][n] for i in range(dimensiune)],"rs",markersize=7,label="Dupa mutatie")
    return copii_m

if __name__=="__main__":
    max=50
    dim=12
    c=np.genfromtxt("cost.txt")
    v = np.genfromtxt("valoare.txt")
    p=gen(c,v,max,dim)
    o=mutatie_populatie(p,c,v,max,0.1,0.7)
    grafic.legend()
    grafic.show()




