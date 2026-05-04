import numpy as np
from FunctiiCrossoverIndivizi import crossover_OCX
from FunctiiMutatieIndivizi import m_perm_interschimbare, m_perm_inserare
from FunctiiSelectii import SUS, elitism
import matplotlib.pyplot as grafic
import datetime


#reprezentarea unui mesaj in format numeric si eliminarea dublurilor
# I: mesaj - sir de caractere format cu litere mici ale alfabetului englez
# E: numd - varianta numerica cu 'a'-->0 a mesajului din care au fost eliminate dublurile
def mesaj2num(mesaj):
    #obtinerea reprezentarii 'a'-0, 'b'-1,...
    mesajnum=[ord(c)-ord('a') for c in mesaj]
    #eliminarea dublurilor
    numd=list(dict.fromkeys(mesajnum))
    return numd

#preluarea mesajului corect si a mesajului codificat, obtinerea reprezentarilor numerice cu eliminarea dublurilor
#mesajele sunt memorate pe cate o linie a fisierului text fis
# I: fis - fisierul din care sunt preluate variantele corecta si codificata a mesajului
# E: mesaj, cod, dimensiune - variantele numerice ale mesajului corect, respectiv mesajului codificat si dimensiunea acestora
#    mesaj2 - mesajul codificat original, pentru obtinerea decodificarii
#   mesaj1 - mesajul initial corect
def preia_date(fis):
    #este preluat tot textul intr-o singura linie - fara eventualele \n
    with open(fis, 'r') as file:
        data = file.read().replace('\n', '')
    n=int(len(data)/2)
    #fiecare jumatate de text - mesajul corect, mesajul codificat
    mesaj1=data[:n]
    mesaj2=data[n:]
    mesaj=mesaj2num(mesaj1)
    cod=mesaj2num(mesaj2)
    return mesaj,cod,len(mesaj), mesaj1, mesaj2


#functia obiectiv
# I: p - permutarea care reprezinta corespondenta caracter din alfabetulenglez  - caracter corespondent din mesaj codificat - in repr. numerica
#    p este reprezentarea cromozomiala a unui candidat la solutie
#    mesaj, cod, lm - variantele numerice ale mesajului corect, respectiv mesajului codificat si dimensiunea acestora
# E : fitnessul, dat de expresia 1/(1+ suma|numar(caracter) din mesaj corect - numar(caracter) din mesaj codificat|
#     fitnesul solutiei corecte este 1
def foCod(p,lm,mesaj,cod):
    val=0
    for i in range(lm):
        j=np.where(p==cod[i])
        val+=abs(mesaj[i]-j[0][0])
    return 1/(1+val)


#generarea populatiei initiale
# I : fis - fisierul din care citim mesajele
#     dim - dimensiunea populatiei
# E:  pop - populatia de permutari care reprezinta candidati la solutie
#     val - vectorul calitatilor
#     mesaj, cod, mesaj1, mesaj2 - ca mai sus
def gen(fis,dim):
    #citeste datele din fisierul cu cele 2 mesaje
    mesaj,cod,lm,mesaj1,mesaj2 =preia_date(fis)
    #n=dimensiunea problemei
    n = 26
    pop=np.zeros((dim,n),dtype=int)
    val=np.zeros(dim,dtype=float)
    for i in range(dim):
        #genereaza candidatul permutare cu n elemente
        pop[i] = np.random.permutation(n)
        # evalueaza candidat
        val[i] = foCod(pop[i],lm,mesaj,cod)
    return pop, val, mesaj, cod, lm, mesaj1, mesaj2


#CROSSOVER - procedura standard: OCX si recombinare asexuata
def crossover(pop,valori,dim,lm,mesaj,cod,pc):
    # initializeaza populatia de copii, po, cu matricea pop
    po=pop.copy()
    # initializeaza valorile populatiei de copii, val, cu vectorul valorilor curente, valori
    val=valori.copy()
    #populatia este parcursa astfel incat sunt selectati aleator cate 2 indivizii - matricea este accesata dupa o permutare a multimii de linii 0,2,...,dim-1
    poz=np.random.permutation(dim)
    for i in range(0,dim-1,2):
        #selecteaza parintii
        x = pop[poz[i]]
        y = pop[poz[i+1]]
        r = np.random.uniform(0,1)
        if r<=pc:
            c1,c2 = crossover_OCX(x,y,26)
            v1=foCod(c1,lm,mesaj,cod)
            v2=foCod(c2,lm,mesaj,cod)
             #copiaza rezultatul in populatia urmasilor
            po[poz[i]] = c1.copy()
            po[poz[i+1]] = c2.copy()
            val[poz[i]]=v1
            val[poz[i+1]]=v2
    return [po, val]


#MUTATIE - procedura standard
def mutatie(po,vo,dim,lm,mesaj,cod,pm):
    mpo=po.copy()
    mvo=vo.copy()
    for i in range(dim):
        r=np.random.uniform(0,1)
        if r<=pm:
            x=mpo[i]
            y=m_perm_interschimbare(x,26)
            #y = m_perm_inserare(x,26)
            mpo[i]=y
            mvo[i]=foCod(y,lm,mesaj,cod)
    return [mpo,mvo]

#afisarea graficulelor evolutiilor intr-o singura figura
def arata(sol, v):
    t = len(v)
    val = max(v)
    print(f"Cea mai buna valoare calculată: {val:.3f}")
    print(f"Diferenta minima mesaj-mesaj decodificat cu cel mai bun cod: {int((1 - val) / val)}")
    print(f"Permutarea cod este: {sol}")

    x = [i for i in range(t)]

    # Creez figura cu 2 subploturi (pe 2 rânduri)
    fig, axs = grafic.subplots(2, 1, figsize=(8, 8))

    # Primul grafic
    y1 = [v[i] for i in range(t)]
    axs[0].plot(x, y1, 'ro-')
    axs[0].set_ylabel("Valoarea maxima")
    axs[0].set_xlabel("Generația")
    axs[0].set_title("Evoluția calității celui mai bun individ")

    # Al doilea grafic
    y2 = [int((1 - v[i]) / v[i]) for i in range(t)]
    axs[1].plot(x, y2, 'bo-')
    axs[1].set_ylabel("Diferența mesaj - mesaj decodificat")
    axs[1].set_xlabel("Generația")
    axs[1].set_title("Evoluția diferenței pe generații")

    grafic.tight_layout()
    grafic.show()


#afisarea graficulelor evolutiilor in cate o figura
def arata1(sol,v):
    t=len(v)
    val=max(v)
    print("Cea mai buna valoare calculată: ",val)
    print("Diferenta minima mesaj-mesaj decodificat cu cel mai bun cod: ", int((1-val)/val))
    print("Permutarea cod este: ",sol)
    grafic.figure()
    x=[i for i in range(t)]
    y=[v[i] for i in range(t)]
    grafic.plot(x,y,'ro-')
    grafic.ylabel("Valoarea maxima ")
    grafic.xlabel("Generația")
    grafic.title("Evoluția calității celui mai bun individ din fiecare generație")
    grafic.figure()
    x = [i for i in range(t)]
    y = [int((1-v[i])/v[i]) for i in range(t)]
    grafic.plot(x, y, 'ro-')
    grafic.ylabel("Diferenta mesaj-mesaj decodificat cu cel mai bun cod")
    grafic.xlabel("Generația")
    grafic.title("Evoluția calității celui mai bun individ din fiecare generație")
    grafic.show()


# afisarea corespondentelor intr-un fisier text si scrierea pe monitor a mesajului decodificat conform solutiei calculate de GA
# I: Solutie - permutarea cu cel mai bun fitness, declarata de GA castigatoare
#    fiso - fisierul in care sunt scrise corespondentele date de Solutie
#    mesaj2- mesajul codificat
#    mesaj1 - mesajul corect
# E: Alfabet, Coresp - sirurile de caractere "abc...z" si corespondentul pentru decodificare
def scrie_rezultate(Solutie,fisO,mesaj1,mesaj2):
    Alfabet=''
    Coresp=''
    for i in range(26):
        Alfabet=Alfabet + ' ' + chr(i+ord('a'))
        Coresp=Coresp+' '+chr(Solutie[i]+ord('a'))
    with open(fisO, 'w') as fis:
        fis.write(Alfabet+'\n'+Coresp)
    D=''
    lm=len(mesaj2)
    for i in range(lm):
        lit=mesaj2[i]
        poz=ord(lit)-ord('a')
        pp=np.where(Solutie==poz)
        D=D+Alfabet[2*pp[0][0]+1]
    print(f"\nMesajul decodificat: {D}")
    print(f"\nMesajul corect: {mesaj1}")
    return Alfabet, Coresp



##ALGORITMUL GENETIC PENTRU REZOLVAREA PROBLEMEI DE CODIFICARE
#I: fc - fisierul cu cele 2 mesaje
#   dim - dimensiunea unei populatii
#   NMAX - numarul maxim de simulari ale unei evolutii
#   pc - probabilitatea de crossover
#   pm - probabilitatea de mutatie
#
#E: sol - solutia calculata de GA
#   val - diferenta minima
def GA(fc,dim,NMAX,pc,pm,fisO):
    #inregistrarea timpului necesar executiei - start
    tstart = datetime.datetime.now()
    #generarea populatiei la momentul initial
    pop,qual,mesaj,cod,lm,mesaj1, mesaj2 =gen(fc,dim)
    #initializari pentru GA
    it=0
    gata=False
    #in istoric_v pastram cel mai bun cost din populatia curenta, la fiecare moment al evolutiei
    tt=np.max(qual)
    istoric_v=[tt]
    # evolutia - cat timp
    #                - nu am depasit NMAX  si
    #                - populatia are macar 2 indivizi cu calitati diferite  si
    #                - valoarea maxima este subunitara - fitness-ul trebuie adus pe valoarea 1
    while it<NMAX and not gata and tt!=1:
        spop,sval=SUS(pop,qual,dim,26)
        po,vo=crossover(spop,sval,dim,lm,mesaj,cod,pc)
        mpo,mvo=mutatie(po,vo,dim,lm,mesaj,cod,pm)
        newpop,newval=elitism(pop,qual,mpo,mvo,dim)
        minim=np.min(newval)
        maxim=np.max(newval)
        if maxim==minim :
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
    arata(sol,istoric_v)
    A, C=scrie_rezultate(sol,fisO,mesaj1,mesaj2)
    # timpul la care s-a incheiat executia
    tstop = datetime.datetime.now()
    print(f"\n\nTimpul de executie este de {(tstop - tstart).total_seconds()} secunde")
    return sol,val, A,C

if __name__=="__main__":
    #sol,val,A,C=GA("intrari.txt",500,300,0.8,0.2,"iesiri.txt")
    sol,val,A,C=GA("intrari1.txt",1000,300,0.8,0.2,"iesiri1.txt")
    #sol,val,A,C=GA("intrari_exp.txt",500,300,0.8,0.2,"iesiri_exp.txt")
    grafic.show()
