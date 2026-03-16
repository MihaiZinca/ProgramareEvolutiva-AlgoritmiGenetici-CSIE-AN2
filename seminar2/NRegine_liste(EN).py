# for generation using lists (not ndarray)
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

## HC for a single initial point
def HC(n):
    # generate permutation
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

# solving the problem – HC called k times, for k initial points
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
    print("Computed maximum ",v_max," for selection ",p_max)
    arata(p_max,v_max)
    return p_max,v_max,Puncte,Valori

def arata(sol,val):
    # visualization of queens placement on the chessboard

    # I: sol - the permutation defining the placement
    #    v - the vector with the best quality at each run
    # E: -

    n=len(sol)
    minim=n*(n-1)/2-val
    t1="Quality evolution (best individual from each generation).\nResult "
    t2="Best queens placement found.\nResult "
    t4="is optimal (" + str(minim) + " vs 0" + ")"
    if minim>0:
        t3="is not "
    else:
        t3=""
    # title1=f'{t1}{t3}{t4}'
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
