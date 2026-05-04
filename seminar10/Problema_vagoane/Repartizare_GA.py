import numpy as np
from FunctiiCrossoverIndivizi import crossover_uniform
from FunctiiMutatieIndivizi import m_ra
from FunctiiSelectii import SUS, elitism
import matplotlib.pyplot as grafic

# m containere cu mase memorate in mase.txt
# n vagoane
# alocarea unui container în câte un vagon astfel incat diferenta de incarcare sa fie cat mai mica:
# masa vagonului celui mai incarcat - masa vagonului celui mai putin incarcat sa fie minima
# alternativ, deviatia standard a vectorului maselor/vagon sa fie minima
# masa unui vagon: suma maselor containerelor incarcate in acel vagon

# individ - vector cu m componente x[i]= vagonul în care este încărcat containerul i, fiecare x[i] este in 0...n
#functia obiectiv
def fitness_alocare(x,mase,n):
    m=len(mase)
    vagoane=np.zeros(n,dtype=int) #masa incarcata in fiecare vagon
    for i in range(m):
        vagoane[x[i]]+=mase[i]
    #return 1/(1+np.max(vagoane)-np.min(vagoane)), vagoane
    return 1 / (1 + np.std(vagoane)), vagoane


#generarea populatiei initiale
def gen(fis,dim):
    date=np.genfromtxt(fis)
    #ultima valoare din fisierul in care pastram masele este numarul de vagoane
    p=len(date)
    mase=date[:-2]
    #m containere, n vagoane
    m=p-1
    n=int(date[-1])
    pop=np.zeros((dim,m),dtype=int)
    val=np.zeros(dim,dtype=float)
    for i in range(dim):
        pop[i] = np.random.randint(0,n,m)
        # evalueaza candidat
        val[i],_ = fitness_alocare(pop[i],mase,n)
    return pop, val, mase,n


#CROSSOVER - procedura standard: recombinare uniforma + recombinare asexuata
def crossover(pop,valori,dim,mase,n,pc):
    # initializeaza populatia de copii, po, cu matricea pop
    po=pop.copy()
    # initializeaza valorile populatiei de copii, val, cu vectorul valorilor curente, valori
    val=valori.copy()
    m=len(mase)
    #populatia este parcursa astfel incat sunt selectati aleator cate 2 indivizii - matricea este accesata dupa o permutare a multimii de linii 0,2,...,dim-1
    for i in range(0,dim-1,2):
        #selecteaza parintii
        x = pop[i]
        y = pop[i+1]
        r = np.random.uniform(0,1)
        if r<=pc:
            c1,c2 = crossover_uniform(x,y,m)
            v1,_=fitness_alocare(c1,mase,n)
            v2,_=fitness_alocare(c2,mase,n)
             #copiaza rezultatul in populatia urmasilor
            po[i] = c1.copy()
            po[i+1] = c2.copy()
            val[i]=v1
            val[i+1]=v2
    return po, val


#MUTATIE - procedura standard
def mutatie(po,vo,dim,mase,n,pm):
    mpo=po.copy()
    mvo=vo.copy()
    m=len(mase)
    for i in range(dim):
        mutat=False
        for j in range(m):
            r=np.random.uniform(0,1)
            if r<=pm:
                x=mpo[i,j]
                y=m_ra(0,n)
                mpo[i,j]=y
                mutat=True
        if mutat:
            mvo[i],_=fitness_alocare(mpo[i],mase,n)
    return mpo,mvo

#afisarea graficului evolutiilor
def arata(sol,v,mase,n):
    t=len(v)
    val=max(v)
    print("Solutia este: ",sol)
    _,vagoane=fitness_alocare(sol,mase,n)
    print("Incarcarea vagoanelor: ",vagoane)
    print("Cea mai mica diferenta de incarcare maxim-minim: ", np.max(vagoane)-np.min(vagoane))
    print("Deviatia standard : ", np.std(vagoane))
    fig = grafic.figure()
    x = [i for i in range(t)]
    y = [int((1-v[i])/v[i]) for i in range(t)]
    grafic.plot(x, y, 'ro-')
    grafic.ylabel("Deviatia standard / incarcare")
    grafic.xlabel("Generația")
    grafic.title("Evoluția costului celui mai bun individ din fiecare generație")
    grafic.show()



##ALGORITMUL GENETIC PENTRU REZOLVAREA PROBLEMEI DE REPARTIZARE

def GA(fc,dim,NMAX,pc,pm):
    pop,qual,mase,n=gen(fc, dim)
    m=len(mase)
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
        spop,sval=SUS(pop,qual,dim,m)
        po,vo=crossover(spop,sval,dim,mase,n,pc)
        mpo,mvo=mutatie(po,vo,dim,mase,n,pm)
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
    arata(sol,istoric_v,mase,n)
    return sol,val

if __name__=="__main__":
    #Problema din exemplu
    sol,val=GA("mase.txt",400,300,0.8,0.1)
    #Un exemplu mai complex
    sol,val=GA("mase1.txt",1000,500,0.8,0.1)
