#AICI O POPULATIE ESTE O LISTA DE INDIVIZI, UN INDIVID ESTE O LISTA CU 0,1 COMPLETATA CU VALOAREA

import numpy as np
import random
import matplotlib.pyplot as grafic


#verifica fezabilitatea alegerii x si calculeaza si f. obiectiv
def ok(x,c,v,max):
    val=np.dot(x,v)
    cost=np.dot(x,c)
    return cost<=max,val

#figurarea populatiei prin punctele (indice individ, calitate) - pentru a vedea variabilitatea in populatie
def reprezinta_pop(pop,dim,n):
    #fig = grafic.figure()
    x=[i for i in range(dim)]
    y=[pop[i][n] for i in range(dim)]
    grafic.plot(x,y,"gs",markersize=11)
    grafic.title("Calitatile indivizilor generați în populația inițială")
    grafic.xlabel("Index individ")
    grafic.ylabel("Calitate individ")
    grafic.show()


#genereaza populatia initiala
#I:
# fc, fv - numele fisierelor cost, valoare
# max - capacitatea maxima
# dim - numarul de indivizi din populatie
#E: pop - populatia initiala
def gen(fc,fv,max,dim):
    #citeste datele din fisierele cost si valoare
    c=np.genfromtxt(fc)
    v = np.genfromtxt(fv)
    #n=dimensiunea problemei
    n=v.size
    #lucreaza cu populatia ca lista de dim elemente - liste cu cate n+1 indivizi
    pop=[]
    for i in range(dim):
        gata=False
        while gata == False:
            #genereaza candidatul x cu elemente n 0,1
            #x=[random.choice([0,1]) for _ in range(n)]
            x=random.choices([0,1],k=n)
            gata,val=ok(x,c,v,max)
        #am gasit o solutie candidat fezabila, in data de tip lista x
        # adauga valoarea
        x.append(val)
        #adauga la populatie noul individ cu valoarea f. obiectiv - adauga inca o lista cu n+1 elemente ca element al listei pop
        pop.append(x)
    reprezinta_pop(pop, dim, n)
    return pop


if __name__=="__main__":
    p = gen("cost.txt", "valoare.txt", 50, 10)
    for element in p:
        print("Individ: ",element[:-1])
        print("   calitate:",element[-1])

