#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <string.h>

struct alignement
{
	char * x;
	char * y;
};


/* =============================================================== */
char * readtextfile(char * filename)
  /* Retourne le contenu du fichier texte filename */
/* =============================================================== */
{
	struct stat monstat;
	int N;
	char * text = NULL;
	FILE *fd = NULL;

	N = stat(filename, &monstat);
	if (N == -1)
	{
	fprintf(stderr, "error : bad file %s\n", filename);
	exit(0);
	}
	N = monstat.st_size;
	text = (char *)malloc(N+1);
	if (text == NULL)
	{   fprintf(stderr,"readtextfile() : malloc failed for text\n");
	  exit(0);
	}
	fd = fopen(filename,"r");
	if (!fd)
	{
	fprintf(stderr, "readtextfile: can't open file %s\n", filename);
	exit(0);
	}

	fread(text, sizeof(char), N, fd);
	if((N>0) && (text[N-1] == '\n') ) text[N-1] = '\0';
	else text[N-1] = '\0';
	fclose(fd);
	return text;
}

/* =============================================================== */
int Imax(int a, int b)
/* Retourne  le maximum de a et b                                  */
/* =============================================================== */
{
	if (a < b) return b;
	else return a;	       
}

/* =============================================================== */
int Imin2(int a, int b)
/* Retourne  le minimum de a et b                                  */
/* =============================================================== */
{
	if (a < b) return a;
	else return b;	       
}

/* =============================================================== */
int Imin3(int a, int b, int c)
/* Retourne  le minimum de a, b et c                               */
/* =============================================================== */
{
	return Imin2(Imin2(a,b),c);
}

/* =============================================================== */
void retourne(char *c)
/* Retourner la chaîne de caractère c                              */
/* =============================================================== */
{
	char tmp;
	int m, j, i;
	m = strlen(c);
	j = m/2;
	for(i = 0; i < j; i++ ){
	tmp = c[i];
	c[i] = c[m-i-1];
	c[m-i-1] = tmp;
	}
}
/* =============================================================== */
void afficheSeparateurHorizontal(int nbcar)
/* =============================================================== */
{
	int i;
	printf("|-");
	for(i=0; i < nbcar; i++)
	printf("-");
	printf("-|-");
	for(i=0; i < nbcar; i++)
	printf("-");
	printf("-|\n");
}


/* =============================================================== */
void affiche(char* texte1, char* texte2, int nbcar)
  /* Affiche simultanément texte1 et texte 2 en positionnnant nbcar  
     caractères sur chaque ligne. */
/* =============================================================== */
{
	int i, l1, l2, l;

	char *t1,*t2;

	char out[512];

	l1 = strlen(texte1);
	l2 = strlen(texte2);

	t1 = (char*) malloc(sizeof(char) * (nbcar + 1));
	t2 = (char*) malloc(sizeof(char) * (nbcar + 1));

	l = Imax(l1, l2);
	afficheSeparateurHorizontal(nbcar);
	for(i = 0; i < l; i+= nbcar){
	if (i < l1) {
	  strncpy(t1, &(texte1[i]), nbcar);
	  t1[nbcar] = '\0';
	} else t1[0] = '\0';
	if (i < l2) {
	  strncpy(t2, &(texte2[i]),nbcar);
	  t2[nbcar] = '\0';
	} else t2[0] = '\0';

	sprintf(out, "| %c-%ds | %c-%ds |\n",'%', nbcar, '%', nbcar);
	printf(out, t1,t2);
	}
	afficheSeparateurHorizontal(nbcar);
	free(t1);
	free(t2);
}



/* =============================================================== */
void affiche2(char* texte1, char* texte2, int nbcar)
  /* idem affiche, mais avec un formattage différent
/* =============================================================== */
{

	int i, l1, l2, l;

	char *t1,*t2;

	char out[512];

	l1 = strlen(texte1);
	l2 = strlen(texte2);

	t1 = (char*) malloc(sizeof(char) * (nbcar + 1));
	t2 = (char*) malloc(sizeof(char) * (nbcar + 1));

	l = Imax(l1, l2);

	for(i = 0; i < l; i+= nbcar){
	if (i < l1) {
	  strncpy(t1, &(texte1[i]), nbcar);
	  t1[nbcar] = '\0';
	} else t1[0] = '\0';
	if (i < l2) {
	  strncpy(t2, &(texte2[i]),nbcar);
	  t2[nbcar] = '\0';
	} else t2[0] = '\0';

	sprintf(out, "x: %c-%ds \ny: %c-%ds\n",'%', nbcar, '%', nbcar);
	printf(out, t1,t2);

	}
	free(t1);
	free(t2);
}

/* =============================================================== */
int sub(char x, char y)
/* Renvoie le coup d'une substitution des caractères x et y. */
/* =============================================================== */
{
	if( x == y ) return 0;
	else return 1;
}

/* =============================================================== */
int distance(char* texte1, char* texte2)
/* Calcule le la distance optimale entre les textes 1 et 2 */
/* =============================================================== */
{
	int l1, l2;
	int i, j;
	int dist;

	l1 = strlen(texte1);
  	l2 = strlen(texte2);
  	
  	int T[l1][l2];

	T[0][0] = 0;
	
	for(i = 1; i < l1; i++){
		T[i][0] = T[i-1][0] + 1;
	}
	for(j = 1; j < l2; j++){
		T[0][j] = T[0][j-1] + 1;
	}
	for(i = 1; i < l1; i++){
		for(j = 1; j < l2; j++){
			T[i][j] = Imin3(T[i][j-1] + 1,
							T[i-1][j] + 1,
							T[i-1][j-1] + sub(texte1[i-1], texte2[j-1]) );
		}
	}
	
	// Afficher le tableau T *******************
/*	printf("\tl1(i) = %d, l2(j) = %d", l1, l2);
	for(i = 0; i < l1; i++){
		printf("\n");
		for(j = 0; j < l2; j++){
			printf("\t%d", T[i][j]);
		}
		printf("\n");
	}
	//******************************************/

	dist = T[l1-1][l2-1];
	return dist;
}



/* =============================================================== */
int main(int argc, char **argv)
/* =============================================================== */
{
	char *x, *y; 

	if(argc != 3){
		printf("usage: %s text1 text2\n", argv[0]);
		exit(0);
	}  

	x = "abbacb";
	y = "cbbbacab";

	printf("\ndist(%s, %s) = %d\n\n", x, y, distance(x, y));

/*
	x = readtextfile(argv[1]);
	y = readtextfile(argv[2]);
	
	printf("\ndist(x,y) = %d\n\n", distance(x, y));

	affiche(x, y, 50);

	free(x);
	free(y); */
}
