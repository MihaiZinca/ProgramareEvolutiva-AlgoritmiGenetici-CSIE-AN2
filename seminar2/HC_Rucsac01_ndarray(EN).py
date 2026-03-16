import numpy as np

# implementation using vectors/matrices – ndarray

# checks the feasibility of choosing x and also computes the objective function
def ok(x,c,v,max):
    cost=np.dot(x,c)
    val=np.dot(x,v)
    return cost<=max,val

# computation of neighbors of the current point – via bit flip, ensuring feasibility
def vecini(x,c,v,max):
    # creating vectors with 0 components
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


## HILL CLIMBING ALGORITHM FOR SOLVING THE 0–1 KNAPSACK PROBLEM
# I: fc, fv – files containing costs/values
#    dim – number of starting points – how many times we run hill climbing
#    max – maximum capacity of the knapsack
#
# E: sol – computed solution
#    val – maximum fitness function value

def HC(fc,fv,dim,max):
    # reading data
    c = np.genfromtxt(fc)
    v = np.genfromtxt(fv)
    # n = problem size
    n = c.size
    puncte=np.zeros([dim,n],dtype="int")
    calitati=np.zeros(dim,dtype="float")
    for apeluri in range(dim):
        # generate the initial point
        local=False
        gata = False
        while gata == False:
            # generate candidate x with elements 0, 1
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
    print("Best computed value: ", vmax)
    print("Corresponding selection is: ", sol)
    return sol,vmax,puncte,calitati

# Console calls
# import HC_Rucsac01_ndarray as r1
# sol,val,P,C=r1.HC("cost.txt","value.txt",70,50)   # – max 81
# sol,val,P,C=r1.HC("cost1.txt","value1.txt",90,50) # – max 108
# sol,val,P,C=r1.HC("cost2.txt","value2.txt",1000,56.6) # – max 128.2

# executable code
if __name__=="__main__":
    sol, val, P, C = HC("cost.txt", "valoare.txt", 70, 50)
    sol1, val1, P1, C1 = HC("cost1.txt", "valoare1.txt", 90, 50)
    sol2, val2, P2, C2 = HC("cost2.txt", "valoare2.txt", 1000, 56.6)
