import numpy as np


# functia obiectiv pentru problema reginelor

# I: x - individul (permutarea) evaluat(a), n-dimensiunea problemei
# E: c - calitate (numarul de perechi de regine care nu se ataca
def foNR(x):
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
