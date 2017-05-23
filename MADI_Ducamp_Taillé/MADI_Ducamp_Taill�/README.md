Projet de MADI de Gaspard Ducamp et Yoann Taillé.

Utiliser de préférence le main.py à la racine du projet.

Les fichiers cnb et bif contiennent respectivement les différents fichiers .csv et .bif, le reste contient des fichiers .py.

###################################
# Partie 1: Génération de données #
###################################

Les fichiers .py de génération de données sont situés dans le dossier genere.

La génération de cas sans valeur manquante se fait grâce à la fonction genererCSV du fichier genere.py.

#########################################################
# Partie 2: Apprentissage sur base de données complètes #
#########################################################

L'apprentissage sur base complète est fait grâce à la fonction plearn se trouvant dans plearn/plearn.py.

L'estimation de différence de paramètres entre deux BN est faite grâce à la fonction compareParams se trouvant dans perf/perf.py

L'utilisation de cette estimation est effectuée dans la fonction evalLearning du même fichier.
Pour lancer cete fonction avec comme apprentissage plearn, mettre à 0 le paramètre methode.

###########################
# Partie 3: Algorithme EM #
###########################

La génération de cas avec valeurs manquantes se fait grâce à la fonction genererCSV du fichier genere/genere_missing.py.

Une fois la base incomplète générée, l'algorithme EM peut y être appliqué en appelant la fonction learn du fichier em/emlearn.py.

#############################
# Partie 4: Variable Cachée #
#############################

L'ajout d'une variable à un BN est possible grâce à la fonction ecrireBIF du fichier genere/variable_cachee.py.

La génération de cas avec valeurs manquantes et variable cachée se fait grâce à la fonction genererCSV du fichier genere/variable_cachee.py.

Une fois la base de données générée, apprendre les paramètres du BN avec EM est possible grâce à la fonction learn du fichier em/emlearn.py. 

################# 
# Partie 5: CNB #
#################

Pour générer un BN de type CNB, utiliser la fonction cnb du fichier cnb/cnb.py.

Pour apprendre les paramètres du CNB, utiliser la fonction learn du fichier em/emcnb.py.

Pour la classification, il faut avoir appris les paramètres du CNB.

Ensuite, il faut tout d'abord utiliser la fonction inverser du fichier. Cela permet d'obtenir les probabilités conditionnelles de Y sur la base de données de test.

Une fois ces probabilités calculées, appeler classer du même fichier pour attribuer une classe à chaque ligne d'un fichier.








































