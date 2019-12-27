
import re
import ctypes
from ctypes import *
so_file = "./affichage.so"
affichage = CDLL(so_file)

#print(type(affichage.affiche))

## QUESTION 1
##RAPPEL : plus le score est haut, plus l'alignement est mauvais et le plagiat ne sera pas avéré
def Del():
    return 1#Ici, on pénalise de 1 point la fonction DEL utlisée dans String Edit (en gros c'est juste un malus)

def Ins():#Pareil que pour DEl
    return 1

def Sub(x,y):#Ici si les lettres correspondent, on ne pénalise pas, sinon on pénalise de 1 point
    if(x==y):
        return 0
    return 1

##fonction qui permet de calculer le score d'alignement, stock dans une matrice le score d'alignement de seqAi,seqBj

def score_alignement_opti(seqA,seqB):#prends en entrée les deux séquences
    tailleA = len(seqA)+1 #on va créer deux nouvelles séquences (les étirements), de la taille de la séquence A +1 (car la première valeur dans la matrice)
    tailleB = len(seqB)+1#pareil qu'au dessus
    t = [[0 for x in range(tailleB)]for y in range(tailleA)] #on initialise les deux séquences

#algo string edit
    for i in range(1,tailleA):
        t[i][0] = t[i-1][0] + Del()

    for j in range(1,tailleB):
        t[0][j]= t[0][j-1] + Ins()

    for i in range(1,tailleA):
        for j in range(1,tailleB):
            v1 = t[i][j-1] + Ins()
            v2 = t[i-1][j] + Del()
            v3 = t[i-1][j-1] + Sub(seqA[i-1],seqB[j-1])
            t[i][j] = min(v1,v2,v3)#on prends bien le score minimum des 3 (car on cherche à minimiser ce score)
            if(t[i][j]<0):#score négatif n'existe pas
                t[i][j] = 0
    return t#retourne la matrice qu'on utilisera à la question 2


#test = score_alignement_opti("abbacb","cbbbacab")#test pour check que ça marche

#print(test[-1][-1])#résultat attendu
#print(test)


##QUESTIOn 2
#on a la matrice t via la fonction précédente

#On va remonter la matrice précédent en prenant les scores minimaux à chaque fois pour reconstuire les alignements optimaux
def retourne_indices(i_actuel,j_actuel,t):#prends les indices actuels et la matrice

#fonction de complexité constante

##on va regarder le score minimal des 3 possiblités qu'on a lorqu'on part de la fin puis on continue
    if(t[i_actuel - 1 ][j_actuel]<t[i_actuel][j_actuel-1] and t[i_actuel - 1 ][j_actuel]<t[i_actuel-1][j_actuel-1] ):
        i_actuel = i_actuel-1
        return i_actuel,j_actuel#retourne les nouveaux indices à prendre

    elif(t[i_actuel ][j_actuel - 1]<t[i_actuel-1][j_actuel] and t[i_actuel][j_actuel-1]<t[i_actuel-1][j_actuel-1] ):
        j_actuel= j_actuel-1
        return i_actuel,j_actuel#retourne les nouveaux indices à prendre

    elif(t[i_actuel - 1 ][j_actuel-1]<t[i_actuel][j_actuel-1] and t[i_actuel - 1 ][j_actuel-1]<t[i_actuel-1][j_actuel] ):
        i_actuel= i_actuel-1
        j_actuel = j_actuel -1
        return i_actuel,j_actuel#retourne les nouveaux indices à prendre
#si on a des scores minimums égaux on prends la diagonale car je ne sais pas comment faire pour aller voir les horizons suivants en O(n) - Piste d'amélioration : récursivité
    else:
        i_actuel= i_actuel-1
        j_actuel = j_actuel -1
        return i_actuel,j_actuel#retourne les nouveaux indices à prendre

#permettra d'inverser une liste pour la prochaine fonction
def inverse_tab(t):
    t_p = [t[-i] for i in range(1,len(t)+1)]
    return t_p



#fonction de "backtracking" des alignements optimaux

def alignements_optimaux(seqA,seqB):#prends les deux séquences de base
    if(len(seqA)>len(seqB)):
        seq_a_p = seqA
        seqA = seqB
        seqB = seq_a_p
    seqA_p = []#on crée les liste qui nous serviront à stocker les alignements optimaux
    seqB_p = []

    i=len(seqA)#on part de la case de la matrice tout en bas à droite (en gros là où il y a le score optimale pour les deux séquences entières)
    j=len(seqB)#
    i_p=0#ici seront stockés les indices suivants qui seront calculés avec la fonction précédente
    j_p=0

    t = score_alignement_opti(seqA,seqB) #on calcule la matrice des scores d'alignement et on la stocke dans t
    #print("t : ",t)
    while(i!=0 and j !=0):#tant qu'on est pas revenu au point de départ de la matrice (en haut à gauche i=0 etj =0)
        i_p,j_p = retourne_indices(i,j,t)#on stocke ici les indices suivants où il y a le score d'alignement minimal
        #print("i-p : ",i_p)
        #print("j_p : ",j_p)


        if(i_p-i==-1 and j_p-j==-1):##Si la différence des deux indices vaut -1 (ou 1 dans l'autre sens), c'est qu'il faut remonter en diagonale
            seqA_p.append(seqA[i_p])#on mets dans les alignements optimaux les 2 caractères des séquences de base (car remontée en diagonale)
            seqB_p.append(seqB[j_p])
            i=i-1 #on décrémente bien les deux indices pour le calcul des prochains
            j=j-1

        elif(i_p-i==-1 and j_p-j==0):#si le prochain score minimal est sur la gauche (il n'y a que i qui change)
            seqA_p.append(seqA[i_p])#on mets dans l'alignement optimal de A la valeur correspondante de la séquence A
            seqB_p.append("_")#pour l'alignement opti de B on mets un tiret (ou un vide quoi)
            i=i-1#il n'y a que i qui bouge pour le prochain calcul des indices du score minimal

#meme principe qu'au dessus mais avec j
        elif(i_p-i==0 and j_p-j==-1):#faudrait mettre un else pour que ce soit opti mais on voit mieux le principe comme ça
            seqA_p.append("_")
            seqB_p.append(seqB[j_p])
            j=j-1
        else:#ne doit jamais arriver car les autres cas couvrent l'ensemble des possibilités mais on sait jamais
            print("i_p : ",i_p)
            print("i : ",i)
            print("j_p : ",j_p)
            print("j : ",j)

    return inverse_tab(seqA_p),inverse_tab(seqB_p)#retourne les deux alignements optimaux (MAIS A L ENVERS VU QU ON PART DE LA FIN DE LA MATRICE), donc on les inverse

def read_text(file):
    f = open(file,"r")
    return f.read()

#print(type(read_text("texte1.txt")))
text1 = read_text("texte1.txt")
text2 = read_text("texte2.txt")
#text1=re.sub('[\W_]+', '',text1)
#text2=re.sub('[\W_]+', '',text2)

#text2=regex.sub(text2, 'ab3d*E')

#print(text1)

a,b = alignements_optimaux("Source wiki, un étudiant a essayé de tricjer c'est vraiment bizarre","Source prof un étudiant a essayé de tricher ça ne m'étonne pas")#marche sur ce test
#e,f = alignements_optimaux(text1,text2)
c,d = alignements_optimaux("abbacb","cbbbacab")

#print(a)#donne bien deux alignements optimaux car seuls 3 caractères sont dépareillésé
#print(b)
#print(c)
#print(d)
#affichage.affiche2.argtypes = [c_wchar_p,c_wchar_p, c_int] # (all defined by ctypes)
#affichage.affiche.argtypes = [c_wchar_p,c_wchar_p, c_int] # (all defined by ctypes)

t1 ="test"
t2 = "test2"
affichage.affiche(str(a),str(b),6)
affichage.affiche((ctypes.c_wchar * len(a))(*a),(ctypes.c_wchar * len(b))(*b),c_int(6))

affichage.affiche2(str(a),str(b),6)
#print(e)
#print(f)
