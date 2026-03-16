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
    grafic.plot(valori,"gs",markersize=11,label="Initial")
    return populatie, valori


def mutatie_inversiune(p,c):
    n=p.size
    print(f"Individul initial {p}")
    i=np.random.randint(0,n-1)
    j=np.random.randint(i+1,n)
    print(f"Pozitiile de mutatie: {i} , {j}")
    r=p.copy()
    r[i:j+1]=[p[k] for k in range(j,i-1,-1)]
    print(f"Individul dupa mutatie {r}\n")
    return r

def mutatie_populatie(pcopii,vcopii,c,pm):
    mpcopii=pcopii.copy()
    mvcopii=vcopii.copy()
    dim=mpcopii.shape[0]
    n=mpcopii.shape[1]
    for i in range(dim):
        r=np.random.uniform(0,1)
        if r<=pm:
            x=mpcopii[i]
            y=mutatie_inversiune(x,c)
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