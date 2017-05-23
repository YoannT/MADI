#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils.utils import *
from genere import genere_missing
from genere import variable_cachee
from em import emlearn
from em import emcnb
from perf import perf
#from em import emlearnvarC
import pyAgrum as gum
from cnb import cnb

csvpath = './csv/'
bifpath = './bif/'

 ###################
# GENERATIONS DE BN #
 ###################

#variable_cachee.ecrireBIF('x',[0.7,0.3],[2,4],bifpath+"bn.bif",bifpath+"varC.bif") # ajoute une variable a un bn et l'enregistre dans un fichier bif
#cnb.cnb(csvpath+'cnb_learning_noY.csv',bifpath+'cnb.bif',10,csvpath) # genere un BN de type CNB

 ####################
# GENERATIONS DE CSV #
 ####################

#genere_missing.genererCSV(1000,csvpath+'test1.csv',bifpath+'bn.bif',10.0) # genere un fichier csv avec un certain pourcentage de valeurs manquantes
variable_cachee.genererCSV(6,1000,csvpath+'varC.csv',bifpath+'varC.bif',0.0) # genere un fichier csv avec un certain pourcentage de valeurs manquantes et une variable cachee

 ####
# EM #
 ####
 
#emlearn.learn(bifpath+"empty_bn.bif",csvpath+"test1.csv",bifpath+'bn_res.bif',30) # EM sur base
emlearn.learn(bifpath+"empty_varC.bif",csvpath+"varC.csv",bifpath+'test1.bif',20) # EM sur base de donnees avec valeurs et variables cachees
#emcnb.learn(bifpath+"cnb.bif",csvpath+'cnb_learning_noY_missing.csv',bifpath+'cnb_res.bif',20) # EM dans un CNB

 #######
# PERFS #
 #######

#perf.evalLearning(1000,0) # Evaluation des performances sur des fichiers d'un certain nombre de lignes (deuxieme parametre = 0 pour plearn,1 pour EM,2 pour EM avec variables cachees)

 ################
# CLASSIFICATION #
 ################
 
#cnb.inverser(bifpath+"cnb.bif",csvpath+'cnb_test_noY.csv') # sert a la classification, apres avoir appris les parametres avec EM
#cnb.classer(bifpath+'inv.bif',csvpath+'cnb_test_noY.csv',csvpath+'cnb_test.csv') # A utiliser apres inverse


