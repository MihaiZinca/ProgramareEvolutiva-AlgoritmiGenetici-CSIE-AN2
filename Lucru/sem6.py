# from functools import total_ordering
# from lib2to3.fixes.fix_tuple_params import simplify_args
#
# CROSSOVER
#
# pc>0,5   0,6; 0,7
#
# 1.Binar/Int
#
# a) crossover unipunct -> il facem in momentul in care nu avem nicio dependenta intre gene
#
# x=[1 1 1 1 1]
# y=[0 0 0 0 0]
# aleator un i
#
# ex i=2
# c1= [1 1 0 0 0 ] primele 2 din x si dupa din y
# c2= [0 0 1 1 1]
#
# b) crossover uniform -> il folosim la problemele de selectie(de ex rucsac)
# r apartine{0,1} ->0 =>nu fac nimic
#                 ->1 =>interschimb valoriile
#
# x=[1 1 1 1]         c1=[1 0 1 0]
# y=[0 0 0 0]   =>    c2=[0 1 0 1]
# r=[0 1 0 1]
#
# 2.Permutari
#
# a) PMX  ->problemele de selectie si pozitile sunt importante(N regine, de ex:
# pozitia in calendar sa nu se intersecteze)
# x=[1 2  :3 4 5 6:  7 8]
# y=[5 6  :7 8 1 2:  3 4]
#
# trebuie sa alegem 2 poz random
# p1=2        p2=6
#
# c=[7 8 3 4 5 6 1 2]
#
#
# b)OCX -> ne interseaza ORDINEA, nu neap poz exacta(
# x=[1 2  :3 4 5 6:  7 8]
# y=[5 6  :7 8 1 2:  3 4]
#
# p1=2 p2=6
#
# 1) c=[_ _ 3 4 5 6 _ _]
# 2) elimin din y 3 4 5 6 => ramanem cu 7 8 1 2
# => c=[1 2 3 4 5 6 7 8]
# invers practic de la p2+1 -> n-1  si 0 -> p1-1
#
#
# c)CX - se bazeaza pe cicluri
# -> f putin foosit, mai mult de pastrarea relatiilor dintre poz
#
# index: 0 1 2.....7
# x=[1 2 3 4 5 6 7 8]
# y=[2 1 4 3 6 5 7 8]
#
# incercam sa construim ciclu1
# c1=poz(0,1)
# c2=poz(2,3)
# c3=poz(4,5)
# c4=poz(6)
# c5=poz(7)
#
# daca nr cicluri(c1-impar,c2-par...) este impar => iau din x
#                                            altfel iau din y
#
# => c=[1 2 4 3 5 6 7 8]
#
# d)ECX - ne interseaza vecinii
# x=[1 2 3 4 5]
# y=[1 3 5 4 2]
#
# n=5
# Cautam vecinii pt fiecare nr in ordine crescatoare
# 1) Pt 1:
# x={2,5}    => 1->{2,3,5} (are vecinii)
# y={3,2}
#
# 2)Pt 2:
# x={1,3}   => 2->{1,3,4}
# y={4,1}
#
# 3)Pt 3:
# x={2,4}  => 3->{1,2,4,5}
# y={1,5}
#
# 4)Pt 4:
# x={3,5}  => 4->{2,3,5}
# y={5,2}
#
# 5)Pt 5:
# x={1,4}  => 5->{1,3,4}
# y={3,4}
#
#
# 1) c=[1 _ _ _ _]
# 1 se regasete in vecinii: 2,3,5
# 2=are 3 vecini
# 3= are 4 vecini  => alegem acel nr care are cei mai putini vecini adica 2 SAU 5
# 5= are 3 vecini
# stergem 1 din toate listele
#
# 2)Alegem 2
# c=[1 2 _ _ _]
# stergem 2 din toate listele!
# vecinii lui 2:{1,3,4} => {3,4}
# 3 -> 2 vecini:{4,5}
# 4->2 vecini:{3,5}    => alegem pe cel care are cei mai putini vecini 3 SAU 4
#
# 3)Alegem 4
# c=[1 2 4 _ _ ]
#
# stergem pe 4 din toate listele
# vecimnii lui 4:{3,5}
# 3-> 1 vecin {5}
# 5-> 1 vecin{3}   => alegem pe 3 sau 5 => alegem 3 => c=[1 2 4 3 5]
#
#
#
# 3) NR REALE
#
# a) crossover singular
#  alegem random o pozitie i ->Medie ponderata
#
# b) crossover simplu
#     i
#     j-> i->n-1   => Medie ponderata
#
# c) crossover total
#  Medie ponderata pe toate genele
#
#
