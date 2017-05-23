#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

from cnb import cnb
from em import emlearn
from plearn import plearn
from genere import genere
from genere import genere_missing as gm
from genere import variable_cachee as vc
import pyAgrum as gum
import matplotlib.pyplot as plt


csvpath = parentdir + '/csv/'
bifpath = parentdir + '/bif/'

# Comparaison des parametres de deux BN
def compareParams(nomBIF1,nomBIF2):

	bn1 = gum.BayesNet()
	bn1.loadBIF(nomBIF1)

	bn2 = gum.BayesNet()
	bn2.loadBIF(nomBIF2)

	somme = 0
	for nodeid in range(bn1.size()):
		p1=bn1.cpt(nodeid)
		i1=gum.Instantiation(p1)
		i1.setFirst()
		p2=bn2.cpt(nodeid)
		while (not i1.end()):
			somme += pow((p1.get(i1)-p2.get(i1)),2)
			i1.inc()

	return (1.0/bn1.size()) * somme

# Evaluation des performances des methodes d'apprentissage

def evalLearning(N,methode = 0):
	"""
	N: nombre de lignes des bases de donnees
	methode: determine quel apprentissage on evalue
	"""

	# methode = 0: plearn
	# methode = 1: EM sans variable cachee
	# methode = 2: EM avec variable cachee
	
	if methode == 0:
		
		res = []
	
		for I in range(1,N+100,100):
			print (I)
			genere.genererCSV(I,csvpath+"perf.csv",bifpath+"bn.bif")
			plearn.learn(bifpath+"empty_bn.bif",csvpath+"perf.csv",bifpath+'perf1.bif')
			res.append(compareParams(bifpath+'perf1.bif',bifpath+'bn.bif'))
		
		plt.xlabel('Nombre de lignes de la base')
		plt.ylabel(u'Différence')
		plt.plot(range(1,N+100,100),res)
		plt.show()
		
	elif methode == 1:
		res = []
		pourcs = [0.0,3.0,5.0,10.0,20.0,50.0]
		
		for pourc in pourcs:
			print ("Pourcentage de valeurs manquantes",pourc)
			gm.genererCSV(N,csvpath+"perf.csv",bifpath+"bn.bif",pourc)
			emlearn.learn(bifpath+"empty_bn.bif",csvpath+"perf.csv",bifpath+'perf1.bif',30)
			res.append(compareParams(bifpath+'perf1.bif',bifpath+'bn.bif'))
		
		plt.xlabel('Pourcentage de valeurs manquantes')
		plt.ylabel(u'Différence')
		plt.plot(pourcs,res)
		plt.show()
		
	elif methode == 2:
		res = []
		pourcs = [0.0,3.0,5.0,10.0,20.0,50.0]
		for pourc in pourcs:
			print ("Pourcentage de valeurs manquantes",pourc)
			
			vc.genererCSV(6,N,csvpath+'perf.csv',bifpath+'varC.bif',pourc)
			emlearn.learn(bifpath+"empty_varC.bif",csvpath+"perf.csv",bifpath+'perf1.bif',10)
			
			res.append(compareParams(bifpath+'perf1.bif',bifpath+'varC.bif'))
			
		plt.xlabel('Pourcentage de valeurs manquantes')
		plt.ylabel(u'Différence')
		plt.plot(pourcs,res)
		plt.show()
