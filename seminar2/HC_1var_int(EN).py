import numpy
from math import sin, cos
import matplotlib.pyplot as grafic


def f_obiectiv(x):
    # an objective function to maximize, with multiple local maxima points

    # I: x - the point where the function value is computed
    # E: y - the value of the function at point x

    # an arbitrary function with local extrema

    # x**3  - x to the power of 3
    y = x**3 * sin(x/3) + x**3 * cos(2*x) -2*x*sin(3*x) + 2*x*cos(x)

    return y

def vecini(x, nr, pas, a, b):
    # computes the neighbors of a point (on an axis), together with their qualities

    # I: x - current point
    #    nr - number of neighbors in each direction
    #    pas - distance between consecutive neighbors
    #    a, b - endpoints of the working interval
    # E: v - list of neighbors (2 rows: points, qualities)

    # list comprehensions are used

    vec=[x+i*pas for i in range(-nr, nr+1) if ((x+i*pas>=a) and (x+i*pas<=b))]
    valv=[f_obiectiv(x+i*pas) for i in range(-nr, nr+1) if ((x+i*pas>=a) and (x+i*pas<=b))]
    return [vec,valv]


def HC(a, b, nrp, nrv, pas):
    # hill climbing implementation for finding the maximum of a single-variable function

    # I: a, b - endpoints of the interval where the function is defined (an axis)
    #    nrp - number of initial points used by the algorithm
    #    nrv - number of neighbors in each direction used (total 2*nrv+1 - 1 is the current point)
    #    pas - distance between two consecutive neighbors
    # E: x - maximum point
    #    fx - maximum value of the function (at point x)
    # Note: if the plot window is not closed after running an example, then when running the next example
    #    the new plot will be drawn on top of the previous one

    # initialize empty coordinate lists
    X=[None]*nrp
    Y=[None]*nrp
    # for each initial point
    for i in range(nrp):
        # apply hill climbing for the current randomly generated starting point
        pc=numpy.random.uniform(a,b)    # choose a random starting point
        local=0                         # we have not reached a local maximum
        while not local:
            # compute the neighbors of the current point and the corresponding function values
            nvec, nval=vecini(pc,nrv,pas,a,b)
            valmax=max(nval)
            poz=nval.index(valmax)
            vecmax=nvec[poz]
            # replace the current point with the best neighbor, if a better one exists
            if valmax>f_obiectiv(pc):
                pc=vecmax
            else:
                # no better neighbor, which means we reached a local maximum
                local=1
        # store the best point found and the corresponding function value
        X[i]=vecmax
        Y[i]=f_obiectiv(vecmax)

    # determine the best among the final points and the corresponding objective function value
    fx=max(Y)
    poz=Y.index(fx)
    x=X[poz]

    # display results and the plot (if you know how to plot the graph)
    print("Computed maximum value: ", fx)
    print("It is reached at point: ", x)
    deseneaza(a, b, X, Y, x, fx)
    return x,fx


def deseneaza(a, b, X, Y, xmax, ymax):
    # results visualization for 1-variable hill climbing

    # I: a, b - endpoints of the working interval
    #    X, Y - lists with the coordinates of the computed final points
    #    xmax, ymax - coordinates of the best point found
    # E: -

    x=numpy.arange(a,b,0.01)
    grafic.plot(x,[f_obiectiv(i) for i in x],'k-')
    grafic.plot(X,Y,'bo',label='local optimum')
    grafic.plot(xmax,ymax,'r*',label='best computed')
    grafic.title("Graph of function f")
    grafic.legend()
    grafic.show()



if __name__=="__main__":
    x, fx = HC(0, 50, 100, 100, 0.01)
