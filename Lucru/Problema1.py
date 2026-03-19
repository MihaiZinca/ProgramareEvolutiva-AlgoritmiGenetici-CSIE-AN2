from copy import deepcopy

import numpy as np
import random

import pylab as p

def fitness(p):
    n=len(p)
    count=0
    for i in range(n):
        for j in range(i+1,n):
            if p[i]==j and p[j]==i:
                count+=1
    return count

def gen_pop(n,dim):
    pop=[]
    for _ in range(dim):
        p=list(range(n))
        random.shuffle(p) #amesteca lista p in mod aleator, modifica lista(nu ret alta)
        val=fitness(p)

        p.append(val) #adagua fitness la final
        pop.append(p) #aduga perm+fitness
    return pop


# mutatia prin inserare a permutarii x cu n componete
# I:x,n
# E:y - permutarea rezultat
def m_perm_inserare(x,n):
    poz=np.random.randint(0,n,2)
    while poz[0]==poz[1]:
        poz=np.random.randint(0,n,2)
    p1=np.min(poz)
    p2=np.max(poz)

    y=x.copy()
    y[p1+1]=x[p2]
    if p1<n-2:
        y[p1+2:n]=np.array([x[i] for i in range(p1+1,n) if i!=p2])
    return y

def mutatie_populatie(pop,pm):
    popm=pop.copy()
    dim=len(pop)
    n=len(pop[0])-1 #lung permutarii(Fara fitness)

    for i in range(dim):
        x=pop[i][:n].copy()
        r=np.random.uniform(0,1)
        if r<=pm:
            x=m_perm_inserare(x,n)
        val=fitness(x)
        x.append(val)
        popm.append(x)
    return popm

if __name__=="__main__":
    n = 5
    dim = 6
    pm = 0.6

    pop = gen_pop(n, dim)
    print("Populația inițială:")
    for ind in pop:
        print(ind)

    popm = mutatie_populatie(pop, pm)
    print("\nPopulația după mutație:")
    for ind in popm:
        print(ind)