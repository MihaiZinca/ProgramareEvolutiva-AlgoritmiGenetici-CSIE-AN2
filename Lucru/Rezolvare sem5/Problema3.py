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
        random.shuffle(p) #amesteca aleator
        val=fitness(p)

        p.append(val)
        pop.append(p)
    return pop


def m_perm_amestec(p):
    y=p.copy()
    random.shuffle(y) #amesteca toate elemet permutarii
    return y

def mutatie_populatie(pop,pm):
    popm=[]
    dim=len(pop)
    n=len(pop[0])-1 #lung perm fara fitness

    for i in range(dim):
        x=pop[i][:n].copy()
        r=np.random.uniform(0,1)
        if r<=pm:
            x=m_perm_amestec(x)
        val=fitness(x)
        x.append(val)
        popm.append(x)
    return popm

if __name__ == "__main__":
    n = 5
    dim = 6
    pm = 0.5
    pop = gen_pop(n, dim)
    print("Populatia initiala:")
    for ind in pop:
        print(ind)
    popm = mutatie_populatie(pop, pm)
    print("\nPopulatia dupa mutatie:")
    for ind in popm:
        print(ind)
