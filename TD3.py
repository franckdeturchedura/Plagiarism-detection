from ctypes import CDLL, c_char_p
so_file = './affichage.so'
affichage = CDLL(so_file)
# Compilation du .so avec :
# gcc -shared -Wl,-soname,affichage -o affichage.so -fPIC affichage.c

def read_text(textfile):
    '''
    Permet de lire un fichier texte.
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
    tab_inv = [ tab[-i] for i in range(1,len(tab)+1) ]
    return tab_inv

def retourne_indices(i, j, T):
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
            B_p.append("_")
            i = i-1
        
        elif(i_p-i == 0 and j_p-j == -1):
            A_p.append("_")
            B_p.append(B[j_p])
            j = j-1
        else:
            print("i_p :", i_p)
            print("i :", i)
            print("j_p :", j_p)
            print("j :", j)

    return "".join(inverse_tab(A_p)), "".join(inverse_tab(B_p))

# Question 4 #


if __name__ == '__main__':
    A = 'abbacb'
    B = 'cbbbacab'

    text1 = read_text('texte1.txt')
    text2 = read_text('texte2.txt')

    text3 = read_text('texte1_v2.txt')
    text4 = read_text('texte2_v2.txt')

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

    test1 = "abcd\n423\namen\n"
    test2 = "abcE\n123\n"

    a, b = alignements_optimaux(text3, text4)

    tab1 = a[:-1].split('\n') # On fait la liste des différents paragraphes
    tab2 = b[:-1].split('\n')

    matchs = []
    for p1 in tab1: # On parcours les paragrphes du 1er texte
        # print("p1 = {}".format(p1))
        dist = 9999
        p = tab2[0]
        for p2 in tab2: # Pour chaque p1 on parcours les paragraphes du 2nd texte
            # print("p2 = {}".format(p2))
            T = distance(p1, p2)
            if T[-1][-1] < dist : # On retient le paragraphe p2 qui est le plus proche de p1
                dist = T[-1][-1]
                p = p2
                # print("p = {}".format(p))
        matchs.append([p1, p]) # On renvoie la paire de paragrahes dans matchs
        # print('***********')
    # print(matchs)

    # On affiche les paires de paragraphes ensembles
    for k in matchs:
        t1 = c_char_p(k[0].encode('utf-8'))
        t2 = c_char_p(k[1].encode('utf-8'))
        affichage.affiche(t1, t2, 65)

