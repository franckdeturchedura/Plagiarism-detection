#include <stdio.h>
#include <stdlib.h>
#include <string.h>



//DEL et INS sont considérés comme des malus pour pénaliser l'introduction d'insertions dans l'alignement

int Del(){
  return -1;
}

int Ins(){
  return -1;
}


//Donne 2 points si x et y sont pareils et enlève 2 points sinon
int Sub(char x,char y){
  if(x==y){
    return 2;
  }
  return -2;
}

int max2(int x,int y){
  if(x>y){
    return x;
  }
  return y;
}

int max3(int x,int y,int z){
  return max2(max2(x,y),z);
}


void score_alignement_opti(int ** t,char * seqA,char * seqB,int tailleA,int tailleB){
  int i=0;
  int j=0;

  t[0][0] = 0;

  for(i=1;i<tailleA;i++){
    t[i][0] = t[i-1][0] + Del();
  }

  for(j=1;j<tailleB;j++){
    t[0][j]= t[0][j-1] + Ins();

  }

  int v1,v2,v3;
  for(i=1;i<tailleA;i++){
    for(j=1;j<tailleB;j++){
      v1 = t[i][j-1] + Ins();
      v2 = t[i-1][j] + Del();
      v3 = t[i-1][j-1] + Sub(seqA[i-1],seqB[j-1]);
      t[i][j] = max3(v1,v2,v3);
    }
  }


}

int main(void){
  printf("salut");
  char * seqA = "abbbabdaaa";
  char * seqB = "baadbbd";
  int tailleA = 10;
  int tailleB = 7;
  int ** t ;
  score_alignement_opti(t,seqA,seqB,tailleA,tailleB);



  //score_alignement_opti(t,"abbacb","cbbbacab");
}
