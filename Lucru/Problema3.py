import numpy as np
import random

def fitness(x1,x2,x3,x4):
    return 1+np.sin(2*x1-x3)+(x2*x4)**(1/3)

def gen_pop(dim):
    pop=[]
    for _ in range(dim):
        x1=random.uniform(-1,1)
        x2=random.uniform(0,0.2)
        x3 = random.uniform(0, 1)
        x4 = random.uniform(0, 5)
        val=fitness(x1,x2,x3,x4)
        pop.append([x1,x2,x3,x4,val])
    return pop

#mutatie fluaj
#x - valoarea de modificat
#   a,b - limitele in care trebuie sa rezulte iesirea y, varianta a lui x modificata cu o unitate
#E:y - ca mai sus
def m_fluaj(x,a,b):
    #generare +1 sau -1
    p=np.random.randint(0,2)
    if p==0:
        s=-1
    else:
        s=1

    y=x+s
    if y>b:
        y=b
    if y<a:
        y=a
    return y

def populatie_noua(pop,pm):
    popm=[]
    dim=len(pop)
    n=4
    for i in range(dim):
        x=pop[i][:n].copy()
        for j in range(n):
            r = np.random.uniform(0, 1)
            if r<=pm:
                if j==0:
                    a,b=-1,1
                elif j==1:
                    a,b-0,0.2
                elif j==2:
                    a,b=0,1
                else:
                    a,b=0,5
            x[j]=m_fluaj(x[j],a,b)
        val=fitness(x[0],x[1],x[2],x[3])
        popm.append([x[0],x[1],x[2],x[3],val])
    return popm


if __name__ == "__main__":
    dim = 5  # dimensiunea populatiei
    pm = 0.6  # probabilitatea de mutatie

    # generam populatia initiala
    pop = gen_pop(dim)
    print("Populatia initiala:")
    for ind in pop:
        print(ind)

    # aplicam mutatia fluaj
    popm = populatie_noua(pop, pm)
    print("\nPopulatia dupa mutatie fluaj:")
    for ind in popm:
        print(ind)