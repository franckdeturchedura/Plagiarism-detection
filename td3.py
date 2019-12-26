
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
        return i_actuel,j_actuel#retourne les nouveaux indices à prendre

    if(t[i_actuel ][j_actuel - 1]<t[i_actuel-1][j_actuel] and t[i_actuel][j_actuel-1]<t[i_actuel-1][j_actuel-1] ):
        j_actuel= j_actuel-1
        return i_actuel,j_actuel#retourne les nouveaux indices à prendre

    if(t[i_actuel - 1 ][j_actuel-1]<t[i_actuel][j_actuel-1] and t[i_actuel - 1 ][j_actuel-1]<t[i_actuel-1][j_actuel] ):
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
        seqB = seqA
        seqA = seq_a_p
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
            print("ah")


    return inverse_tab(seqA_p),inverse_tab(seqB_p)#retourne les deux alignements optimaux (MAIS A L ENVERS VU QU ON PART DE LA FIN DE LA MATRICE), donc on les inverse



#a,b = alignements_optimaux("Source Wikipedia modifie par un etudiant du cours IT-4301E, traitement algorithmique de l information. La distance de d editon est une distance au sens mathematique donnant une mesure de la similarite entre deux sequences. Elle est egale au nombre minimal de caracteres qu il faut supprimer, inserer ou substituer pour passer d une sequence a l autre. Elle a ete proposee par Vladimir Levenshtein en 1965. Elle est ainsi egalement connue sous les noms de distance de Levenshtein ou de distance de deformation dynamique temporelle dans le domaine de la reconnaissance de formes. Cette distance est est une fonction croissante du nombre de differences entre les deux sequences. La distance d edition peut etre consideree comme une generalisation de la distance de Hamming (donnee par le nombre de position en lesquelles les deux sequences possedent des caracteres differents). On peut montrer en particulier que la distance de Hamming est un majorant de la distance d edition.Definition formelle : on appelle distance d edition entre deux mots M et P le cout minimal transformer M en P en effectuant les operations elementaires, dites d edition, suivantes : i) substitution d un caractere de M par un caractere de P ; ii) insertion dans M d un caractere de P ; iii) suppression (ou deletion) d un caractere de M. On associe ainsi a chacune de ces operations un cout. On choisit souvent un cout egal a 1 pour toutes les operations excepte la substitution de caracteres identiques qui a un cout nul.Exemples : si M = 'examen' et P = 'examen', alors Lev(M, P) = 0 parce qu aucune operation n a ete realisee. Si M = 'examen' et P = 'examan', alors Lev(M, P) = 1, parce qu il y a eu une substitution (changement du e en a), et que l on ne peut pas en faire une transformation de M en P avec un moindre cout.","Source Wikipedia. La distance de Levenshtein une distance mathematique donnant une mesure de la similarite entre deux chaines de caracteres. Elle est egale au nombre minimal de caracteres qu il faut supprimer, inserer ou remplacer pour passer d une chaine a l autre. Elle a ete proposee par Vladimir Levenshtein en 1965. Elle est egalement connue sous les noms de distance d edition ou de deformation dynamique temporelle, notamment en reconnaissance de formes et particulierement en reconnaissance vocale1,2.Cette distance est d autant plus grande que le nombre de differences entre les deux chaines est grand. La distance de Levenshtein peut etre consideree comme une generalisation de la distance de Hamming. On peut montrer en particulier que la distance de Hamming est un majorant de la distance de Levenshtein.Definition : on appelle distance de Levenshtein entre deux mots M et P le cout minimal pour aller de M a P en effectuant les operations elementaires suivantes : i) substitution d un caractere de M en un caractere de P ; ii) ajout dans M d un caractere de P ; iii) suppression d un caractere de M. On associe ainsi a chacune de ces operations un cout. Le cout est toujours egal a 1, sauf dans le cas d une substitution de caracteres identiques. Exemples : si M = 'examen' et P = 'examen', alors LD (M, P) = 0, parce qu aucune operation n a ete realisee. Si M = 'examen' et P = 'examan', alors LD (M, P) = 1, parce qu il y a eu un remplacement (changement du e en a), et que l on ne peut pas en faire moins.")#marche sur ce test

c,d = alignements_optimaux("abbacb","cbbbacab")

#print(a)#donne bien deux alignements optimaux car seuls 3 caractères sont dépareillésé
#print(b)
print(c)
print(d)
