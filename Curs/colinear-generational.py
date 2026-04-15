import numpy as np
import random
import matplotlib.pyplot as grafic
from CrossoverFunctions import crossover_uniform
from Mutation_operators import m_ra
from Selection import SUS, elitism



def triangle_area(A,B,C):
    return abs(A[0]*(B[1]-C[1]) + B[0]*(C[1]-A[1]) + C[0]*(A[1]-B[1])) / 2

def fitness(x,S):
    A=S[x[0]]
    B=S[x[1]]
    C=S[x[2]]
    area=triangle_area(A,B,C)
    return 1/(1+area)


def generate_p(nf,dim):
    S=np.genfromtxt(nf)
    n=len(S)
    pop=np.zeros([dim,3],dtype=int)
    val=np.zeros(dim)
    for i in range(dim):
        pop[i]=random.sample(range(0,n),3)
        val[i]=fitness(pop[i],S)
    return pop,val,S


def feasible(x):
    ok=True
    if x[0]==x[1] or x[0]==x[2] or x[1]==x[2]:
        ok=False
    return ok


def crossover_pop(p_pop, p_val,dim, S, pc):
    o_pop = p_pop.copy()
    o_val=p_val.copy()
    for i in range(0, dim - 1, 2):
        x = p_pop[i]
        y = p_pop[i + 1]
        r = np.random.uniform(0, 1)
        if r <= pc:
            c1, c2 = crossover_uniform(x, y, 3)
            if feasible(c1):
                o_pop[i]=c1.copy()
                o_val[i]=fitness(c1,S)
            if feasible(c2):
                o_pop[i+1]=c2.copy()
                o_val[i+1]=fitness(c2,S)
    return o_pop,o_val


def mutation_pop(o_pop, o_val,dim, S, pm):
    mo_pop = o_pop.copy()
    mo_val=o_val.copy()
    n=len(S)
    for i in range(dim):
        x = o_pop[i]
        for j in range(3):
            r = np.random.uniform(0, 1)
            if r <= pm:
                x[j]= m_ra(0,n)
        if feasible(x):
            mo_pop[i]=x.copy()
            mo_val[i]=fitness(x,S)
    return mo_pop,mo_val


def disp_sol(sol, P):
    nor=grafic.figure()
    n=len(P)
    x=[P[i,0] for i in range(n)]
    y=[P[i,1] for i in range(n)]
    grafic.plot(x,y,color='k', linestyle='none', marker='.',
                markerfacecolor='blue', markersize=4)
    x = [P[sol[i], 0] for i in range(3)]
    y = [P[sol[i], 1] for i in range(3)]
    grafic.plot(x,y,"ro-")
    grafic.show()


def GA_solver(nf,dim,NMAX,pc,pm):
    pop, val, S=generate_p(nf,dim)
    t=0
    max_val=max(val)
    pos=np.argmax(val)
    sol=pop[pos]

    stop=False

    if max_val>=0.99999:
        stop=True

    history=[max_val]

    while t<NMAX and not stop and max_val<0.99999:
        p_pop,p_val=SUS(pop, val, dim, 3)
        o_pop,o_val=crossover_pop(p_pop,p_val,dim,S,pc)
        mo_pop,mo_val=mutation_pop(o_pop,o_val,dim,S,pm)
        new_pop,new_val=elitism(pop,val,mo_pop,mo_val,dim)

        max_val=max(new_val)
        pos=np.argmax(new_val)
        sol=new_pop[pos]

        min_val=min(new_val)

        if min_val==max_val:
            stop=True

        history.append(max_val)
        pop=new_pop.copy()
        val=new_val.copy()
        t+=1

    fig = grafic.figure()
    x = [i for i in range(t)]
    y = [history[i] for i in range(t)]
    grafic.plot(x, y, 'ro-')
    grafic.ylabel("Fitness")
    grafic.xlabel("Generation")
    grafic.title("Quality evolution")
    grafic.show()

    if max_val<0.99999:
        print('No solution')
    else:
        P=[S[sol[0]],S[sol[1]],S[sol[2]]]
        print('3 colinear points are: ',P[0],P[1],P[2])
        print('Fitness value:',max_val)

    disp_sol(sol, S)

    return sol,max_val,(1-max_val)/max_val


if __name__=="__main__":
    sol,fit,er=GA_solver('points.txt',300,250,0.8,0.2)