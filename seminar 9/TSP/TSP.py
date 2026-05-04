import numpy as np
import matplotlib.pyplot as grafic
from FunctiiCrossoverIndivizi import crossover_PMX
from FunctiiMutatieIndivizi import m_perm_inversiune
from FunctiiSelectii import elitism, SUS, SUS_rangl

#f. obiectiv
def foTSP(p,c):
    n=p.size
    cost=c[p[0]][p[-1]]+sum([c[p[i]][p[i+1]] for i in range(n-1)])
    return 100/cost


#genereaza populatia initiala
#I:
# fc - numele fisierului costurilor
# dim - numarul de indivizi din populatie
#E: pop,val - populatia initiala si vectorul valorilor
def gen(c,dim):
    #n=dimensiunea problemei
    n = len(c)
    pop=np.zeros((dim,n),dtype=int)
    val=np.zeros(dim,dtype=float)
    for i in range(dim):
        #genereaza candidatul permutare cu n elemente
        pop[i] = np.random.permutation(n)
        # evalueaza candidat
        val[i] = foTSP(pop[i,:n],c)
    return pop, val



#crossover pe populatia de parinti pop, de dimensiune dimxn
# I: pop, valori,dim,n -  ca in functia de generare
#     c - datele problemei
#     pc- probabilitatea de crossover
#E: po,val - populatia copiilor, insotita de calitati
# este implementata recombinarea asexuata
def crossover(pop,valori,c,pc):
    # initializeaza populatia de copii, po, cu matricea cu elementele 0
    dim,n=pop.shape
    po=np.zeros((dim,n),dtype=int)
    # initializeaza valorile populatiei de copii, val, cu matricea cu elementele 0
    val=np.zeros(dim,dtype=float)
    #populatia este parcursa astfel incat sunt selectati aleator cate 2 indivizi - matricea este accesata dupa o permutare a multimii de linii 0,2,...,dim-1
    poz=np.random.permutation(dim) # - rang liniar
    #sau populatia este parcursa astfel incat sunt selectati 2 indivizi consecutivi
    #poz=range(dim) #- pentru pastrarea ordinii, FPS
    for i in range(0,dim-1,2):
        #selecteaza parintii
        x = pop[poz[i]]
        y = pop[poz[i+1]]
        r = np.random.uniform(0,1)
        if r<=pc:
            # crossover x cu y - PMX - potrivit pentru probleme cu dependenta de adiacenta
            c1,c2 = crossover_PMX(x,y,n)
            v1=foTSP(c1,c)
            v2=foTSP(c2,c)
        else:
            # recombinare asexuata
            c1 = x.copy()
            c2 = y.copy()
            v1=valori[poz[i]]
            v2=valori[poz[i+1]]
        #copiaza rezultatul in populatia urmasilor
        po[i] = np.copy(c1)
        po[i+1] = np.copy(c2)
        val[i]=v1
        val[i+1]=v2
    return po, val

#MUTATIE
 # operatia de mutatie a descendentilor obtinuti din recombinare
    # I: po,vo - populatia copiilor insoltita de vectorul calitatilor
    #   dim,n - dimensiunile
    #    pm - probabilitatea de mutatie
    #    c - matricea costurilor
    # E: mpo,mvo - indivizii obtinuti, insotiti de calitati
def mutatie(po,vo,c,pm):
    mpo=po.copy()
    mvo=vo.copy()
    dim, n = po.shape
    for i in range(dim):
        r=np.random.uniform(0,1)
        if r<=pm:
            x=mpo[i]
            y=m_perm_inversiune(x,n)
            mpo[i]=y
            mvo[i]=foTSP(y,c)
    return mpo,mvo


def arata(sol,v):
    # vizualizare rezultate TSP
    # I: x - permutarea care defineste asezarea
    # E: -

    n=len(sol)
    t=len(v)
    cost=min(v)
    print("Cea mai mică distanță calculată: ",cost)
    print("Un drum cu costul ",cost," este: ",sol)
    x=[i for i in range(t)]
    y=[v[i] for i in range(t)]
    grafic.plot(x,y,'ro-')
    grafic.ylabel("Costul")
    grafic.xlabel("Generația")
    grafic.title("Evoluția calității celui mai bun individ din fiecare generație")
    grafic.show()



##ALGORITMUL GENETIC PENTRU REZOLVAREA TSP
#I: fc - fisierul cu matricea costurilor(distantelor)
#   dim - dimensiunea unei populatii
#   NMAX - numarul maxim de simulari ale unei evolutii
#   pc - probabilitatea de crossover
#   pm - probabilitatea de mutatie
#
#E: sol - solutia calculata de GA
#   val - 100/maximul functiei fitness - cost_minim

def GA(fc,dim,NMAX,pc,pm):
    # citeste datele din fisierul nxn al costurilor
    c = np.genfromtxt(fc)
    #generarea populatiei la momentul initial
    pop,qual=gen(c,dim)
    n=len(c)
    #initializari pentru GA
    it=0
    gata=False
    #in istoric_v pastram cel mai bun cost din populatia curenta, la fiecare moment al evolutiei
    istoric_v=[100/np.max(qual)]
    # evolutia - cat timp
    #                - nu am depasit NMAX  si
    #                - populatia are macar 2 indivizi cu calitati diferite  si
    #                - in ultimele NMAX/3 iteratii s-a schimbat macar o data calitatea cea mai buna
    nrm=1
    while it<NMAX and not gata:
        # SELECTIA PARINTILOR
        #1.
        spop, sval = SUS(pop, qual, dim, n)
        #2.
        #spop,sval=SUS_rangl(pop,qual,dim,n,1.5)
        # RECOMBINARE
        copii,val_copii=crossover(spop,sval,c,pc)
        # MUTATIE
        copiim,val_copiim=mutatie(copii,val_copii,c,pm)
        # SELECTIA GENERATIEI URMATOARE
        newpop,newval=elitism(pop,qual,copiim,val_copiim,dim)
        minim=np.min(newval)
        maxim=np.max(newval)
        if maxim==100/istoric_v[it]:
            nrm=nrm+1
        else:
            nrm=0
        if maxim==minim or nrm==int(NMAX/3):
            gata=True
        else:
            it=it+1
        istoric_v.append(100/np.max(newval))
        pop=newpop.copy()
        qual=newval.copy()
    i_sol = np.argmax(qual)
    sol=pop[i_sol]
    val=maxim
    arata(sol,istoric_v)
    return sol,100/val

if __name__=="__main__":
    sol,val=GA("distante3.txt",200,300,0.8,0.2) #- costul minim 29, se obtin valori apropiate
    sol,val=GA("costuri.txt",200,300,0.8,0.2) #- costul minim 15, se obtin valori apropiate