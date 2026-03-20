import numpy as np
import random

def fitness(x1,x2,x3):
    return 1+np.sin(2*x1-x3)+np.cos(x2)

def gen_pop(dim):
    pop=[]
    for _ in range(dim):
        x1=random.uniform(-1,1)
        x2=random.uniform(0,1)
        x3=random.uniform(-2,1)
        val=fitness(x1,x2,x3)
        pop.append([x1,x2,x3,val])
    return pop

def m_neuniforma(x,sigma,a,b):
    p=np.random.uniform(0,sigma)
    y=x+p
    if y>b:
        y=b
    if y<a:
        y=a
    return y


def mutatie_populatie(pop,pm,sigma):
    popm=[]
    dim=len(pop)
    n=3
    for i in range(dim):
        x=pop[i][:n].copy()
        for j in range(n):
            r=np.random.uniform(0,1)
            if r<=pm:
                 if j==0:
                     a,b=-1,1
                 elif j==1:
                    a,b=0,1
                 else:
                     a,b=-2,1

            x[j]=m_neuniforma(x[j],sigma,a,b)
        val=fitness(x[0],x[1],x[2])
        popm.append([x[0],x[1],x[2],val])
    return popm

if __name__ == "__main__":
    dim = 10  # dimensiunea populației
    pm = 0.1  # probabilitatea de mutație
    sigma = 0.2  # intensitatea mutației

    # generare populație inițială
    pop = gen_pop(dim)
    print("Populația inițială:")
    for ind in pop:
        print(ind)

    # aplicare mutație
    popm = mutatie_populatie(pop, pm, sigma)
    print("\nPopulația după mutație:")
    for ind in popm:
        print(ind)

    # cel mai bun individ
    best = max(popm, key=lambda x: x[3])
    print("\nCel mai bun individ după mutație:")
    print(best)