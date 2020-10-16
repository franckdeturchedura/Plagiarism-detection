# Détection de plagiat - Project ESIEE Paris

@authors Par Franck Deturche-Dura et Guillaume Gay 

Algorithme de détection de plagiat (ou similitude entre deux chaînes de caractères)



## Compiler sous Ubuntu 


On installe les librairies nécessaires : 

`sudo apt-get install gcc cython3 python3-pip python3-lxml`

`sudo python3 -m pip install requests docopt path.py`

Pour créer le fichier .c : 

`cython3 <nom_du_fichier.py> -o <nom_du_fichier.c> --embed`

On compile ensuite le fichier.c

`gcc -Os -I /usr/include/python3.6m  <nom_du_fichier.c> -o <nom_du_compilé_sans_extension> -lpython3.6m -lpthread -lm -lutil -ldl`

Si ça ne marche pas c'est que la version de python spécifiée n'est pas la bonne.

Alors : `locate Python.h` puis remplacer dans la commande ci-dessus `/usr/include/python3.6m` par le résultat et `-lpython3.6m`par la bonne version également.

On donne les bons droits :

`chmod u+x <nom_du_compilé_sans_extension>`

On peut l'éxécuter :

`./<nom_du_compilé_sans_extension`

## Compiler en .tar.gz sous ubuntu  

`tar czvf <nom_archive>.tar.gz <nom_rep>`

## Execution

Run `gcc affichage.c` and `./affichage`

