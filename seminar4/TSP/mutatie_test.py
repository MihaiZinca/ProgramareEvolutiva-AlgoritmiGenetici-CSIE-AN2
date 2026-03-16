import numpy as np
from FunctiiMutatieIndivizi import m_perm_inversiune
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
    grafic.plot(valori,"gs",markersize=11,label="Initial")
    return populatie, valori


#MUTATIE
 # operatia de mutatie a descendentilor obtinuti din recombinare

    # I: pcopii,vcopii - populatia copiilor si vectorul calitatilor
    #    pm - probabilitatea de mutatie
    #    c - matricea costurilor
    # E: mpo,mvo - indivizii obtinuti, vectorul calitatilor
def mutatie_populatie(pcopii,vcopii,c,pm):
    mpcopii=pcopii.copy()
    mvcopii=vcopii.copy()
    dim=mpcopii.shape[0]
    n=mpcopii.shape[1]
    for i in range(dim):
        r=np.random.uniform(0,1)
        if r<=pm:
            x=mpcopii[i]
            y=m_perm_inversiune(x,n)
            mpcopii[i]=y.copy()
            mvcopii[i]=foTSP(y,c)
    grafic.plot(mvcopii, "rs", markersize=7,label="Dupa mutatie")
    return mpcopii,mvcopii

if __name__=="__main__":
    c=np.genfromtxt("costuri.txt")
    p,v=gen(c,14)
    o,vo=mutatie_populatie(p,v,c,0.2)
    grafic.legend()
    grafic.show()