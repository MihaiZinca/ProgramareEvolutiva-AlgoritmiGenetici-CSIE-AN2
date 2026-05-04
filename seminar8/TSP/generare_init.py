import numpy as np

#f. obiectiv
def foTSP(p,c):
    n=p.size
    cost=c[p[0]][p[-1]]+sum([c[p[i]][p[i+1]] for i in range(n-1)])
    return 100/cost

#genereaza populatia initiala
#I:
# c - matricea costurilor
# dim - numarul de indivizi din populatie
#E: populatia initiala si vectorul valorilor


def gen(c,dim):
    n=c.shape[0]
    populatie=np.zeros([dim,n],dtype="int")
    valori=np.zeros(dim)
    for i in range(dim):
       populatie[i]=np.random.permutation(n)
       valori[i] = foTSP(populatie[i],c)
    return populatie, valori




