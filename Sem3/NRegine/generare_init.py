# AICI POPULATIA ESTE O MATRICE IN CARE FIECARE LINIE ESTE O PERMUTARE COMPLETATA DE CALITATEA ACESTEIA

import numpy as np
import matplotlib.pyplot as grafic


#f. obiectiv
def foNR(x):
    # functia obiectiv pentru problema reginelor

    # I: x - individul (permutarea) evaluat(a), n-dimensiunea problemei
    # E: c - calitate (numarul de perechi de regine care nu se ataca

    n=x.size
    c = n*(n-1)/2  # pentru numar intreg -> //
    for i in range(n-1):
        for j in range(i+1,n):
            if abs(i-j)==abs(x[i]-x[j]):
                c-=1
    #echivalent cu
    #c=len([(i,j) for i in range(n-1) for j in range(i+1,n) if abs(i-j)!=abs(x[i]-x[j])])

    return c


#genereaza populatia initiala
#I:
# n - dimensiunea prolemei
# dim - numarul de indivizi din populatie
#E: pop - populatia initiala
def gen(n,dim):
    #defineste o variabila ndarray cu toate elementelo nule
    pop=np.zeros((dim,n+1),dtype=int)
    for i in range(dim):
        #genereaza candidatul permutare cu n elemente
        pop[i,:n]=np.random.permutation(n)
        pop[i,n]=foNR(pop[i,:n])
    reprezinta_pop(pop, dim, n)
    return pop


#figurarea populatiei prin punctele (indice individ, calitate) - pentru a vedea variabilitatea in populatie
def reprezinta_pop(pop,dim,n):
    y=[pop[i][n] for i in range(dim)]
    grafic.plot(range(dim),y,"gs",markersize=11)
    grafic.title("Calitatile indivizilor generați în populația inițială")
    grafic.xlabel("Index individ")
    grafic.ylabel("Calitate individ")
    grafic.show()


if __name__=="__main__":
    p = gen(8, 20)
    print(p)


