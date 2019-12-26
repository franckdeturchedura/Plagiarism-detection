def read_text(textfile):
    with open(textfile, 'r') as f:
        text = f.read()
    return text

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

def inverse_tab(T):
    T_inv = [ T[-i] for i in range(1,len(T)+1) ]
    return T_inv

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
    if(len(A) > len(B)):
        A, B = B, A

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

if __name__ == '__main__':
    A = 'abbacb'
    B = 'cbbbacab'

    text1 = read_text('texte1.txt')
    text2 = read_text('texte2.txt')

    T = distance(text1, text2)
    
    a, b = alignements_optimaux(text1, text2)

    print("Dist(A, B) = {}\n".format(T[-1][-1]))
    # print(a)
    # print('\n\n\n')
    # print(b)
    print("len(text1) =", len(text1), ", len(text2) =", len(text2))
    print("len(a) =", len(a), ", len(b) =", len(b))