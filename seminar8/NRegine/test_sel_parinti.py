# script pentru testul selectiei parintilor - selectia de tip ruleta cu distributie fps cu sigma-scalare
import numpy as np
from FunctiiSelectii import ruleta
import generare_init as gi
import matplotlib.pyplot as grafic



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


grafic.plot(p[:,n],"go",markersize=16,label='Calitatile populatiei curente')
grafic.plot(rez[:,n],"ro",markersize=10,label='Calitatile parintilor')
grafic.legend()
grafic.show()

