# script pentru testul selectiei parintilor - selectia de tip SUS cu distributie fps cu sigma-scalare
import numpy as np
from FunctiiSelectii import *

import generare_init as gi
import matplotlib.pyplot as grafic


#generarea aleatoare a unei populatii
dim=12
c=np.genfromtxt("costuri.txt")

p,v=gi.gen(c,dim)
# calculul parintilor si calitatii acestora utilizand selectia SUS cu FPS cu sigma-scalare
parinti,valori=SUS(p,v,dim,c.shape[0])


x=range(dim)
grafic.plot(x,v,"go",markersize=16,label='Calitatile populatiei curente')
grafic.plot(x,valori,"ro",markersize=10,label='Calitatile parintilor')
grafic.legend()
grafic.show()