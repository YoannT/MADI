#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils.utils import *
from random import randint
import pyAgrum as gum
from pyAgrum.lib.pretty_print import pretty_cpt
import numpy as np
import genere
import matplotlib.pyplot as plt
from copy import deepcopy as dc

# Lire un fichier bif et generer un fichier bif avec une variable en plus
def ecrireBIF(nomVar,probasVar,filsVar,nomBIF,saveBIF):
	"""
	nomVar: nom de la variable a ajouter
	probasVar: probabilités de la variable a ajouter
	filsVar: fils de la variable
	nomBIF: nom du fichier bif a lire
	saveBIF: nom du fichier bif a generer
	"""
	bn = gum.BayesNet()
	bn.loadBIF(nomBIF)
	
	var = bn.add(gum.LabelizedVariable(nomVar,'',len(probasVar)))
	bn.cpt(var)[:] = dc(probasVar)
	for f in filsVar:
		
		bn.addArc(var,f)
		for v in range(len(probasVar)):
			bn.cpt(f)[{nomVar:v}] = randomDistrib(bn.variable(f).domainSize())

		aSuppr = list(set(bn.parents(f)).intersection(filsVar))

		for nodeid in aSuppr:
			bn.eraseArc(nodeid,f)

	printBN(bn)
	bn.saveBIF(saveBIF)
	
# Generer un fichier csv avec une valeur cachee
def genererCSV(idManquant,N,nomCSV,nomBIF,pourcManquant):
	"""
	idManquant: ID de la variable cachee
	N: nombre de lignes a generer
	nomCSV: nom du fichier csv a generer
	nomBIF: nom du fichier bif a lire
	pourcManquant: pourcentage de valeurs manquantes
	"""
	bn = gum.BayesNet()
	bn.loadBIF(nomBIF)

	CSV = open(nomCSV,'w')
	for I in range(N):
		Vals = [None]*bn.size()
		while None in Vals:
			for nodeid in bn.topologicalOrder():
				if Vals[nodeid] == None:
					parents = bn.parents(nodeid)
					if len(bn.parents(nodeid)) == 0:
						proba = np.append(bn.cpt(nodeid)[:-1], 1.0 - sum(bn.cpt(nodeid)[:-1]))
						Vals[nodeid] = np.random.choice(len(proba),1, p = proba)[0]
					else:
						possible = True
						for p in parents:
							if Vals[p] == None:
								possible = False
						if possible:
							dico = {}
							for p in parents:
								dico[bn.variable(p).name()] = Vals[p]
							proba = np.append(bn.cpt(nodeid)[dico][:-1],1.0-sum(bn.cpt(nodeid)[dico][:-1]))
							Vals[nodeid] = np.random.choice(len(proba),1, p = proba)[0]
		
		for j in range(len(Vals)):
			Vals[j] = np.random.choice([Vals[j],100],1, p = [1-(pourcManquant/100),(pourcManquant/100)])[0]
		Vals[idManquant] = 100
		if I>0:
			CSV.write('\n')
		for j in range(len(Vals)):
			CSV.write(str(Vals[j]))
			if j<bn.size()-1:
				CSV.write(',')

	CSV.close()

	
  
	







