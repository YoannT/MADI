#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import pyAgrum as gum
from pyAgrum.lib.pretty_print import pretty_cpt
import numpy as np

def genererCSV(N,nomCSV,nomBIF,pourcManquant):
	"""
	N: nombre de lignes
	nomCSV: nom du fichier csv enregistrer
	nomBIF: nom du fichier bif a lire
	pourcManquant: pourcentage de valeurs manquantes a generer
	"""
	bn = gum.BayesNet()
	bn.loadBIF(nomBIF)

	CSV = open(nomCSV,'w')

	for I in range(N):
		Vals = [None]*bn.size()
		while None in Vals:
			for nodeid in range(bn.size()):
				if Vals[nodeid] == None:
					parents = bn.parents(nodeid)
					if len(bn.parents(nodeid)) == 0:
						proba = bn.cpt(nodeid)[:]
						proba = np.append(bn.cpt(nodeid)[:-1],1.0-sum(bn.cpt(nodeid)[:-1]))
						proba[proba < 0.0] = 0.0
						if(np.sum(proba) > 1):
								proba = np.round(proba,4)
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
							proba = bn.cpt(nodeid)[dico]
							proba = np.append(bn.cpt(nodeid)[dico][:-1],1.0-sum(bn.cpt(nodeid)[dico][:-1]))
							proba[proba < 0.0] = 0.0
							if(np.sum(proba) > 1):
								proba = np.round(proba,4)
							Vals[nodeid] = np.random.choice(len(proba),1, p = proba)[0]	
		for j in range(len(Vals)):
			Vals[j] = np.random.choice([Vals[j],100],1, p = [1-(pourcManquant/100),(pourcManquant/100)])[0]
		
		if I>0:
			CSV.write('\n')
		for j in range(len(Vals)):
			CSV.write(str(Vals[j]))
			if j<bn.size()-1:
				CSV.write(',')

	CSV.close()
	

