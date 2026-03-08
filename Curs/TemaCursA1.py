buget_max=5000

costuri=[100,60,50]
autonomii=[6000,4200,2800]
vizibilitati=[1500,2400,1600]

autonomie_max=0
sol=(0,0,0)

def bt(a,b,c):
    global autonomie_max,sol

    cost_total=a * costuri[0] + b * costuri[1] + c * costuri[2]

    if cost_total > buget_max:
        return

    total_avioane=a+b+c

    if total_avioane > 0:

        autonomie_medie=(a*autonomii[0]+b*autonomii[1]+c*autonomii[2])/total_avioane
        vizibilitate_medie=(a*vizibilitati[0]+b*vizibilitati[1]+c*vizibilitati[2])/total_avioane

        if vizibilitate_medie>2000:
            if autonomie_medie>autonomie_max:
                autonomie_max=autonomie_medie
                sol=(a,b,c)

    bt(a+1,b,c)
    bt(a,b+1,c)
    bt(a,b,c+1)

bt(0,0,0)

print("Cea mai buna solutie gasita:")
print("I:",sol[0])
print("II:",sol[1])
print("III:",sol[2])
print("Autonomie medie maxima:",autonomie_max)