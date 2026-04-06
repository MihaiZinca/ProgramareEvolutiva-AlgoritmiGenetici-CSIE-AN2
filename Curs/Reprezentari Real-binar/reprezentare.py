import numpy as np
import math
#EXEMPLU - reprezentarea unui numar real printr-un sir binar, cu o precizie data

# reprezentarea numarului x din [a,b] cu eroare de maxim 10^-nrz prin reprezentarea binara a numarului natural asociat
def r_bin(x,a,b,nrz):
    m = math.ceil(np.log2((b - a) * (10 ** nrz))) + 1
    n = int((x - a) * ((2 ** m) - 1) / (b - a))
    print(n)
    #obtine reprezentarea binara a lui n in forma '0b_sir de biti' si extrage sir_biti
    t=bin(n)[2:]
    #obtine reprezentarea pe exact m biti prin completare cu 0
    rezultat=t.zfill(m)
    return rezultat

# operatia inversa celei prezentate mai sus
def r_dec(sir,a,b):
    m = len(sir)
    #obtine reprezentarea in baza 10 a sirului binar sir
    n = int(sir, 2)
    x = a + n * (b - a) / (2 ** m - 1)
    return x

if __name__=="__main__":
    L = np.random.uniform(-100, 100, 2)
    a = min(L)
    b = max(L)
    x = np.random.uniform(a, b)
    a=-3
    b=4.2
    x=2.173895
    nrz = np.random.randint(1, 10)
    nrz=3
    sir = r_bin(x, a, b, nrz)
    y = r_dec(sir, a, b)
    print("Reprezentarea lui ", x, " din [", a, b, "] cu eroare", 10 ** -nrz, " este ", sir)
    print("Aproximarea cu eroare", 10 ** -nrz, "a lui x pe baza sirului binar este ", y)
    


