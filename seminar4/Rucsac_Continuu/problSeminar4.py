#f:[-7,15] -> R
#x+y-2z<=14 -conditie, x,y,z apartine [-7,15]
#f(x,y,z)=x^3 +2y -3z -functia fitness(Maximizat)

#INDIVID  {Vx, Vy,Vz,ff(val functie fitness}

#8 indivizi si vrem sa maximizam functia fitness
#1)Definesc functia fitness
# f(x,y,z), asigurandu ma ca x+y-2z<=14
#2)Generare populatia initiala
# ->generam primul individ in intervalul [-7,15]
# x=1 y=2 z=3 ->verificam functia fitness 1+2-3*2<=14 ? Da => il adaug la populatie
# ->generam al doilea individ
# x=15 y=15 z=2 15+ 15 -3 *2<=14 ? Nu => Regeneram pana cand verifica identitatea

import numpy as np
import random
import matplotlib.pyplot as grafic
import copy

#functia fitness
#input x,y,z
#output:validitatea individului(daca respecta conditia),valoarea functiei
def fitness(x,y,z):
    val=x+y-2*z
    val_functie=x**3 +2*y -3*z
    return val<=14, val_functie

#genereaza populatia initiala
#I:
# a,b - capetele intervalului
# dim - numarul de indivizi din populatie
# E:
#pop - populatia insotita de calitati
def gen(a,b,dim):
    #lucreaza cu populatia ca lista de dim elemente - liste cu cate n+1 indivizi
    pop=[]
    for i in range(dim):
        gata=False
        while gata == False:
            #genereaza candidatul x cu elemente 0,1
            x=[random.uniform(a,b) for _ in range(3)]
            ok,val=fitness(x[0],x[1],x[2])
        #am gasit o solutie candidat fezabila, in data de tip lista x
        # adauga valoarea
            if ok:
                gata = True
                x.append(val)
                pop.append(x)
        #adauga la populatie noul individ cu valoarea f. obiectiv - adauga inca o lista cu n+1 elemente ca element al listei pop

    vectv=[pop[i][-1] for i in range(dim)]
    grafic.plot(vectv, "gs", markersize=11,label="Initial")
    return pop

#mutatia uniforma

#I:a,b - intervalul in care se face resetarea
#E: y - noua valoare
def m_uniforma(a,b):
    y=np.random.uniform(a,b)
    return y

#MUTATIE UNIFORMA
#I:
#pop - populatia insotita de calitati - in GA populatia de copii
# dim - numarul de indivizi din populatie
# pm - probabilitatea de mutatie
# E:
#mpop - populatia dupa mutatie
def mutatie_populatie(pop,a,b,pm):
    # copiem populatia curenta in rezultatul mpop
    mpop=copy.deepcopy(pop)
    dim=len(pop)
    n=3
    for i in range(dim):
        #copiem in x individul i
        x=pop[i][:n].copy()
        mutatie=False
        for j in range(n):
            #genereaza aleator daca se face mutatie in individul i gena j
            r=np.random.uniform(0,1)
            if r<=pm:
                x[j]=m_uniforma(a,b)
                mutatie=True
        #individul rezultat sufera posibil mai multe mutatii
        #daca este fezabil, este pastrat
        if mutatie:
            fez, val = fitness(x[0],x[1],x[2])
            if fez:
                x.append(val)
                mpop[i]=x.copy()

    grafic.plot([mpop[i][n] for i in range(dim)],"rs",markersize=7,label="Dupa mutatie")
    return mpop



if __name__ == "__main__":

    a = -7
    b = 15
    dim = 8
    pm = 0.2

    populatie = gen(a,b,dim)

    print("Populatia initiala:")
    for ind in populatie:
        print(ind)

    populatie_mutata = mutatie_populatie(populatie,a,b,pm)

    print("\nPopulatia dupa mutatie:")
    for ind in populatie_mutata:
        print(ind)

    grafic.legend()
    grafic.show()