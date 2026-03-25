import numpy as np
import matplotlib.pyplot as grafic

#f. obiectiv
def foNR(x):
    # functia obiectiv pentru problema reginelor

    # I: x - individul (permutarea) evaluat(a), n-dimensiunea problemei
    # E: c - calitate (numarul de perechi de regine care nu se ataca

    n=x.size
    c=len([(i,j) for i in range(n-1) for j in range(i+1,n) if abs(i-j)!=abs(x[i]-x[j])])

    return c

#genereaza populatia initiala
#I:
# n - dimensiunea prolemei
# dim - numarul de indivizi din populatie
#E: pop - populatia initiala
def gen(n,dim):
    #defineste o variabila ndarray cu toate elementelo nule
    pop=np.zeros((dim,n+1),dtype="int")
    for i in range(dim):
        #genereaza candidatul permutare cu n elemente
        pop[i,:n]=np.random.permutation(n)
        pop[i,n]=foNR(pop[i,:n])
    return pop



#crossover pe populatia de parinti pop, de dimensiune dimx(n+1)
# I: pop,dim,n - ca mai sus
#     pc- probabilitatea de crossover
#E: po - populatia copiilor
# este implementata recombinarea asexuata
def crossover_populatie(pop,pc):
    #initializeaza populatia de copii, po, cu populatia parintilor
    dim=pop.shape[0]
    m=pop.shape[1]
    n=m-1
    po=pop.copy()
    #populatia este parcursa astfel incat sunt selectati indivizii 0,1 apoi 2,3 s.a.m.d
    for i in range(0,dim-1,2):
        #selecteaza parintii
        x = pop[i,:-1]
        y = pop[i+1,:-1]
        r = np.random.uniform(0,1)
        if r<=pc:
            # crossover x cu y - OCX sau CX - potrivit pentru NRegine
            c1,c2 = crossover_OCX(x,y)
            val1=foNR(c1)
            val2= foNR(c2)
            po[i][:n]=c1.copy()
            po[i][n]=val1
            po[i+1][:n]=c2.copy()
            po[i+1][n]=val2
    figureaza(pop[:,n],po[:,n],dim)
    return po

def crossover_OCX(x,y):
    n=x.size
    i=np.random.randint(0,n-1)
    j=np.random.randint(i+1,n)
    copil1=OCX(x,y,i,j)
    copil2=OCX(y,x,i,j)
    return copil1, copil2

def OCX(x,y,p1,p2):
    n=x.size
    # construim cele 3 secventa ale rezultatului
    s2=[x[i] for i in range(p1,p2+1)]
    z1=[y[i] for i in range(p2,n) if y[i] not in s2]
    z2=[y[i] for i in range(0,p2) if y[i] not in s2]
    #z trebuie adaugat la s2 - primele la sfarsit cat incap, restul la inceput
    z=np.append(z1,z2)
    s3=[z[i] for i in range(n-p2-1)]
    s1=[z[i] for i in range(n-p2-1,z.size)]
    rezultat=np.append(s1,s2)
    rezultat=np.append(rezultat,s3)
    return rezultat



def figureaza(valori,val,dim):
    grafic.plot(valori, "go", markersize=12,label='Parinti')
    grafic.plot(val, "ro", markersize=9,label='Copii')
    grafic.legend()
    grafic.xlabel('Indivizi')
    grafic.ylabel('Fitness')
    grafic.show()


if __name__=="__main__":
    p=gen(10,8)
    o=crossover_populatie(p,0.8)



