#pentru generare in liste (nu ndarray)
import random
import matplotlib.pyplot as grafic

def f_ob(p):
    n=len(p)
    nr_poz_corecte=n*(n-1)/2
    for i in range(n-1):
        for j in range(i+1,n):
            if abs(i-j)==abs(p[i]-p[j]):
                nr_poz_corecte-=1
    return nr_poz_corecte


def vecini(p):
    n=len(p)
    Vecini_p=[]
    Calitati_vecini_p=[]
    for i in range(n-1):
        for j in range(i+1,n):
            x=p.copy()
            x[i],x[j]=p[j],p[i]
            Vecini_p.append(x)
            Calitati_vecini_p.append(f_ob(x))
    return Vecini_p, Calitati_vecini_p

## HC pentru un punct initial
def HC(n):
    #generare permutare
    s=random.sample(range(n),n)
    v_s=f_ob(s)
    local=False
    while not local:
        Vecini,Calitati=vecini(s)
        index=max(range(len(Calitati)), key=lambda i: Calitati[i])
        if v_s<Calitati[index]:
            s=Vecini[index].copy()
            v_s=Calitati[index]
        else:
            local=True
    return s,v_s

# rezolvarea problemei - HC apelat de k ori, pentru k puncte initiale
def apel_HC(n,k):
    Puncte=[]
    Valori=[]
    for i in range(k):
        x,v_t=HC(n)
        Puncte.append(x)
        Valori.append(v_t)
    v_max=max(Valori)
    index = max(range(len(Valori)), key=lambda i: Valori[i])
    p_max=Puncte[index]
    print("Maximul calculat ",v_max," la alegerea ",p_max)
    arata(p_max,v_max)
    return p_max,v_max,Puncte,Valori

def arata(sol,val):
    # vizualizare asezare regine pe tabla de sah

    # I: sol - permutarea care defineste asezarea
    #    v - vectorul cu cea mai buna calitate la fiecare apel
    # E: -

    n=len(sol)
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




