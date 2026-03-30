import numpy as np
import random

def fitness(x):
    return np.sum(x)

def gen_pop(dim):
    pop=[]
    for _ in range(dim):
        individ=random.choices([0,1],k=7)
        individ.append(fitness(individ))
        pop.append(individ)
    return pop

def recombinare(x,y):
    i,j=sorted(random.sample(range(1,6),2))
    copil1=x[:i]+ y[i:j] + x[j:]
    copil2=y[:i]+ x[i:j] + y[j:]
    return copil1,copil2

def crossover_2pct(parinti,pc):

    copii=[]
    dim=len(parinti)

    for i in range(0,dim-1,2):

        r=random.uniform(0,1)
        if r<pc:
            p1=parinti[i][:-1]
            p2=parinti[i+1][:-1]

            copil1,copil2=recombinare(p1,p2)

            copil1.append(fitness(copil1))
            copil2.append(fitness(copil2))

            copii[i]=copil1.copy()
            copii[i+1]=copil2.copy()
    return copii












