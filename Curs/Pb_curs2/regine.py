import numpy as np
from numpy.ma.core import argmax
import matplotlib.pyplot as grafic

def calitate(p):
    n=p.size
    cal_p=int(n*(n-1)/2)
    for i in range(n-1):
        for j in range(i+1,n):
            if abs(i-j)==abs(p[i]-p[j]):
                cal_p-=1
    return cal_p

def vecini(p):
    n=p.size
    vec_p=np.zeros([int(n*(n-1)/2),n],dtype="int")
    cal_p=np.zeros(int(n*(n-1)/2),dtype="int")
    contor=0
    for i in range(n-1):
        for j in range(i+1,n):
            v=p.copy()
            v[i],v[j]=p[j],p[i]
            vec_p[contor]=v.copy()
            cal_p[contor]=calitate(v)
    return vec_p, cal_p

def HC(n):
    p=np.random.permutation(n)
    cal_max=calitate(p)
    local=False
    while not local:
        V,C=vecini(p)
        index=argmax(C)
        if C[index]>cal_max:
            cal_max=C[index]
            p=V[index].copy()
        else:
            local=True
    return p, cal_max

def rezolva(n,NMAX):
    p,c=HC(n)
    for i in range(NMAX-1):
        p1,c1=HC(n)
        if c<c1:
            p=p1.copy()
            c=c1
    print('Cea mai buna solutie calculata are ', n*(n-1)/2-c,' perechi  de regine in pozitie de atac')
    print(p)
    return p,c


def arata(sol,val):
    # vizualizare asezare regine pe tabla de sah

    # I: sol - permutarea care defineste asezarea
    #    v - vectorul cu cea mai buna calitate la fiecare apel
    # E: -

    n=sol.size
    minim=n*(n-1)/2-val
    t1="Evoluția calității (cel mai bun individ din fiecare generație).\nRezultatul "
    t2="Cea mai bună așezare a reginelor găsită.\nRezultatul "
    t4="este optim (" + str(minim) + " vs 0" + ")"
    if minim>0:
        t3="nu "
    else:
        t3=""
    #titlu1=f'{t1}{t3}{t4}'
    titlu=t1+t2+t3+t4

    fig=grafic.figure()
    ax=fig.gca()
    x=[i+0.5 for i in range(n-1,-1,-1)]
    y=[sol[i]+0.5 for i in range(n)]
    grafic.plot(y,x,'r*',markersize=10)
    grafic.xticks(range(n+1))
    grafic.yticks(range(n+1))
    grafic.grid(True,which='both',color='k', linestyle='-', linewidth=1)
    ax.set_aspect('equal')
    grafic.title(titlu)
    grafic.show()


if __name__=="__main__":
    p,c=rezolva(8,50)
    arata(p,c)