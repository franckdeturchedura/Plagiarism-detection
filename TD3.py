from ctypes import CDLL, c_char_p
so_file = './affichage.so'
affichage = CDLL(so_file)
# Compilation du fichier affichage.so avec :
# gcc -shared -Wl,-soname,affichage -o affichage.so -fPIC affichage.c

def read_text(textfile):
    '''
    Permet de lire le contenu d'un fichier texte.
    '''
    with open(textfile, 'r') as f:
        text = f.read()
    return text

# Question 1 #
def Del(): return 1
def Ins(): return 1
def Sub(x, y):
    if(x==y): return 0
    return 1

def distance(A, B):
    '''
    Renvoie la table T des distances entre les préfixes des chaines A et B.
    La distance entre A et B est contenue dans T[-1][-1].
    '''
    lenA = len(A)+1
    lenB = len(B)+1

    T = [ [0 for j in range(lenB)] for i in range(lenA) ]

    for i in range(1, lenA):
        T[i][0] = T[i-1][0] + Del()

    for j in range(1, lenB):
        T[0][j] = T[0][j-1] + Ins()

    for i in range(1, lenA):
        for j in range(1, lenB):
            T[i][j] = min(
                T[i][j-1] + Ins(),
                T[i-1][j] + Del(),
                T[i-1][j-1] + Sub(A[i-1], B[j-1])
            )

    return T

# Question 2 #
def inverse_tab(tab):
    '''
    Prend en argument un tableau et le renvoie à l'envers.
    Utile pour la fonction alignements_optimaux()
    '''
    tab_inv = [ tab[-i] for i in range(1,len(tab)+1) ]
    return tab_inv

def retourne_indices(i, j, T):
    '''
    Permet de remonter le tableau T en partant de la fin
    et en empruntant un chemin de cput minimum.
    '''
    if( T[i-1][j] < T[i][j-1] and T[i-1][j] < T[i-1][j-1] ):
        i = i-1
        return i, j

    elif( T[i][j-1] < T[i-1][j] and T[i][j-1] < T[i-1][j-1] ):
        j = j-1
        return i, j

    elif(T[i-1][j-1] < T[i][j-1] and T[i-1][j-1] < T[i-1][j] ):
        i = i-1
        j = j -1
        return i, j

    else:
        i = i-1
        j = j-1
        return i, j

def alignements_optimaux(A, B):
    '''
    Renvoie un alignement optimal des strings A et B.
    '''
    A_p = []
    B_p = []

    i = len(A)
    j = len(B)
    i_p = 0
    j_p = 0

    T = distance(A, B)
    #print("T :", T)

    while(i!=0 and j!=0):
        i_p, j_p = retourne_indices(i,j,T)
        #print("i_p :", i_p)
        #print("j_p :", j_p)

        if(i_p-i == -1 and j_p-j == -1):
            A_p.append(A[i_p])
            B_p.append(B[j_p])
            i = i-1
            j = j-1

        elif(i_p-i == -1 and j_p-j == 0):
            A_p.append(A[i_p])
            B_p.append(" ")
            i = i-1

        elif(i_p-i == 0 and j_p-j == -1):
            A_p.append(" ")
            B_p.append(B[j_p])
            j = j-1
        else:
            print("i_p :", i_p)
            print("i :", i)
            print("j_p :", j_p)
            print("j :", j)

    # return "".join(inverse_tab(A_p)), "".join(inverse_tab(B_p))
    A_p.reverse()
    B_p.reverse()
    return "".join(A_p), "".join(B_p)

# Question 4 #

def in_tab(e, L):
    '''
    Renvoie True si l'élément e est dans la liste de listes L.
    '''
    for i in range(len(L)):
        if e in L[i]:
            return True
    return False



def indice_der_lettre(Seq):
    alphab = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    ind = len(Seq)
    for i in reversed(Seq):

        if i in alphab:
            return ind
        ind = ind - 1


def ind_min(SeqA,SeqB):
    ind_a = indice_der_lettre(SeqA)
    ind_b = indice_der_lettre(SeqB)
    ind_min = min(ind_a,ind_b)
    return int(ind_min)


def calcul_score(a,b):
    ind_minim = ind_min(a,b)
    a,b = a[:ind_minim],b[:ind_minim]
    print("a = ",a)
    print("b = ",b)
    print("len(b) = ",len(b))
    print("dist(a, b) = ",distance(a, b)[-1][-1])
    score1 = distance(a, b)[-1][-1]/len(b)
    print("score1 = ", score1)

    return score1

if __name__ == '__main__':
    A = 'abbacb'
    B = 'cbbbacab'

    text1 = read_text('texte1.txt')
    text2 = read_text('texte2.txt')

    text3 = read_text('t1.txt')
    text4 = read_text('t2.txt')

    #******************************************************************

    tab1 = text3[:-1].split('\n')
    tab2 = text4[:-1].split('\n') # On fait la liste des différents paragraphes
    if( len(tab1) < len(tab2) ): # On commence par parcourir le texte avec le plus de paragraphes
        tab1, tab2 = tab2, tab1

    # print("tab1 = {}\n\ntab2 = {}\n".format(tab1, tab2))

    # pairs = []
    # for p1 in tab1:

    #     dist = 9999
    #     p = tab2[0]

    #     for p2 in tab2[1:]:
    #         a, b = alignements_optimaux(p1, p2)
    #         T = distance(a, b)
    #         c = T[-1][-1]/len(a)

    #         if( c < dist ):
    #             dist = c
    #             p = p2

    #     if( not(in_tab(p1, pairs)) and not(in_tab(p, pairs)) ):
    #         pairs.append([p1, p])
    #     elif( in_tab(p1, pairs) ):
    #         pairs.append([' '*len(p), p])
    #     elif( in_tab(p, pairs) ):
    #         pairs.append([p1, ' '*len(p1)])



    # for k in pairs:
    #     t1 = c_char_p(k[0].encode('utf-8'))
    #     t2 = c_char_p(k[1].encode('utf-8'))
    #     affichage.affiche3(t2, t1, 65)
    # affichage.afficheSeparateurHorizontal(65)

    #******************************************************************

    # a, b = alignements_optimaux(text3, text4)
    # T = distance(a, b)

    # print("\nDist({}, {}) = {}\n".format(a[:15], b[:15], T[-1][-1]))

    # print(a)
    # print()
    # print(b)
    # print()

    # print("len(text1) =", len(text3), ", len(text2) =", len(text4))
    # print("len(a) =", len(a), ", len(b) =", len(b))
    # print()

    # t1 = c_char_p(a.encode('utf-8'))
    # t2 = c_char_p(b.encode('utf-8'))
    # affichage.affiche2(t1, t2, 65)

    # t1 = c_char_p(text1.encode('utf-8'))
    # t2 = c_char_p(text2.encode('utf-8'))
    # affichage.affiche(t1, t2, 65)

    # test1 = "abcd\n423\namen\n"
    # test2 = "abcE\n123\n"

    # a, b = alignements_optimaux(text3, text4)
    # a, b = alignements_optimaux(test1, test2)

    # tab1 = a[:-1].split('\n') # On fait la liste des différents paragraphes
    # tab2 = b[:-1].split('\n')

    # print("tab1 =", tab1)
    # print("tab2 =", tab2)

    # matchs = []
    # for p1 in tab1: # On parcours les paragraphes du 1er texte
    #     # print("p1 = {}".format(p1))
    #     dist = 9999
    #     p = tab2[0]
    #     for p2 in tab2: # Pour chaque p1 on parcours les paragraphes du 2nd texte
    #         # print("p2 = {}".format(p2))
    #         # a, b = alignements_optimaux(p1, p2)
    #         # print("a = {}, b = {}".format(a,b))
    #         T = distance(p1, p2)
    #         # print("dist =", T[-1][-1])
    #         if T[-1][-1] < dist : # On retient le paragraphe p2 qui est le plus proche de p1
    #             dist = T[-1][-1]
    #             p = p2
    #             # print("p = {}".format(p))
    #     matchs.append([p1, p]) # On renvoie la paire de paragrahes dans matchs
    #     # print('***********')
    # print(matchs)

    # T = distance(a, b)

    # Test de la similarité
    # s1 = 'ab'
    # s2 = 'abc'
    # a, b = alignements_optimaux(s1, s2)
    # T = distance(s1, s2)

    # simi = 1-(T[-1][-1]/len(a))
    # print()
    # print('Distance entre les textes : {}; longueur de t1.txt : {}, longueur de t2.txt : {}'.format(
    #     T[-1][-1],
    #     len(text3),
    #     len(text4)
    # ))
    # print('Score de similarité en % : {:.3f}'.format(simi*100))

    # # On affiche les paires de paragraphes ensembles
    # for k in matchs:
    #     t1 = c_char_p(k[0].encode('utf-8'))
    #     t2 = c_char_p(k[1].encode('utf-8'))
    #     affichage.affiche(t2, t1, 65)

    # Bonne méthode pour apparier
    a, b = alignements_optimaux(tab2[0], tab1[0])
    print("avec la fonction, score = ", calcul_score(a,b))

    a, b = alignements_optimaux(tab2[-1], tab1[0])
    print("avec la fonction, score = ", calcul_score(a,b))

"""    ind_min1 = ind_min(a,b)
    print("indice minimale",ind_min1)
    a,b = a[:ind_min1],b[:ind_min1]
    print("a1 = ",a)
    print("b1 = ",b)
    print("len(b1) = ",len(b))
    print("dist(a1, b1) = ",distance(a, b)[-1][-1])
    score1 = distance(a, b)[-1][-1]/len(b)
    print("score1 = ", score1)


    ind_min2 = ind_min(a,b)
    print("indice minimale",ind_min2)
    a,b = a[:ind_min2],b[:ind_min2]
    print("\na2 = ",a)
    print("b2 = ",b)
    print("len(b2) = ",len(b))
    print("dist(a2, b2) = ",distance(a, b)[-1][-1])
    score2 = distance(a, b)[-1][-1]/len(b)
    print("score2 = ", score2)

"""

    #print("meilleur alignement = ", min(score1, score2))
