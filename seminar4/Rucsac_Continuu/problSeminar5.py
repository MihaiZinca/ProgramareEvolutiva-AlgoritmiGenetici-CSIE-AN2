#f:[-1,1]x[0,0.2]x[0,1]x[0,5] -> R
#f(x1,x,2,x3,x4)=1+sin(2x1-x3) +(x2*x4)^1/3
#x=(x1,x2,x3,x4)T
#x ap [-1,1]x[0,0.2]x[0,1]x[0,5]

#a)Generare pop initiala
#b)Mutatie de tip neuniform =>generatie noua, prag t=0.6

import numpy as np
import random
import matplotlib.pyplot as grafic
import copy

#definitia functiei fitness
#fara a adauga restictiile de validitate(individ)
def fitness(x):
    return 1 +np.sin(2*x[0]-x[2])+(x[1]*x[3])**(1/3)

#generare populatia initiliaa
def gen_pop(dim,a,b):
    pop=np.zeros([dim,5])
    for i in range(dim):
        pop[i,:4]=np.random.uniform(a,b,4)
        pop[i,4]=fitness(pop[i,:4])
    return pop

#mutatie neuniforma

def m_neuniforma(x,a,b,sigma):
    perturbare=random.uniform(0,sigma)
    y=x+ perturbare
    if y<a:
        y=a
    elif y>b:
        y=b
    return y

#generam noua populatie
def populatie_noua(pop,dim,a,b,sigma,pm):
    mpop=pop.copy();

    for i in range(dim):
        for j in range(4):
            r=np.random.uniform(0,1)
            if r<=pm:
                mpop[i,j]=m_neuniforma(mpop[i,j],a,b,sigma)
        mpop[i,4]=fitness(mpop[i,:4])

    return mpop

if __name__=="__main__":
    dim = 10
    a = 0
    b = 1
    sigma = 0.1
    pm = 0.6

    pop = gen_pop(dim, a, b)
    print("Pop initial:\n", pop)

    mpop = populatie_noua(pop, dim, a, b, sigma, pm)
    print("\nPop dupa mutatie:\n", mpop)
