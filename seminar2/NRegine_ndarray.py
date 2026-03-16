import numpy as np
import matplotlib.pyplot as grafic

def f_ob(p):
    n=p.size
    calitate=n*(n-1)/2
    for i in range(n-1):
        for j in range(i+1,n):
            if abs(i-j)==abs(p[i]-p[j]):
                calitate-=1
    return calitate

def vecini(p):
    n=p.size
    Vecini_p=np.zeros([round(n*(n-1)/2),n],dtype='int')
    Calitati_vecini_p=np.zeros(round(n*(n-1)/2),dtype='int')
    #vecinii sunt toate transpozitiile lui p
    for i in range(n-1):
        for j in range(i+1,n):
            v=p.copy()
            v[i],v[j]=p[j],p[i]
            Vecini_p[i]=v
            Calitati_vecini_p[i]=f_ob(v)
    return Vecini_p, Calitati_vecini_p

## HC pentru un punct initial
def HC(n):
    s=np.random.permutation(n)
    v_s=f_ob(s)
    local=False
    while not local:
        Vecini,Calitati=vecini(s)
        index=np.argmax(Calitati)
        if v_s<Calitati[index]:
            s=Vecini[index].copy()
            v_s=Calitati[index]
        else:
            local=True
    return s,v_s

# rezolvarea problemei - HC apelat de k ori, pentru k puncte initiale
def apel_HC(n,k):
    Puncte=np.zeros([k,n],dtype="int")
    Valori=np.zeros(k,dtype="int")
    for i in range(k):
        x,v_t=HC(n)
        Puncte[i]=x.copy()
        Valori[i]=v_t
    v_max=Valori.max()
    p_max=Puncte[np.argmax(Valori)]
    print("Maximul calculat ",v_max," la alegerea ",p_max)
    arata(p_max,v_max)
    return p_max,v_max,Puncte,Valori


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
    sol,val,P,C=apel_HC(8,200)




