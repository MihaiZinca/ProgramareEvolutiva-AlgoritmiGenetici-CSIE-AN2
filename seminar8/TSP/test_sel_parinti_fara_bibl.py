# script pentru testul selectiei parintilor - selectia de tip SUS cu distributie fps cu sigma-scalare
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

def SUS(pop,qual,dim):
    spop=pop.copy()
    squal=np.zeros(dim)
    qfps=calcul_prob_sigma_scalare(qual)
    r=np.random.uniform(0,1/dim)
    k,i=0,0
    while (k<dim):
        while (r<=qfps[i]):
            spop[k]=pop[i].copy()
            squal[k]=qual[i]
            r=r+1/dim
            k=k+1
        i=i+1
    return spop, squal


#generarea aleatoare a unei populatii
dim=12
c=np.genfromtxt("costuri.txt")

p,v=gi.gen(c,dim)
# calculul parintilor si calitatii acestora utilizand selectia SUS cu FPS cu sigma-scalare
parinti,valori=SUS(p,v,dim)

# print(p)
# print(parinti)

print(f"Calitatile in populatia curenta {v}")
print(f"Calitatile in populatia parintilor {valori}")

grafic.plot(v,"go",markersize=16,label='Calitatile populatiei curente')
grafic.plot(valori,"ro",markersize=10,label='Calitatile parintilor')
grafic.legend()
grafic.show()