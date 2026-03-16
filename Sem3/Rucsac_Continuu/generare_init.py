#AICI O POPULATIE ESTE O LISTA DE INDIVIZI, UN INDIVID ESTE O LISTA CU ELEMENTE IN [0,1] COMPLETATA CU VALOAREA

import matplotlib.pyplot as grafic
import numpy as np
import random


#verifica fezabilitatea alegerii x si calculeaza si f. obiectiv
def ok(x,c,v,max):
    val=sum([x[i]*v[i] for i in range(len(x))])
    cost=sum([x[i]*c[i] for i in range(len(x))])
    return cost<=max,val


#genereaza populatia initiala
#I:
# fc, fv - numele fisierelor cost, valoare
# max - capacitatea maxima
# dim - numarul de indivizi din populatie
#E: pop - populatia initiala
def gen(fc,fv,max,dim):
    #citeste datele din fisierele cost si valoare
    c=np.genfromtxt(fc)
    v=np.genfromtxt(fv)
    #n=dimensiunea problemei
    n=len(c)
    #lucreaza cu populatia ca lista de dim elemente - liste cu cate n+1 indivizi
    pop=[]
    for i in range(dim):
        gata=False
        while gata == False:
            #genereaza candidatul x cu elemente pe [0,1]
            x=[random.uniform(0,1) for _ in range(n)]
            gata,val=ok(x,c,v,max)
        #am gasit o solutie candidat fezabila, in data de tip lista x
        # adauga valoarea
        x=x+[val]
        #adauga la populatie noul individ cu valoarea f. obiectiv - adauga inca o lista cu n+1 elemente ca element al listei pop
        pop=pop+[x]
    reprezinta_pop(pop,dim,n)
    return pop

#figurarea populatiei prin punctele (indice individ, calitate) - pentru a vedea variabilitatea in populatie
def reprezinta_pop(pop,dim,n):
    x=[i for i in range(dim)]
    y=[pop[i][n] for i in range(dim)]
    grafic.plot(x,y,"gs",markersize=11)
    grafic.title("Calitatile indivizilor generați în populația inițială")
    grafic.xlabel("Index individ")
    grafic.ylabel("Calitate individ")
    grafic.show()


if __name__=="__main__":
    p = gen("cost.txt", "valoare.txt", 50, 10)
    for element in p:
        list_format=[float(f"{el:.3f}") for el in element[:-1]]
        print(f"Individul: {list_format} , calitatea {element[-1]:.4f}")

