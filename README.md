# Detection_plagiat
Algo de détection de plagiat (ou similitude entre deux chaînes de caractères)



**Comment compiler sous Ubuntu : **


On installe les librairies nécessaires : 

`sudo apt-get install gcc cython3 python3-pip python3-lxml`

`sudo python3 -m pip install requests docopt path.py`

Pour créer le fichier .c : 

`cython3 <nom_du_fichier.py> -o <nom_du_fichier.c> --embed`

On compile ensuite le fichier.c

`gcc -Os -I /usr/include/python3.6m  <nom_du_fichier.c> -o <nom_du_compilé_sans_extension> -lpython3.6m -lpthread -lm -lutil -ldl`

Si ça ne marche pas c'est que le python installé n'est pas le bon

Alors : `locate Python.h` puis remplacer `/usr/include/python3.6m` par le résultat et `-lpython3.6m`par la bonne version également.

On donne les bons droits :

`chmod u+x <nom_du_compilé_sans_extension>`

On peut l'éxécuter :

`./<nom_du_compilé_sans_extension`

**Compiler en .tar.gz sous ubuntu : **

`tar czvf <nom_archive>.tar.gz <nom_rep>`


**Envoi au prof : **

Compresser les .py, les .c correspondants et les compilés, ainsi que les instructions précédentes (à mettre également dans le rapport).

Il faut également inclure le rapport.

Le tout à destination de `jean.cousty@esiee.fr` avec pour objet `INF-4202B : TDm #2 : livrables` avec les deux membres du binôme en copie avant le 06/01/2020 à 23h55.

