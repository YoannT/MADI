#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils.utils import *
from random import randint
import pyAgrum as gum
from pyAgrum.lib.pretty_print import pretty_cpt
from sklearn.cluster import KMeans
import numpy as np
import scipy.cluster.hierarchy as hcluster
from copy import deepcopy as dc

# Kmeans pour determiner les classes
def kmeans(lignes,nbClasses):
	"""
	lignes: liste de strings
	nbClasse: nombre de classes a determiner
	"""
	for i,li in enumerate(lignes):
		lignes[i] = lignes[i].strip(' \n').split(',')
		lignes[i] = [int(lignes[i][j]) for j in range(len(lignes[i]))]	
	lignes = np.array(lignes)
	
	lignes = np.asmatrix(lignes)

	kmeans = KMeans(n_clusters=nbClasses, random_state=0).fit(lignes)
	
	return kmeans.cluster_centers_

# Generation d'un CNB
def cnb(nomCSV,saveBIF,nbClasses,chemin):
	"""
	nomCSV: nom du fichier CNB a lire
	saveBIF: nom du fichier bif ou enregistrer le BN de type CNB
	nbCLasses: nombre de classes du CNB
	"""
	fic = open(nomCSV,'r')

	lignes = fic.readlines()

	fic.close()
	
	ligs = dc(lignes)
	del ligs[0]
	
	classes = kmeans(ligs, nbClasses)
	
	print(classes)
	
	exit()
	
	fic = open(chemin+'classes.csv', 'w')
	
	
	fic.close()

	nomVars = []

	for v in lignes[0].strip(' \n').split(','):
		nomVars.append(v)

	y = len(nomVars)

	bn = gum.BayesNet()
	
	for v in nomVars:
		var = bn.add(gum.LabelizedVariable(v, '', 3))
		
	y = bn.add(gum.LabelizedVariable('Y', '', len(classes)))
	
	for v in bn.topologicalOrder():
		if v != y:
			bn.addArc(y, v)
			
			
	bn.saveBIF(saveBIF)

	writeCSV = nomCSV[:len(nomCSV)-4]+"_missing.csv"

	fic_write = open(writeCSV,'w')

	for ligne in lignes[1:]:
		fic_write.write(ligne.strip(' \n')+',100\n')

	fic_write.close()
	
# Inverse la cpt de Y: chaque ligne contient maintenant Y| X1,X2...
# Calcule pour chaque cas X de la base la probabilité de Y|X
# Sauvegarde le bn obtenu dans "inv.bif"

def inverser(nomBIF,nomCSV):
	"""
	nomBIF: nom du fichier bif a lire
	nomCSV: nom du fichier csv a lire
	"""
	bn = gum.BayesNet()
	bn.loadBIF(nomBIF)

	fic = open(nomCSV, 'r')

	lignes = fic.readlines()
	del lignes[0]

	fic.close()
	
	inv = gum.BayesNet()
	inv.loadBIF(nomBIF)
	# print dir(inv)
	
	Y = bn.topologicalOrder()[0]
	
	for c in bn.children(Y):
		inv.eraseArc(Y, c)
		inv.addArc(c, Y)
	
	
	inv.generateCPT(Y)
	
	for num, lig in enumerate(lignes):
		print(num)
		l = lig.strip('\n').split(',')
		l = [int(l[i]) for i in range(len(l))]
		dic = {bn.variable(i).name():l[i] for i in range(len(l))}
		inv.cpt(Y)[dic] = 1.0
		for c in bn.children(Y):
			inv.cpt(Y)[dic] *= bn.cpt(c)[dic]
		inv.cpt(Y)[dic] *= bn.cpt(Y)[dic]
	print("FIN PARCOURS LIGNES")
	inv.cpt(Y).normalizeAsCPT()
	printBN(inv)
	inv.saveBIF("inv.bif")

# Utilise le bn inverse obtenu grace a inverser pour attribuer a chaque ligne de la base une valeur de Y
def classer(nomBIF,nomCSV,saveCSV):
	"""
	nomBIF:  nom du fichier bif a lire
	nomCSV: nom du fichier csv a lire
	saveCSV: nom du fichier csv a generer
	"""
	bn = gum.BayesNet()
	bn.loadBIF(nomBIF)
	Y = bn.size()-1
	bn.cpt(Y).normalizeAsCPT()
	fic = open(nomCSV, 'r')
	lignes = fic.readlines()
	fic.close()

	
	fic = open(saveCSV, 'w')
	fic.write(lignes[0]+',Y\n')
	del lignes[0]
	for num, lig in enumerate(lignes):
		print(num)
		fic.write(lig.strip('\n'))
		l = lig.strip('\n').split(',')
		l = [int(l[i]) for i in range(len(l))]
		dic = {bn.variable(i).name():l[i] for i in range(len(l))}
		#classe = np.random.choice(range(bn.variable(Y).domainSize()),p = bn.cpt(Y)[dic])
		classe = np.argmax(bn.cpt(Y)[dic])
		fic.write(','+str(classe)+'\n')
	fic.close()
	




