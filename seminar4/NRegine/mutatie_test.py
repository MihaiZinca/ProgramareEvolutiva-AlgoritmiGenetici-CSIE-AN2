import numpy as np
from FunctiiMutatieIndivizi import m_perm_inserare
import matplotlib.pyplot as grafic


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
    pop=np.zeros((dim,n+1),dtype=int)
    for i in range(dim):
        #genereaza candidatul permutare cu n elemente
        pop[i,:n]=np.random.permutation(n)
        pop[i,n]=foNR(pop[i,:n])
    grafic.plot(pop[:,n], "go", markersize=11, label="Initial")
    return pop



#mutatie asupra populatiei de copii
# I:pop,dim,n - populatia de dimensiuni dimx(n+1)
#   pm - probabilitatea de mutatie
#E: - mpop - populatia mutata
def mutatie_populatie(pop,dim,n,pm):
    mpop=pop.copy()
    for i in range(dim):
        #genereaza aleator daca se face mutatie
        r=np.random.uniform(0,1)
        if r<=pm:
            #mutatie in individul i - prin inserare
            x=m_perm_inserare(mpop[i,:n],n)
            mpop[i,:n]=x.copy()
            mpop[i,n]=foNR(x)
    grafic.plot(mpop[:,n], "ro", markersize=7,label="Dupa mutatie")
    return mpop

if __name__=="__main__":
    p=gen(12,14)
    o=mutatie_populatie(p,14,12,0.2)
    grafic.legend()
    grafic.show()


