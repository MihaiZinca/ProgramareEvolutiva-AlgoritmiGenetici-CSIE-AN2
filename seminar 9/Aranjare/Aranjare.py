import numpy as np
import matplotlib.pyplot as grafic
from FunctiiCrossoverIndivizi import crossover_uniform, crossover_unipunct
from FunctiiMutatieIndivizi import m_binar
from FunctiiSelectii import elitism, SUS


#f. calitate
def fitness(x,n,m):
    # functia obiectiv pentru problema reginelor

    # I: x - individul - sir binar, m+n
    # E: c - calitate =1/(1+cost), unde cost inglobeaza aranjari gresite

    cost=0
    if x[n+m-1]==0 and x[0]==1 and x[1]==0:
        cost+=1
    if x[n+m-2]==0 and x[n+m-1]==1 and x[0]==0:
        cost+=1
    for i in range(n+m-2):
        if x[i]==0 and x[i+1]==1 and x[i+2]==0:
            cost+=1
    cost+=abs(sum(x)-m)
    return 1/(1+cost)


#genereaza populatia initiala
#I:
# n,m - nr. caini, nr. pisici
# dim - numarul de indivizi din populatie
#E: pop, cal - populatia initiala, vectorul calitatilor
def gen(n,m,dim):
    #defineste o variabila ndarray cu toate elementelo nule
    pop=np.zeros((dim,n+m),dtype=int)
    cal=np.zeros(dim)
    for i in range(dim):
        #genereaza candidatul permutare cu n elemente
        pop[i]=np.random.randint(0,2,n+m)
        cal[i]=fitness(pop[i],n,m)
    return pop, cal

#crossover pe populatia de parinti pop, de dimensiune dimx(n+m+1)
# I: pop,cal, n, m - ca mai sus
#     pc- probabilitatea de crossover
#E: po, co - populatia copiilor, co vectorul calitatilor
# este implementata recombinarea asexuata
def crossover_populatie(pop,cal,n,m,pc):
    #initializeaza populatia de copii, po, cu populatia parintilr
    po=pop.copy()
    co=cal.copy()
    dim,_=pop.shape
    #populatia este parcursa astfel incat sunt selectati indivizii 0,1 apoi 2,3 s.a.m.d
    for i in range(0,dim-1,2):
        #selecteaza parintii
        x = pop[i]
        y = pop[i+1]
        r = np.random.uniform(0,1)
        if r<=pc:
            #c1,c2 = crossover_uniform(x,y,n+m)
            c1, c2 = crossover_unipunct(x, y, n+m)
            val1=fitness(c1, n, m)
            val2= fitness(c2, n, m)
            po[i]=c1.copy()
            co[i]=val1
            po[i+1]=c2.copy()
            co[i+1]=val2
    return po, co



#mutatie asupra populatiei de copii
# I:pop,cal, n, m - ca mai sus
#   pm - probabilitatea de mutatie
#E: - mpop, mcal - populatia mutata, vectorul calitatilor
def mutatie_populatie(pop,cal,n,m,pm):
    mpop=pop.copy()
    mcal=cal.copy()
    dim, _ = pop.shape
    for i in range(dim):
        for k in range(m+n):
            #genereaza aleator daca se face mutatie
            if np.random.uniform(0,1) <= pm:
                #mutatie
                mpop[i,k]=m_binar(mpop[i,k])
        mcal[i]=fitness(mpop[i],n, m)
    return mpop, mcal

# grafic
def arata(sol,v):
    n=len(sol)
    t=len(v)

    x=[i for i in range(t)]
    grafic.plot(x,v,'ro-')
    grafic.ylabel("Calitate")
    grafic.xlabel("Generația")
    grafic.title("Evolutia celui mai bun individ/populatie in timp")
    grafic.show()



##ALGORITMUL GENETIC
# #I: n, m - dimensiunea problemei
#   dim - dimensiunea unei populatii
#   NMAX - numarul maxim de simulari ale unei evolutii
#   pc - probabilitatea de crossover
#   pm - probabilitatea de mutatie
#
#E: sol - solutia calculata de GA
#   val - cat este de buna solutia (val=1, val>.999999999)
def GA(n,m, dim,NMAX,pc,pm):
    #generarea populatiei la momentul initial
    pop,cal=gen(n,m, dim)
    #initializari pentru GA
    it=0
    gata=False
    maxim=np.max(cal)
    minim=np.min(cal)
    if maxim==minim:
        gata=True
    istoric_v=[maxim]
    #conditia de terminare:
        # am depasit un numar maxim de repetari, NMAX SAU
        # populatia contine indivizi cu aceeasi calitate SAU
        # nu a fost atins maximul functiei obiectiv, 1
    while it<NMAX and not gata and maxim<0.99999999 :
        #selectia parintilor
        spop,sval=SUS(pop,cal,dim,n+m)
        # recombinarea
        pop_o,cal_o=crossover_populatie(spop,sval,n,m,pc)
        # mutatia
        pop_mo, cal_mo=mutatie_populatie(pop_o,cal_o,n,m,pm)
        #selectia generatiei urmatoare
        newpop,newval=elitism(pop,cal,pop_mo,cal_mo,dim)
        #actualizarea populatie curente
        pop= newpop.copy()
        cal = newval.copy()
        minim=np.min(newval)
        maxim=np.max(newval)
        #opreste evolutia la populatia cu toti indivizii de aceeasicalitate
        if maxim==minim:
            gata=True
        else:
            it+=1
        istoric_v.append(maxim)

    i_sol=np.argmax(cal)
    sol=pop[i_sol]
    val=cal[i_sol]
    print(f"solutia calculata {sol} are calitatea {val}")
    arata(sol,istoric_v)
    return sol, val

if __name__=="__main__":
    numar_caini=38
    numar_pisici=17
    sol,val=GA(numar_caini,numar_pisici,300,350,0.85,0.15)
    print(f"verificare: {sum(sol)} vs {numar_pisici}")
    if fitness(sol,numar_caini,numar_pisici)<0.99999999:
        print("Nu a fost obtinuta o aranjare corecta")
    else:
        print("Aranjare corecta")
