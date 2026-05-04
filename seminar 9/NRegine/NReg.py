import numpy as np
import matplotlib.pyplot as grafic
from FunctiiCrossoverIndivizi import crossover_OCX, crossover_CX
from FunctiiMutatieIndivizi import m_perm_inserare, m_perm_interschimbare
from FunctiiSelectii import elitism, ruleta


# functia obiectiv pentru problema reginelor

# I: x - individul (permutarea) evaluat(a), n-dimensiunea problemei
# E: c - calitate (numarul de perechi de regine care nu se ataca
def foNR(x):
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
    pop=np.zeros((dim,n+1),dtype=int)
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
    #initializeaza populatia de copii, po, cu populatia parintilr
    po=pop.copy()
    dim,n=pop.shape
    n-=1
    #populatia este parcursa astfel incat sunt selectati indivizii 0,1 apoi 2,3 s.a.m.d
    for i in range(0,dim-1,2):
        #selecteaza parintii
        x = pop[i,:-1]
        y = pop[i+1,:-1]
        r = np.random.uniform(0,1)
        if r<=pc:
            # crossover x cu y - CX sau OCX - potrivite pentru NRegine
            c1,c2 = crossover_OCX(x,y,n)
            val1=foNR(c1)
            val2= foNR(c2)
            po[i][:n]=c1.copy()
            po[i][n]=val1
            po[i+1][:n]=c2.copy()
            po[i+1][n]=val2
    return po



#mutatie asupra populatiei de copii
# I:pop,dim,n - populatia de dimensiuni dimx(n+1)
#   pm - probabilitatea de mutatie
#E: - mpop - populatia mutata
def mutatie_populatie(pop,pm):
    mpop=pop.copy()
    dim, n = pop.shape
    n-=1
    for i in range(dim):
        #genereaza aleator daca se face mutatie
        r=np.random.uniform(0,1)
        if r<=pm:
            #mutatie in individul i - prin interschimbare
            x=m_perm_interschimbare(mpop[i,:n],n)
            mpop[i,:n]=x.copy()
            mpop[i,n]=foNR(x)
    return mpop

#MUTATIE


def arata(sol,v):
    # vizualizare asezare regine pe tabla de sah

    # I: sol - permutarea care defineste asezarea
    #    v - vectorul cu cea mai buna calitate din fiecare generatie
    # E: -

    n=len(sol)
    t=len(v)
    minim=min(v)
    t1="Evoluția calității (cel mai bun individ din fiecare generație).\nRezultatul "
    t2="Cea mai bună așezare a reginelor găsită.\nRezultatul "
    t4="este optim (" + str(minim) + " vs 0" + ")"
    if minim>0:
        t3="nu "
    else:
        t3=""
    titlu1 =t1+t3+t4
    titlu2=t2+t3+t4

    x=[i for i in range(t)]
    grafic.plot(x,v,'ro-')
    grafic.ylabel("Calitate")
    grafic.xlabel("Generația")
    grafic.title(titlu1)

    fig=grafic.figure()
    ax=fig.gca()
    y=[n-1-i+0.5 for i in range(n)]
    x=[sol[i]+0.5 for i in range(n)]
    grafic.plot(x,y,'r*',markersize=10)
    grafic.xticks(range(n+1))
    grafic.yticks(range(n+1))
    grafic.grid(True,which='both',color='k', linestyle='-', linewidth=1)
    ax.set_aspect('equal')
    grafic.title(titlu2)
    grafic.show()



##ALGORITMUL GENETIC PENTRU REZOLVAREA PROBLEMEI CELOR N REGINE
#I: n - dimensiunea problemei
#   dim - dimensiunea unei populatii
#   NMAX - numarul maxim de simulari ale unei evolutii
#   pc - probabilitatea de crossover
#   pm - probabilitatea de mutatie
#
#E: sol - solutia calculata de GA
#   val - maximul functiei fitness - n*(n-1)/2 - nr de perechi de regine aflate in pozitie de atac
def GA(n,dim,NMAX,pc,pm):
    #generarea populatiei la momentul initial
    pop=gen(n,dim)
    #initializari pentru GA
    it=0
    gata=False
    maxim=np.max(pop[:,n])
    istoric_v=[n*(n-1)//2-maxim]
    #conditia de terminare:
        # am depasit un numar maxim de repetari, NMAX SAU
        # populatia contine indivizi cu aceeasi calitate SAU
        # nu a fost atins maximul functiei obiectiv, n*(n-1)/2
    while it<NMAX and not gata and maxim<n*(n-1)//2 :
        #selectia parintilor
        spop,sval=ruleta(pop[:,:n],pop[:,n],dim,n)
        # adaugarea sval ca ultima coloana a slui spop
        pop_s=np.hstack((spop,sval.reshape(-1,1)))
        # recombinarea
        pop_o=crossover_populatie(pop_s,pc)
        # mutatia
        pop_mo=mutatie_populatie(pop_o,pm)
        #selectia generatiei urmatoare
        newpop,newval=elitism(pop[:,:n],pop[:,n],pop_mo[:,:n],pop_mo[:,n],dim)
        #actualizarea populatie curente
        pop[:, :n] = newpop.copy()
        pop[:, n] = newval.copy()
        minim=np.min(newval)
        maxim=np.max(newval)
        #opreste evolutia la populatia cu toti indivizii de aceeasicalitate
        if maxim==minim:
            gata=True
        else:
            it+=1
        istoric_v.append(n*(n-1)//2-int(maxim))

    i_sol=np.argmax(pop[:,n])
    sol=pop[i_sol,:n]
    val=n*(n-1)//2-pop[i_sol,n]
    print(f"solutia calculata {sol} are {val} erori de aranjare")
    arata(sol,istoric_v)
    return sol, val

if __name__=="__main__":
    sol,val=GA(14,120,500,0.85,0.15)
