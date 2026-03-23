import numpy as np
import random

def fitness(x1,x2,x3,x4):
    return np.log(1+x2**2) +np.exp(-(x1-x3)**2)+ np.sqrt(x4)

def gen_pop(dim):
    pop=[]
    for _ in range(dim):
        x1=random.uniform(-2,2)
        x2=random.uniform(0,4)
        x3=random.uniform(-1,1)
        x4=random.uniform(1,10)
        val=fitness(x1,x2,x3,x4)
        pop.append([x1,x2,x3,x4,val])
    return pop

def m_neuniform(x,sigma,a,b):
    p=np.random.normal(0,sigma)
    y=x+p
    if y>b:
        y=b
    if y<a:
        y=a
    return y

def mutatie_populatie(pop,pm,sigma):
    popm=[]
    dim=len(pop)
    n=4
    for i in range(dim):
        x=pop[i][:n].copy()
        for j in range(n):
            r=np.random.uniform(0,1)
            if r<=pm:
                if j==0:
                    a,b=-2,2
                elif j==1:
                    a,b=0,4
                elif j==2:
                    a,b=-1,1
                else:
                    a,b=1,10

                x[j]=m_neuniform(x[j],sigma,a,b)
        val=fitness(x[0],x[1],x[2],x[3])
        popm.append([x[0],x[1],x[2],x[3],val])
    return popm

if __name__=="__main__":
    dimensiune_populatie = 10
    probabilitate_mutatie = 0.2
    sigma_mutatie = 0.5
    numar_generatii = 5

    populatie = gen_pop(dimensiune_populatie)
    print("Populatia inițiala:")
    for i in range(3):
        print(populatie[i])

    for gen in range(numar_generatii):
        populatie = mutatie_populatie(populatie, probabilitate_mutatie, sigma_mutatie)

        # Gasire cel mai bun individ din generatia curenta
        cel_mai_bun = max(populatie, key=lambda ind: ind[4])
        print(f"\nGeneratia {gen + 1}:")
        print(f"Cel mai bun fitness: {cel_mai_bun[4]:.4f}")


    print("\nCel mai bun individ final:")
    print(f"X: {cel_mai_bun[:4]}")
    print(f"Fitness: {cel_mai_bun[4]:.4f}")