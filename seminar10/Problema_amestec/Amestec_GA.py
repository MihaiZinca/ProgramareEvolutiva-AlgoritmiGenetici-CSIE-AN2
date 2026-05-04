import numpy as np
from FunctiiCrossoverIndivizi import crossover_unipunct, crossover_uniform
from FunctiiMutatieIndivizi import m_fluaj
from FunctiiSelectii import SUS, elitism
import matplotlib.pyplot as grafic

masa_pachet=0.2 # masa unui pachet (in kg)
# m cantitati de produse brute memorate in cantitati.txt (in kg.)
# n tipuri de combinatii, memorate in combinatii.txt
# n profituri, memorate in profituri.txt

#citirea datelor
def citire_date(fis_pr,fis_comb,fis_cant):
    profit = np.genfromtxt(fis_pr)
    combinatii = np.genfromtxt(fis_comb)
    cantitati = np.genfromtxt(fis_cant)
    return profit, combinatii, cantitati

#definirea spatiului solutiilor
# individ - vector cu n componente x[i]= numărul de pachete din combinația i
# calculul numarului maxim de pachete/combinatie

def limite(combinatii,cantitati):
    n,m=np.shape(combinatii)
    limite_s=np.zeros(n)
    nr_produse=np.zeros(m)
    for i in range(n):
        #pt fiecare combinatie i, vectorul maximului de pachete in functie de materia prima folosita
        for j in range(m):
            if combinatii[i,j]:
                nr_produse[j]=cantitati[j]/(masa_pachet*combinatii[i,j]/100)
            else:
                nr_produse[j]=1000000
        limite_s[i]=int(np.min(nr_produse))
    return limite_s


#functia obiectiv - dacă un individ este fezabil și profitul adus
def fitness_alocare(x,cantitati,combinatii,profituri):
    n,m=np.shape(combinatii)
    profit=np.dot(x,profituri)
    #cat consuma fiecare combinatie din fiecare produs/pachet
    #consum_combinatie[i,j] - cat consuma combinatia i din produsul j
    consum_combinatie=combinatii*masa_pachet/100
    #cat consuma din fiecare produs alegerea x
    for i in range(n):
        consum_combinatie[i,:]*=x[i]
    #verificarea fezabilitatii
    #total consum din fiecare produs - suma pe coloane
    total_consum_combinatie=np.sum(consum_combinatie,0)
    fezabil = True
    for i in range(m):
        if total_consum_combinatie[i]>cantitati[i]:
            fezabil=False
            break
    return fezabil,profit, total_consum_combinatie


#generarea populatiei initiale
def gen(profituri, combinatii, cantitati,limite_s,dim):
    n, _ = np.shape(combinatii)
    pop=np.zeros((dim,n),dtype=int)
    val=np.zeros(dim,dtype=float)
    i=0
    while(i<dim):
        for j in range(n):
            pop[i,j]=np.random.randint(0,limite_s[j]+1)
        fezabil, profit, _=fitness_alocare(pop[i],cantitati,combinatii,profituri)
        if fezabil:
            val[i]=profit
            i+=1
    return pop, val


#CROSSOVER - procedura standard: recombinare uniforma + recombinare asexuata
def crossover(pop,valori,cantitati,combinatii,profituri,dim,pc):
    # initializeaza populatia de copii, po, cu matricea pop
    po=pop.copy()
    # initializeaza valorile populatiei de copii, val, cu vectorul valorilor curente, valori
    val=valori.copy()
    #populatia este parcursa astfel incat sunt selectati aleator cate 2 indivizii - matricea este accesata dupa o permutare a multimii de linii 0,2,...,dim-1
    for i in range(0,dim-1,2):
        #selecteaza parintii
        x = pop[i]
        y = pop[i+1]
        r = np.random.uniform(0,1)
        if r<=pc:
            c1,c2 = crossover_uniform(x,y,len(x))
            fezabil, profit, _ = fitness_alocare(c1, cantitati, combinatii, profituri)
            #copiaza rezultatul in populatia urmasilor, daca este fezabil
            if fezabil:
                po[i] = c1.copy()
                val[i] = profit
            fezabil, profit, _ = fitness_alocare(c2, cantitati, combinatii, profituri)
            if fezabil:
                po[i+1] = c2.copy()
                val[i+1]=profit
    return po, val


#MUTATIE - procedura standard
def mutatie(po,vo,cantitati, combinatii, profituri,limite_s,dim,pm):
    mpo=po.copy()
    mvo=vo.copy()
    for i in range(dim):
        mutat=False
        x=mpo[i].copy()
        for j in range(len(x)):
            r=np.random.uniform(0,1)
            if r<=pm:
                y=m_fluaj(x[j],0,limite_s[j])
                x[j]=y
                mutat=True
        if mutat:
            fezabil, profit, _ = fitness_alocare(x, cantitati, combinatii, profituri)
            if fezabil:
                mpo[i]=x.copy()
                mvo[i]=profit
    return mpo,mvo

#afisarea graficului evolutiilor
def arata(sol,valm,total_consum,cantitati,v):
    t=len(v)
    print("Solutia este: ",sol)
    print("Profitul: ",valm)
    print('Total ramas: ',cantitati-total_consum)
    fig = grafic.figure()
    x = [i for i in range(t)]
    grafic.plot(x, v, 'ro-')
    grafic.ylabel("Profit maxim / generatie")
    grafic.xlabel("Generația")
    grafic.title("Evoluția profitului celui mai bun individ din fiecare generație")
    grafic.show()



##ALGORITMUL GENETIC PENTRU REZOLVAREA PROBLEMEI DE REPARTIZARE

def GA(fis_pr,fis_comb,fis_cant,dim,NMAX,pc,pm):
    profituri, combinatii, cantitati = citire_date(fis_pr,fis_comb,fis_cant)
    limite_s = limite(combinatii, cantitati)
    n=len(limite_s)
    pop,qual=gen(profituri,combinatii,cantitati,limite_s,dim)
    #initializari pentru GA
    it=0
    gata=False
    #in istoric_v pastram cel mai bun cost din populatia curenta, la fiecare moment al evolutiei
    v_max=np.max(qual)
    istoric_v=[v_max]
    nr_max=1
    # evolutia - cat timp
    #                - nu am depasit NMAX  si
    #                - populatia are macar 2 indivizi cu calitati diferite  si
    #                - valoarea maxima nu s-a schimbat pe parcursul a NMAX/3 iteratii
    while it<NMAX and not gata:
        spop,sval=SUS(pop,qual,dim,n)
        po,vo=crossover(spop,sval,cantitati,combinatii,profituri,dim,pc)
        mpo,mvo=mutatie(po,vo,cantitati,combinatii,profituri,limite_s,dim,pm)
        newpop,newval=elitism(pop,qual,mpo,mvo,dim)
        minim=np.min(newval)
        maxim=np.max(newval)
        if maxim>v_max:
            nr_max=1
            v_max=maxim
        else:
            if maxim==v_max:
                nr_max+=1
        if maxim==minim or nr_max>NMAX/3:
            gata=True
        else:
            it=it+1
        tt=np.max(newval)
        istoric_v.append(tt)
        pop=newpop.copy()
        qual=newval.copy()
    i_sol=np.argmax(qual)
    sol=pop[i_sol]
    val=maxim
    _, _, total_consum_combinatie = fitness_alocare(sol, cantitati, combinatii, profituri)
    arata(sol,val,total_consum_combinatie,cantitati,istoric_v)
    return sol,val


if __name__=="__main__":
    # Problema din enunt
    sol,val=GA('profituri.txt','combinatii.txt','cantitati.txt',400,700,0.9,0.3)
    #sol,val=ag.GA('profituri.txt','combinatii.txt','cantitati.txt',5000,1000,0.9,0.3)
    #Exemple de solutie:
    #Solutia este:  [1250   30    0  265  117]
    #Profitul:  29065.0
    #Total ramas:  [ 0.1 17.5  0.   0. ]
    #Sau
    #Solutia este: [1120   35  103  268  129]
    #Profitul: 28156.0
    #Total ramas: [0.1  18.85  0.    0.05]
    # Evident, pot fi si altele

    #Un alt exemplu pentru test, cu alte date de intrare
    #sol,val=GA('profituri1.txt','combinatii1.txt','cantitati1.txt',1000,1000,0.9,0.3)
    #Exemplu de solutie:
    #Solutia este:  [ 323 1464  734   39    0]
    #Profitul:  43833.0
    #Total ramas:  [0.000e+00 3.361e+01 3.000e-02 3.800e-01 1.030e+01 1.400e-01]