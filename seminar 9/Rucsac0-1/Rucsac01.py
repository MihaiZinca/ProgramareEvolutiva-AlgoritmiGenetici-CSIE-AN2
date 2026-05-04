import numpy as np
import random
import copy
import matplotlib.pyplot as grafic
from FunctiiCrossoverIndivizi import crossover_uniform, crossover_unipunct
from FunctiiMutatieIndivizi import m_binar
from FunctiiSelectii import elitism, ruleta


#verifica fezabilitatea alegerii x si calculeaza si f. obiectiv
def ok(x,c,v,max):
    val=np.dot(x,v)
    cost=np.dot(x,c)
    return cost<=max, val


#genereaza populatia initiala
#I:
# c,v - vectorii cost, valoare
# max - capacitatea maxima
# dim - numarul de indivizi din populatie
# E:
#pop - populatia insotita de calitati

def gen(c,v,max,dim):
    #n=dimensiunea problemei
    n=v.size
    #lucreaza cu populatia ca lista de dim elemente - liste cu cate n+1 indivizi
    pop=[]
    for i in range(dim):
        gata=False
        while gata == False:
            #genereaza candidatul x cu elemente 0,1
            #x=[random.choice([0,1]) for _ in range(n)]
            x=random.choices([0,1],k=n)
            gata,val=ok(x,c,v,max)
        #am gasit o solutie candidat fezabila, in data de tip lista x
        # adauga valoarea
        x.append(val)
        #adauga la populatie noul individ cu valoarea f. obiectiv - adauga inca o lista cu n+1 elemente ca element al listei pop
        pop.append(x)
    return pop


#crossover pe populatia de parinti pop
# I: pop - populatia parintilor insotita de calitati
#     c, v, max - datele problemei
#     pc- probabilitatea de crossover
#E: po - populatia copiilor insotita de calitatile copiilor
# este implementata recombinarea asexuata
def crossover_populatie(pop,c,v,max,pc):
    dim=len(pop)
    n=c.size
    po=copy.deepcopy(pop)
    #populatia este parcursa astfel incat sunt selectati indivizii 0,1 apoi 2,3 s.a.m.d
    for i in range(0,dim-1,2):
        #selecteaza parintii
        x = copy.deepcopy(pop[i][:-1])
        y = copy.deepcopy(pop[i+1][:-1])
        r = np.random.uniform(0,1)
        if r<=pc:
            # crossover x cu y - uniform: mai potrivit aici
            c1,c2=crossover_uniform(x ,y ,n)
            fez, val = ok(c1, c, v, max)
            if fez:
                po[i][:-1]=copy.deepcopy(c1)
                po[i][-1]=val
            fez, val = ok(c2, c, v, max)
            if fez:
               po[i+1][:-1]=copy.deepcopy(c2)
               po[i+1][-1]=val
    return po


#mutatie asupra populatiei de copii
# I:pop - populatiea de copii insotita de calitati
#   pm - probabilitatea de mutatie
#E: - mpop - populatia mutata, calitatile in aceasta
def mutatie_populatie(pop,c,v,max,pm):
    #copiem populatia in rezultat
    dim = len(pop)
    n = c.size
    mpop=copy.deepcopy(pop)
    for i in range(dim):
        #copiem in x individul i din populatia intrare
        x=copy.deepcopy(pop[i][:-1])
        for j in range(n):
            #genereaza aleator daca se face mutatie in individul i gena j
            r=np.random.uniform(0,1)
            if r<=pm:
                #mutatie
                x[j]=m_binar(x[j])
        #individul rezultat sufera posibil mai multe mutatii
        #daca este fezabil, este pastrat
        fez, val = ok(x, c, v, max)
        if fez:
            mpop[i][:-1]=copy.deepcopy(x)
            mpop[i][-1]=val
    return mpop


def arata(sol,v):
    # vizualizare rezultate Rucsac 0-1
    n=len(sol)
    t=len(v)
    val=max(v)
    print("Cea mai buna valoare calculată: ",val)
    print("Alegerea corespunzatoare este: ",sol)
    fig=grafic.figure()
    x=[i for i in range(t)]
    y=[v[i] for i in range(t)]
    grafic.plot(x,y,'ro-')
    grafic.ylabel("Valoarea")
    grafic.xlabel("Generația")
    grafic.title("Evoluția calității celui mai bun individ din fiecare generație")
    grafic.show()



##ALGORITMUL GENETIC PENTRU REZOLVAREA PROBLEMEI RUCSACULUI 0-1
#I: fc,fv - fisierele cu costuri/valori
#   dim - dimensiunea unei populatii
#   NMAX - numarul maxim de simulari ale unei evolutii
#   pc - probabilitatea de crossover
#   pm - probabilitatea de mutatie
#
#E: sol - solutia calculata de GA
#   val - maximul functiei fitness

def GA(fc,fv,cmax,dim,NMAX,pc,pm):
    #generarea populatiei la momentul initial
    c=np.genfromtxt(fc)
    v=np.genfromtxt(fv)
    pop=gen(c,v, cmax, dim)
    n = c.size
    #initializari pentru GA
    it=0
    gata=False
    nrm=1
    #in istoric_v pastram cel mai bun cost din populatia curenta, la fiecare moment al evolutiei
    istoric_v=[max([pop[i][-1] for i in range(dim)])]
    # evolutia - cat timp
    #                - nu am depasit NMAX  si
    #                - populatia are macar 2 indivizi cu calitati diferite  si
    #                - in ultimele NMAX/3 iteratii s-a schimbat macar o data calitatea cea mai buna
    while it<NMAX and not gata:
        #SELECTIA PARINTILOR
        # functia ruleta este implementata pe ndarray
        indivizi=np.array([pop[i][:-1] for i in range(dim)])
        cal=np.array([pop[i][-1] for i in range(dim)])
        spop, sval = ruleta(indivizi, cal, dim, n)
        spop=spop.tolist()
        # RECOMBINAREA
        for i in range(dim):
            spop[i].append(sval[i])
        pop_o= crossover_populatie(spop,c, v, cmax, pc)
        # MUTATIA
        pop_mo = mutatie_populatie(pop_o,c,v,cmax,pm)
        # SELECTIA GENERATIEI URMATOARE
        # functia elitism este implementata pe ndarray
        indivizi=np.array([pop[i][:-1] for i in range(dim)])
        cal=np.array([pop[i][-1] for i in range(dim)])
        indivizi_noi = np.array([pop_mo[i][:-1] for i in range(dim)])
        cal_noi = np.array([pop_mo[i][-1] for i in range(dim)])
        newpop, newval = elitism(indivizi, cal, indivizi_noi, cal_noi, dim)
        minim=min(newval)
        maxim=max(newval)
        if maxim==istoric_v[it]:
            nrm=nrm+1
        else:
            nrm=1
        if maxim==minim or nrm==int(NMAX/3):
            gata=True
        else:
            it=it+1
        istoric_v.append(max(newval))
        pop =copy.deepcopy(newpop.tolist())
        for i in range(dim):
            pop[i].append(newval[i])

    #solutia = cel mai bun individ din ultima generatie
    cal=[pop[i][-1] for i in range(dim)]
    best=max([cal])
    i_sol = np.argmax(cal)
    sol=pop[i_sol][:-1]
    arata(sol,istoric_v)
    return sol,best


if __name__=="__main__":
    sol,val=GA("cost1.txt","valoare1.txt",50,40,100,0.8,0.1)