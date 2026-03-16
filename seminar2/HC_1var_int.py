import numpy
from math import sin, cos
import matplotlib.pyplot as grafic


def f_obiectiv(x):
    # o functie de maximizat cu mai multe puncte de maxim local

    # I: x - punctul in care se calculeaza valoarea functiei
    # E: y - valoarea functiei in punctul x

    # o functie oarecare cu extreme locale

    # x**3  - x la puterea 3
    y = x**3 * sin(x/3) + x**3 * cos(2*x) -2*x*sin(3*x) + 2*x*cos(x)

    return y

def vecini(x, nr, pas, a, b):
    # calculează vecinii unui punct (pe o axă), impreuna cu calitatile acestora

    # I: x - punct curent
    #    nr - numar de vecini pe fiecare directie
    #    pas - distanta intre vecinii consecutivi
    #    a, b - capetele intervalului de lucru
    # E: v - lista vecini (2 linii: puncte, calitati)

    #sunt folosite liste comprehensive

    vec=[x+i*pas for i in range(-nr, nr+1) if ((x+i*pas>=a) and (x+i*pas<=b))]
    valv=[f_obiectiv(x+i*pas) for i in range(-nr, nr+1) if ((x+i*pas>=a) and (x+i*pas<=b))]
    return [vec,valv]


def HC(a, b, nrp, nrv, pas):
    # implementare hillclimbing pentru gasirea maximului unei functii de o variabila

    # I: a, b - capetele intervalului pe care e definita functia  (o axa)
    #    nrp - numarul de puncte initiale folosite de algoritm
    #    nrv - numarul de vecini pe fiecare directie utilizati (total 2*nrv+1 - 1 e punctul curent)
    #    pas - distanta intre doi vecini consecutivi
    # E: x - punct de maxim
    #    fx - valoarea maxima a functiei (in punctul x)
    # Obs.: daca nu se inchide graficul dupa rularea unui exemplu, la rularea urmatorului exemplu
    #    graficul va fi adaugat peste cel anterior

    # initializare liste goale de coordonate
    X=[None]*nrp
    Y=[None]*nrp
    # pentru fiecare punct initial
    for i in range(nrp):
        # aplicare hillclimbing pentru punctul initial curent generat aleator
        pc=numpy.random.uniform(a,b)    # alege un punct de inceput aleator
        local=0                         # nu am ajuns in maxim local
        while not local:
            # calculeaza vecinii punctului curent si valorile corespunzatoare ale functiei
            nvec, nval=vecini(pc,nrv,pas,a,b)
            valmax=max(nval)
            poz=nval.index(valmax)
            vecmax=nvec[poz]
            # inlocuieste punctul curent cu cel mai bun vecin, daca exista unul mai bun
            if valmax>f_obiectiv(pc):
                pc=vecmax
            else:
                # nici un vecin mai bun, inseamna ca am atins un maxim local
                local=1
        # memoreaza cel mai bun punct gasit si valoarea corespunzatoare a functiei
        X[i]=vecmax
        Y[i]=f_obiectiv(vecmax)

    # determina cel mai bun dintre punctele finale si valoarea corespunzatoare a functiei obiectiv
    fx=max(Y)
    poz=Y.index(fx)
    x=X[poz]

    # afiseaza rezultatele si graficul (daca stii sa desenezi graficul)
    print("Valoare maxima calculata: ", fx)
    print("E atinsa in punctul: ", x)
    deseneaza(a, b, X, Y, x, fx)
    return x,fx


def deseneaza(a, b, X, Y, xmax, ymax):
    # vizualizare rezultate pentru hillclimbing 1 variabila

    # I: a, b - capete interval de lucru
    #    X, Y - liste cu coordonatele punctelor finale calculate
    #    xmax, ymax - corrdonatele celui mai bun punct gasit
    # E: -

    x=numpy.arange(a,b,0.01)
    grafic.plot(x,[f_obiectiv(i) for i in x],'k-')
    grafic.plot(X,Y,'bo',label='optim local')
    grafic.plot(xmax,ymax,'r*',label='cel mai bun calculat')
    grafic.title("Graficul functiei f")
    grafic.legend()
    grafic.show()



if __name__=="__main__":
    x, fx = HC(0, 50, 100, 100, 0.01)