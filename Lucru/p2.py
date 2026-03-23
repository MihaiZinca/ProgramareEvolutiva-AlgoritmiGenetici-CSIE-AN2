import numpy as np
import random

def fitness(x1,x2,x3,x4):
    return x1 * np.sin(10*np.pi*x1) + x4/(1+x2**2) + np.cos(x3)

def gen_pop(dim):
    pop=[]
    for _ in range(dim):
        x1=random.uniform(0,5)
        x2=random.uniform(-2,2)
        x3=random.uniform(0,np.pi)
        x4=random.uniform(1,100)
        val=fitness(x1,x2,x3,x4)
        pop.append([x1,x2,x3,x4,val])
    return pop

def m_uniforma(a,b):
    y=np.random.uniform(a,b)
    return y

def mutatie_populatie(pop,pm):
    popm=[]
    dim=len(pop)
    n=4
    for i in range(dim):
        x=pop[i][:n].copy()
        for j in range(n):
            r=np.random.uniform(0,1)
            if r<=pm:
                if j==0:
                    a,b=0,5
                elif j==1:
                    a,b=-2,2
                elif j==2:
                    a,b=0,np.pi
                else:
                    a,b=1,100

                x[j]=m_uniforma(a,b)
        val=fitness(x[0],x[1],x[2],x[3])
        popm.append([x[0],x[1],x[2],x[3],val])
    return popm

if __name__=="__main__":

    dim_pop = 20
    prob_mutatie = 0.25
    generatii = 10

    populatie = gen_pop(dim_pop)
    print(f"--- Populatie Initiala ---")
    best_init = max(populatie, key=lambda ind: ind[4])
    print(f"Cel mai bun fitness initial: {best_init[4]:.4f}")

    for g in range(generatii):
        populatie = mutatie_populatie(populatie, prob_mutatie)
        cel_mai_bun = max(populatie, key=lambda ind: ind[4])
        print(f"Generatia {g + 1} | Best Fitness: {cel_mai_bun[4]:.4f}")

    print("\n--- Rezultat Final ---")
    print(f"X: {cel_mai_bun[:4]}")
    print(f"Fitness: {cel_mai_bun[4]:.4f}")
