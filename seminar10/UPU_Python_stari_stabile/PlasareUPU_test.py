import numpy as np
import matplotlib.pyplot as grafic
from FunctiiMutatieIndivizi import m_ra
from FunctiiSelectii import turneu_2,genitor

#functia obiectiv
def foUPU(p,fr,n):
    val=0
    for i in range(n):
        for j in range(n):
            val+=fr[i,j]*(1.7+3.4*np.sqrt(np.square(p[0]-i)+np.square(p[1]-j)))
    return 1/val



#genereaza populatia initiala
#I:
# ff - numele fisierului frecventelor
# dim - numarul de indivizi din populatie
#E: pop, qual - populatia initiala si vectorul calitatilor
#   fr, n:matricea frecventelor si dimeniunea problemei - pentru transferuri in alte functii
def gen(ff,dim):
    #citeste datele din fisier
    fr = np.genfromtxt(ff)
    #n=dimensiunea problemei
    n=len(fr)
    pop=np.zeros([dim,2],dtype='int')
    qual=np.zeros(dim)
    for i in range(dim):
        pop[i]=np.random.randint(0,n,2)
        qual[i]=foUPU(pop[i],fr,n)
    return pop,qual,n,fr


#crossover pe populatia de parinti pop, cu vectorul de calitati qual
# I: pop,qual,dim_p si n
#     probabilitatea de crossover =1
#E: po,qo - populatia copiilor, calitati qo
def crossover_populatie(pop,qual,dim_p,n,fr):
    po=pop.copy()
    qo=qual.copy()
    #populatia este parcursa astfel incat sunt selectati indivizii dupa un amestec
    poz=np.random.permutation(dim_p)
    for i in range(0,dim_p-1,2):
        #selecteaza parintii
        i1=poz[i]
        i2=poz[i+1]
        x = pop[i1].copy()
        y = pop[i2].copy()
        po[i1][0]=x[0]
        po[i1][1]=y[1]
        po[i2][0]=y[0]
        po[i2][1]=x[1]
        qo[i1]=foUPU(po[i1],fr,n)
        qo[i2]=foUPU(po[i2],fr,n)
    return po,qo



#mutatie asupra populatiei de copii
# I:pop,qual,dim_c,n - populatia, calitatile, dimensiunea populatiei de copii, dimensiunea matricei fr
#   pm - probabilitatea de mutatie
#E: - mpo,mqo - populatia mutata, vectorul calitatilor
def mutatie_populatie(pop,qual,dim_c,n,fr,pm):
    mpo=pop.copy()
    mqo=qual.copy()
    x=np.zeros(2,dtype='int')
    for i in range(dim_c):
        x[:]=pop[i]
        for j in range(2):
            #genereaza aleator daca se face mutatie in individul i gena j
            r=np.random.uniform(0,1)
            if r<=pm:
                #mutatie prin resetare aleatoare
                x[j]=m_ra(0,n)
                mpo[i]=x.copy()
                mqo[i]=foUPU(mpo[i],fr,n)
    return mpo,mqo


def arata(sol,v):
    # vizualizare rezultate
    n=len(sol)
    t=len(v)
    val=max(v)
    print("Cea mai buna valoare calculată: ",1/val)
    print("Alegerea corespunzatoare este: ",sol)
    x=[i for i in range(t)]
    y=[1/v[i] for i in range(t)]
    grafic.plot(x,y,'ro-')
    grafic.ylabel("Valoarea")
    grafic.xlabel("Generația")
    grafic.title("Evoluția calității celui mai bun individ din fiecare generație")




##ALGORITMUL GENETIC PENTRU REZOLVAREA PROBLEMEI PLASARII UPU
#I: ff - fisierul cu frecvente
#   dim - dimensiunea unei populatii
#   dimc - dimensiunea populatiei de copii = dimensiunea parintilor: pc=1
#   NMAX - numarul maxim de simulari ale unei evolutii
#   pm - probabilitatea de mutatie
#
#E: sol - solutia calculata de GA
#   val - 1/maximul functiei fitness - cost_minim
def GA(ff,dim,dimc,NMAX,pm):
    #generarea populatiei la momentul initial
    pop,qual,n,fr=gen(ff,dim)
     #initializari pentru GA
    it=0
    gata=False
    #in istoric_v pastram cel mai bun cost din populatia curenta, la fiecare moment al evolutiei
    istoric_v=[np.max(qual)]
    # evolutia - cat timp
    #                - nu am depasit NMAX  si
    #                - populatia are macar 2 indivizi cu calitati diferite  si
    #                - in ultimele NMAX/3 iteratii s-a schimbat macar o data calitatea cea mai buna
    nrm=1
    while it<NMAX and not gata:
        spop, sval = turneu_2(pop,qual,dim,dimc,2,2)
        po,qo = crossover_populatie(spop,sval, dimc, n, fr)
        mpo,mqo = mutatie_populatie(po,qo,dimc,n,fr,pm)
        newpop, newval = genitor(pop,qual,mpo,mqo,dim,dimc)
        minim=np.min(newval)
        maxim=np.max(newval)
        if maxim==istoric_v[it]:
            nrm=nrm+1
        else:
            nrm=0
        if maxim==minim or nrm==int(NMAX/3):
            gata=True
        else:
            it=it+1
        istoric_v.append(maxim)
        pop =newpop.copy()
        qual =newval.copy()
    i_sol=np.argmax(qual)
    sol=pop[i_sol]
    val=maxim
    arata(sol,istoric_v)
    fig = grafic.figure()
    ax = fig.gca()
    n = len(fr)
    for i in range(n):
        for j in range(n):
            if sol[0] == i and sol[1] == j:
                col = 'r'
            else:
                col = 'k'
            grafic.text(j + 0.5, n - 1 - i + 0.5, fr[i, j], horizontalalignment='center',
                        verticalalignment='center', fontsize=10, color=col)
    grafic.xticks(range(n + 1))
    grafic.yticks(range(n + 1))
    grafic.grid(True, which='both', color='k', linestyle='-', linewidth=1)
    ax.set_aspect('equal')
    grafic.title('Amplasare unitate de urgență')
    grafic.show()
    return sol,1/val

if __name__=="__main__":
    #sol,val=GA("frecventa1.txt",20,4,50,0.3) # sol=[4,5]
    sol,val=GA("frecventa2.txt",20,4,100,0.3) # sol=[4,10]