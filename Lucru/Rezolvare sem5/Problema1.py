import numpy as np
import random

def fitness(p):
    n=len(p)
    count=0
    for i in range(n):
        for j in range(i+1,n):
            if p[i]<p[j]:
                count+=1
    return count

def gen_pop(n,dim):
    pop=[]
    for _ in range(dim):
        p=list(range(n))
        random.shuffle(p)
        val=fitness(p)

        p.append(val)
        pop.append(p)
    return pop

#permutariea x cu n comp
def m_perm_interschimbare(x,n):
    poz=np.random.randint(0,n,2)
    while poz[0]==poz[1]:
        poz=np.random.randint(0,n,2)
    p1=np.min(poz)
    p2=np.max(poz)
    y=x.copy()
    y[p1]=x[p2]
    y[p2]=x[p1]
    return y

def mutatie_populatie(pop,pm):
    popm=[]
    dim=len(pop)
    n=len(pop[0])-1
    for i in range(dim):
        x=pop[i][:n].copy()
        r=np.random.uniform(0,1)
        if r<=pm:
            x=m_perm_interschimbare(x,n)
        val=fitness(x)
        x.append(val)
        popm.append(x)
    return popm
