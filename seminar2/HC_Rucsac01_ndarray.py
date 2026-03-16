import numpy as np

#implementarea cu vectori/matrice - ndarray

#verifica fezabilitatea alegerii x si calculeaza si f. obiectiv
def ok(x,c,v,max):
    cost=np.dot(x,c)
    val=np.dot(x,v)
    return cost<=max,val

#calculul vecinilor punctului curent - prin bitflip si astfel incat este fezabil
def vecini(x,c,v,max):
    #crearea unor vectori cu 0 componente
    n=x.size
    Vec=np.zeros(0,dtype="int")
    Cal=np.zeros(0,dtype="float")
    for i in range(n):
        y=x.copy()
        y[i]=not x[i]
        fez,val=ok(y,c,v,max)
        if fez:
            Vec=np.append(Vec,y)
            Cal=np.append(Cal,val)
    dim=len(Vec)
    Vec=Vec.reshape(round(dim/n),n)
    return Vec, Cal


##ALGORITMUL HILL CLIMBING PENTRU REZOLVAREA PROBLEMEI RUCSACULUI 0-1
#I: fc,fv - fisierele cu costuri/valori
#   dim - numărul punctelor de start - de cate ori apelam hill climbing
#   max=capacitatea maxima a rucsacului
#
#E: sol - solutia calculata
#   val - maximul functiei fitness

def HC(fc,fv,dim,max):
    #citirea datelor
    c = np.genfromtxt(fc)
    v = np.genfromtxt(fv)
    # n=dimensiunea problemei
    n = c.size
    puncte=np.zeros([dim,n],dtype="int")
    calitati=np.zeros(dim,dtype="float")
    for apeluri in range(dim):
        # genereaza punctul initial
        local=False
        gata = False
        while gata == False:
            # genereaza candidatul x cu elemente 0,1
            x = np.random.randint(0, 2, n)
            gata, val = ok(x,c, v, max)
        while not local:
            Vec,Cal=vecini(x,c,v,max)
            if Cal.size==0:
                local=True
            else:
                i = np.argmax(Cal)
                vn = Vec[i]
                if Cal.max()>val:
                    val=Cal.max()
                    x=vn
                else:
                    local=True
        puncte[apeluri] = x.copy()
        calitati[apeluri] = val

    vmax = np.max(calitati)
    i = np.argmax(calitati)
    sol=puncte[i]
    print("Cea mai buna valoare calculată: ", vmax)
    print("Alegerea corespunzatoare este: ", sol)
    return sol,vmax,puncte,calitati

#Apeluri in consola
#import HC_Rucsac01_ndarray as r1
#sol,val,P,C=r1.HC("cost.txt","valoare.txt",70,50) #- max 81
#sol,val,P,C=r1.HC("cost1.txt","valoare1.txt",90,50) #- max 108
#sol,val,P,C=r1.HC("cost2.txt","valoare2.txt",1000,56.6) #- max 128.2

#cod executabil
if __name__=="__main__":
    sol, val, P, C = HC("cost.txt", "valoare.txt", 70, 50)
    sol1, val1, P1, C1 = HC("cost1.txt", "valoare1.txt", 90, 50)
    sol2, val2, P2, C2 = HC("cost2.txt", "valoare2.txt", 1000, 56.6)