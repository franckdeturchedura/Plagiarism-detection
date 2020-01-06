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

# Question 3 #
def Del(): return 1
def Ins(): return 1
def Sub(seq1, seq2):
    if(seq1==seq2): return 0
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

def retourne_indices(i, j, T):
    '''
    Permet de remonter le tableau T en partant de la fin
    et en empruntant un chemin de cout minimum.
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

    else: # En cas d'égalité on choisi de remonter par la diagonale.
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

    while(i!=0 and j!=0):
        i_p, j_p = retourne_indices(i,j,T)  # on calcule les indices suivants pour remonter T

        if(i_p-i == -1 and j_p-j == -1):  # Cas ou le score optimal est sur la diagonale
            A_p.append(A[i_p])
            B_p.append(B[j_p])
            i = i-1
            j = j-1

        elif(i_p-i == -1 and j_p-j == 0):  # Cas ou le score optimal est sur la ligne
            A_p.append(A[i_p])
            B_p.append(" ")
            i = i-1
        
        elif(i_p-i == 0 and j_p-j == -1):  # Cas ou le score optimal est sur la colonne
            A_p.append(" ")
            B_p.append(B[j_p])
            j = j-1

    A_p.reverse() # on remet les séquences à l'endroit
    B_p.reverse()
    return "".join(A_p), "".join(B_p)

# Question 4 #
def Del2(seq): return len(seq)
def Ins2(seq): return len(seq)
def Sub2(seq1, seq2): return distance(seq1, seq2)[-1][-1]

def distance2(T1, T2):
    '''
    Renvoie la table T des distances entre les textes T1 et T2.
    La distance entre T1 et T2 est contenue dans T[-1][-1].
    '''
    lenT1 = len(T1)
    lenT2 = len(T2)

    T = [ [0 for j in range(lenT2)] for i in range(lenT1) ]

    for i in range(1, lenT1):
        T[i][0] = T[i-1][0] + Del2(T1[i])

    for j in range(1, lenT2):
        T[0][j] = T[0][j-1] + Ins2(T2[j])

    for i in range(1, lenT1):
        for j in range(1, lenT2):
            T[i][j] = min(
                T[i][j-1] + Ins2(T2[j-1]),
                T[i-1][j] + Del2(T1[i-1]),
                T[i-1][j-1] + Sub2(T1[i-1], T2[j-1])
            )  
    return T

def alignements_paragraphes(T1, T2):
    '''
    Renvoie un alignement optimal des textes T1 et T2.
    '''
    T1_p = []
    T2_p = []

    i = len(T1)-1
    j = len(T2)-1
    i_p = 0
    j_p = 0

    T = distance2(T1, T2)

    while(i!=0 and j!=0):
        i_p, j_p = retourne_indices(i,j,T)

        if(i_p-i == -1 and j_p-j == -1):
            T1_p.append(T1[i_p])
            T2_p.append(T2[j_p])
            i = i-1
            j = j-1

        elif(i_p-i == -1 and j_p-j == 0):
            T1_p.append(T1[i_p])
            T2_p.append(" ")
            i = i-1
        
        elif(i_p-i == 0 and j_p-j == -1):
            T1_p.append(" ")
            T2_p.append(T2[j_p])
            j = j-1

    T1_p.reverse()
    T2_p.reverse()
    return T1_p, T2_p


if __name__ == '__main__':
    A = 'abbacb'
    B = 'cbbbacab'

    text1 = read_text('texte1.txt')
    text2 = read_text('texte2.txt')

    text3 = read_text('t1.txt')
    text4 = read_text('t2.txt')

    #****************
    # Exemple       #
    #****************
    print("Exemple d'alignement pour {} et {} :\n".format(A, B))

    a, b = alignements_optimaux(A, B)
    T = distance(a, b)

    print("\tDistance({}, {}) = {}".format(a, b, T[-1][-1]))
    print('\t'+a)
    print('\t'+b,'\n')

    print('************************************************')

    #****************
    # Question 3    #
    #****************
    print("QUESTION 3\n")
    print("Alignement des textes 'texte1.txt' et 'texte2.txt' :\n")

    a, b = alignements_optimaux(text1, text2)
    T = distance(text1, text2)

    print("Distance(texte1, texte2) = {}\n".format(T[-1][-1]))
    t1 = c_char_p(a.encode('utf-8'))
    t2 = c_char_p(b.encode('utf-8'))
    affichage.affiche(t1, t2, 65)

    print('\n************************************************')

    #****************
    # Question 4    #
    #****************

    print("QUESTION 4\n")

    # On crée les tableaux contenant les paragraphes de text3 et text4.
    tab1 = text3.split('\n')
    tab2 = text4.split('\n')

    a, b = alignements_paragraphes(tab1, tab2)

    T = distance2(tab1, tab2)
    similarite = 1-(T[-1][-1]/(len(text3)+len(text4)))
    print('Distance entre les textes : {}; longueur de t1.txt : {}, longueur de t2.txt : {}'.format(
        T[-1][-1],
        len(text3),
        len(text4)
    ))
    print('Score de similarité en % : {:.6f}'.format(similarite*100))

    # Affichage
    for i, j in zip(a, b):
        t1 = c_char_p(i.encode('utf-8'))
        t2 = c_char_p(j.encode('utf-8'))
        affichage.affiche3(t1, t2, 65)
    affichage.afficheSeparateurHorizontal(65)
