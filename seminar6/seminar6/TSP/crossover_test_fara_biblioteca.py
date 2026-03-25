import numpy as np
import matplotlib.pyplot as grafic


#f. obiectiv
def foTSP(p,c):
    n=p.size
    cost=c[p[0]][p[-1]]+sum([c[p[i]][p[i+1]] for i in range(n-1)])
    return 100/cost


def gen(c,dim):
    n=c.shape[0]
    populatie=np.zeros([dim,n],dtype="int")
    valori=np.zeros(dim)
    for i in range(dim):
       populatie[i]=np.random.permutation(n)
       valori[i] = foTSP(populatie[i],c)
    return populatie, valori


#crossover pe populatia de parinti pop, de dimensiune dimxn
# I:   pop,valori, ca in functia de generare
#     c - datele problemei
#     pc- probabilitatea de crossover
#E: po,val - populatia copiilor, insotita de calitati
# este implementata recombinarea asexuata
def crossover_populatie(pop,valori,c,pc):
    # initializeaza populatia de copii, po, cu matricea cu elementele 0
    dim=pop.shape[0]
    n=pop.shape[1]
    po=np.zeros((dim,n),dtype="int")
    # initializeaza valorile populatiei de copii, val, cu matricea cu elementele 0
    val=np.zeros(dim,dtype="float")
    #populatia este parcursa astfel incat sunt selectati aleator cate 2 indivizi - matricea este accesata dupa o permutare a multimii de linii 0,2,...,dim-1
    #poz=np.random.permutation(dim)
    #sau populatia este parcursa astfel incat sunt selectati 2 indivizi consecutivi
    poz=range(dim) #- pentru pastrarea ordinii
    for i in range(0,dim-1,2):
        #selecteaza parintii
        x = pop[poz[i]]
        y = pop[poz[i+1]]
        r = np.random.uniform(0,1)
        if r<=pc:
            # crossover x cu y - PMX - potrivit pentru probleme cu dependenta de adiacenta
            c1,c2 = crossover_PMX(x,y)
            v1=foTSP(c1,c)
            v2=foTSP(c2,c)
        else:
            # recombinare asexuata
            c1 = x.copy()
            c2 = y.copy()
            v1=valori[poz[i]]
            v2=valori[poz[i+1]]
        #copiaza rezultatul in populatia urmasilor
        po[i] = c1.copy()
        po[i+1] = c2.copy()
        val[i]=v1
        val[i+1]=v2
    valori=[valori[poz[i]] for i in range(dim)]
    figureaza(valori,val,dim)
    return po, val

def crossover_PMX(x,y):
    n=x.size
    p1=np.random.randint(0,n-1)
    p2=np.random.randint(p1+1,n)
    copil1=PMX(x,y,p1,p2)
    copil2=PMX(y,x,p1,p2)
    return copil1, copil2

def PMX(x,y,p1,p2):
    n=x.size
    copil=-np.ones(n,dtype="int")
    copil[p1:p2+1]=x[p1:p2+1]
    #pozitiile alelelor din secventa de crossover din y care nu apartin lui copil
    poz_alele_neplasate=[k for k in range(p1,p2+1) if not y[k] in copil]
    for p in poz_alele_neplasate:
        a=y[p]
        while copil[p]>-1:
            p=np.where(y==copil[p])[0][0]
        copil[p]=a
    alele_neplasate=[y[k] for k in range(n) if not y[k] in copil]
    pozitii_libere=[k for k in range(n) if copil[k]==-1]
    copil[pozitii_libere]=alele_neplasate.copy()
    return copil



def figureaza(valori,val,dim):
    x = range(dim)
    grafic.plot(x, valori, "go", markersize=12,label="Calitate parinti")
    grafic.plot(x, val, "ro", markersize=10,label="Calitate copii")
    grafic.legend()
    grafic.xlabel("Indicii indivizilor")
    grafic.ylabel("Calitatile indivizilor")
    grafic.show()

if __name__=="__main__":
    c=np.genfromtxt("costuri.txt")
    p,v=gen(c,12)
    o,vo=crossover_populatie(p,v,c,0.8)

