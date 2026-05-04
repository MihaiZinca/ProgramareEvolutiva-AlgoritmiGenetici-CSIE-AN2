# script pentru testul selectiei parintilor - selectia de tip ruleta cu distributie fps cu sigma-scalare
import numpy as np

import generare_init as gi
import matplotlib.pyplot as grafic

def calcul_prob_sigma_scalare(calitati):
    dimensiune=calitati.size
    prob=calitati/sum(calitati)
    medie=np.mean(calitati)
    dev=np.std(calitati)
    calitati_sigma=np.array([max(calitati[i]-(medie-2*dev),0) for i in range(dimensiune)])
    if sum(calitati_sigma)==0:
        p=prob.copy()
    else:
        sigma_prob = calitati_sigma / sum(calitati_sigma)

        p=sigma_prob.copy()
    cumulat=p.copy()
    for i in range(1,dimensiune):
        cumulat[i]=cumulat[i-1]+p[i]
    return cumulat

def ruleta(populatie,calitati,dimensiune,n):
    Parinti=populatie.copy()
    Calitati_parinti=calitati.copy()
    cumulat=calcul_prob_sigma_scalare(calitati)
    for i in range(dimensiune):
        r=np.random.uniform(0,1)
        poz=np.where(cumulat>=r)
        selectat=poz[0][0]
        Parinti[i]=populatie[selectat].copy()
        Calitati_parinti[i]=calitati[selectat]
    return Parinti,Calitati_parinti


#generarea aleatoare a unei populatii
dim=8
n=10
p=gi.gen(n,dim)
#populatia p este impartita in matricea indivizilor si vectorul calitatilor
# calculul parintilor si calitatii acestora utilizand selectia ruleta cu FPS cu sigma scalare
parinti,valori=ruleta(p[:,:n],p[:,n],dim,n)
#constituirea populatiei rezultate
rez=np.zeros([dim,n+1],dtype='int')
rez[:,:n]=parinti.copy()
rez[:,n]=valori.copy()
print("Populatia considerata curenta")
print(p)
print("Populatia de parinti")
print(rez)


x=[i for i in range(dim)]
grafic.plot(x,p[:,n],"go",markersize=16,label='Calitatile populatiei curente')
grafic.plot(x,rez[:,n],"ro",markersize=10,label='Calitatile parintilor')
grafic.legend()
grafic.show()

