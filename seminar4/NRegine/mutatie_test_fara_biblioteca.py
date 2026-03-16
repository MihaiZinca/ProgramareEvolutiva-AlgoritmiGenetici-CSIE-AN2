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
    grafic.plot(pop[:,n], "go", markersize=11, label="Initial")
    return pop


# mutatia prin inserare in permutarea p
def mutatie_inserare(p):
    n=p.size
    print(f"\n\n\nmutatie in {p} cu calitatea {foNR(p)}")
    p1=np.random.randint(0,n-1)
    p2=np.random.randint(p1+1,n)
    print(f"\npozitiile sunt {p1+1} si {p2+1}")
    rez=p.copy()
    if p1+1<p2:
        element_inserat=p[p2]
        x=np.delete(p,p2)
        rez=np.insert(x,p1+1,element_inserat)
    print(f"\nrezulta individul {rez} cu calitatea {foNR(rez)}")
    return rez



#mutatie asupra populatiei de copii
# I:pop,dim,n - populatia de dimensiuni dimx(n+1)
#   pm - probabilitatea de mutatie
#E: - mpop - populatia mutata
def mutatie_populatie(pop,dim,n,pm):
    mpop=pop.copy()
    for i in range(dim):
        #genereaza aleator daca se face mutatie
        r=np.random.uniform(0,1)
        if r<=pm:
            #mutatie in individul i - prin inserare
            x=mutatie_inserare(mpop[i,:n])
            mpop[i,:n]=x.copy()
            mpop[i,n]=foNR(x)
    grafic.plot(mpop[:,n], "ro", markersize=7,label="Dupa mutatie")
    return mpop

if __name__=="__main__":
    p=gen(12,18)
    o=mutatie_populatie(p,18,12,0.2)
    grafic.legend()
    grafic.show()


