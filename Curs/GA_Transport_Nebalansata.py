import numpy
import matplotlib.pyplot as grafic
from FunctiiSelectii import SUS, elitism
from FunctiiCrossoverIndivizi import crossover_CX
from FunctiiMutatieIndivizi import m_perm_interschimbare


def balansare(oferta, cerere, costuri):
    suma_oferta = numpy.sum(oferta)
    suma_cerere = numpy.sum(cerere)

    if suma_oferta > suma_cerere:
        diferenta = suma_oferta - suma_cerere
        cerere = numpy.append(cerere, diferenta)
        coloana_noua = numpy.zeros((len(oferta), 1))
        costuri = numpy.hstack((costuri, coloana_noua))
        print("Problema nebalansata -> s-a adaugat destinatie fictiva")

    elif suma_cerere > suma_oferta:
        diferenta = suma_cerere - suma_oferta
        oferta = numpy.append(oferta, diferenta)
        linie_noua = numpy.zeros((1, len(cerere)))
        costuri = numpy.vstack((costuri, linie_noua))
        print("Problema nebalansata -> s-a adaugat sursa fictiva")

    else:
        print("Problema este deja balansata")

    return oferta, cerere, costuri


def GA_Transport(fo,fc,fcost,dim,nmax,pr,pm):

    oferta=numpy.genfromtxt(fo)
    cerere=numpy.genfromtxt(fc)
    costuri=numpy.genfromtxt(fcost)

    # BALANSARE AUTOMATA
    oferta, cerere, costuri = balansare(oferta, cerere, costuri)

    n=len(oferta)*len(cerere)

    pop=gen_pop(dim,oferta,cerere,costuri)
    v=[min(1000./pop[:,-1])]

    ok=True
    t=0
    while t<nmax and ok:
        sp,vp = SUS(pop[:,:-1],pop[:,-1],dim,n+1)
        parinti=numpy.zeros([dim,n+1])
        parinti[:,:-1]=sp.copy()
        parinti[:,-1]=vp.copy()

        desc = recombinare(parinti, pr, oferta,cerere,costuri)
        descm = mutatie(desc, pm, oferta,cerere,costuri)

        popn,valn = elitism(pop[:,:-1],pop[:,-1],descm[:,:-1],descm[:,-1],dim)

        pop = numpy.zeros([dim, n + 1])
        pop[:, :-1] = popn.copy()
        pop[:, -1] = valn.copy()

        vmax = min(1000./pop[:,-1])
        i = numpy.argmin(pop[:, -1])
        best = pop[i][:-1]

        v.append(vmax)
        t+=1
        ok=max(pop[:,-1])!=min(pop[:,-1])

    print("Cel mai bun cost gasit: ",vmax)
    print("Solutia de transport:")

    sol=gen_alocare(best,oferta,cerere)
    print(sol)

    grafic.plot(v)
    grafic.title("PROBLEMA DE TRANSPORT - GA (NEBALANSATA)")
    grafic.xlabel("Generatia")
    grafic.ylabel("Costul minim")
    grafic.show()

    verificare(sol,oferta,cerere)
    return (sol,vmax)


def f_obiectiv(x,oferta,cerere,costuri):
    a=gen_alocare(x,oferta,cerere)
    c=1000./numpy.sum(a*costuri)
    return c


def gen_alocare(permutare,oferta,cerere):
    m=len(oferta)
    n=len(cerere)
    x=numpy.zeros((m,n))

    i=0
    OR=sum(oferta)

    o_r=oferta.copy()
    c_r=cerere.copy()

    while OR>0:
        lin,col=numpy.unravel_index(int(permutare[i]),(m,n))

        x[lin,col]=min([o_r[lin],c_r[col]])
        o_r[lin]-=x[lin,col]
        c_r[col]-=x[lin,col]
        OR-=x[lin,col]

        i+=1

    return x


def gen_pop(dim,oferta,cerere,costuri):
    m=len(oferta)
    n=len(cerere)

    pop=numpy.zeros((dim,m*n+1))

    for i in range(dim):
        x=numpy.random.permutation(m*n)
        pop[i,:-1]=x
        pop[i,-1]=f_obiectiv(x,oferta,cerere,costuri)

    return(pop)


def recombinare(parinti,pr,oferta,cerere,costuri):
    dim,n=numpy.shape(parinti)
    desc=parinti.copy()

    perechi=numpy.random.permutation(dim)

    for i in range(0,dim,2):
        x = parinti[perechi[i], :n - 1]
        y = parinti[perechi[i + 1], :n - 1]

        r=numpy.random.uniform(0,1)

        if r<=pr:
            d1, d2 = crossover_CX(x, y, n-1)

            desc[i, :n - 1] = d1
            desc[i][n - 1] = f_obiectiv(d1, oferta,cerere,costuri)

            desc[i + 1, :n - 1] = d2
            desc[i + 1][n - 1] = f_obiectiv(d2, oferta,cerere,costuri)

    return desc


def mutatie(desc,pm,oferta,cerere,costuri):
    dim,n=numpy.shape(desc)
    descm=desc.copy()

    for i in range(dim):
        x=descm[i,:n-1]
        r=numpy.random.uniform(0,1)

        if r<=pm:
            y=m_perm_interschimbare(x,n-1)
            descm[i,:n-1]=y
            descm[i,n-1]=f_obiectiv(y,oferta,cerere,costuri)

    return descm


def verificare(sol,oferta,cerere):
    o_r=oferta-numpy.sum(sol,axis=1)
    c_r=cerere-numpy.sum(sol,axis=0)

    print("Oferta ramasa:", o_r)
    print("Cerere ramasa:", c_r)


# APEL
s,c=GA_Transport('T_oferta.txt','T_cerere.txt','T_Costuri.txt',250,300,0.85,0.2)