
## QUESTION 1

def Del():
    return 1

def Ins():
    return 1

def Sub(x,y):
    if(x==y):
        return 0
    return 1



def score_alignement_opti(seqA,seqB):
    tailleA = len(seqA)
    tailleB = len(seqB)
    t = [[0 for x in range(tailleB)]for y in range(tailleA)]
    t[0][0] = 0

    for i in range(1,len(seqA)):
        t[i][0] = t[i-1][0] + Del()

    for j in range(1,len(seqB)):
        t[0][j]= t[0][j-1] + Ins()

    for i in range(1,len(seqA)):
        for j in range(1,len(seqB)):
            v1 = t[i][j-1] + Ins()
            v2 = t[i-1][j] + Del()
            v3 = t[i-1][j-1] + Sub(seqA[i-1],seqB[j-1])
            t[i][j] = min(v1,v2,v3)
            if(t[i][j]<0):
                t[i][j] = 0
    return t


test = score_alignement_opti("abbacb","cbbbacab")

print(test[-1][-1])
print(test)

#print(test[len("cbbbacab")][len("abbacb")])

##QUESTIOn 2
#on a la matrice t via la fonction précédente


##fonction qui retourne les prochains indices où la valeur est STRICTEMENT minimum aux autres. Sinon False
def retourne_indices(i_actuel,j_actuel,t):
    if(t[i_actuel + 1 ][j_actuel]<t[i_actuel][j_actuel+1] and t[i_actuel + 1 ][j_actuel]<t[i_actuel+1][j_actuel+1] ):
        i_actuel= i_actuel+1
        return i_actuel,j_actuel

    if(t[i_actuel ][j_actuel + 1]<t[i_actuel+1][j_actuel] and t[i_actuel][j_actuel+1]<t[i_actuel+1][j_actuel+1] ):
        j_actuel= j_actuel+1
        return i_actuel,j_actuel

    if(t[i_actuel + 1 ][j_actuel+1]<t[i_actuel][j_actuel+1] and t[i_actuel + 1 ][j_actuel+1]<t[i_actuel+1][j_actuel] ):
        i_actuel= i_actuel+1
        j_actuel = j_actuel +1
        return i_actuel,j_actuel

    else:
        return i_actuel+1,j_actuel+1

def alignements_optimaux(seqA,seqB):
    seqA_p = ""
    seqB_p = ""
    i=0
    j=0
    i_p=0
    j_p=0
    y=0
    m = len(seqA)
    n = len(seqB)
    t = score_alignement_opti(seqA,seqB)
    while(i < n-2 and j < m-2):
        i_p,j_p = retourne_indices(i,j,t)
        if(i_p-i==1 and j_p-j==1):
            seqA_p[y]+=seqA[i_p]
            seqB_p[y]+=seqB[j_p]
            y=y+1
            i=i+1
            j=j+1

        elif(i_p-i==1 and j_p-j==0):
            seqA_p[y]+=seqA[i_p]
            seqB_p[y]+="_"
            y=y+1
            i=i+1
            j=j+1

        elif(i_p-i==0 and j_p-j==1):
            seqA_p[y]+="_"
            seqB_p[y]+=seqB[j_p]
            y=y+1
            i=i+1
            j=j+1
        else:
            s=1
            while(i_p ==False and j_p==False):
                i_p,j_p = retourne_indices(i+s,j+s,t)
        return seqA_p,seqB_p

a,b = alignements_optimaux("abbacb","cbbbacab")
print(a)
print(b)
