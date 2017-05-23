#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import pyAgrum as gum
from pyAgrum.lib.pretty_print import pretty_cpt
import numpy as np

def genererCSV(N,nomCSV,nomBIF):
	"""
	N: nombre de lignes
	nomCSV: nom du fichier csv enregistrer
	nomBIF: nom du fichier bif a lire
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
						proba = [p for p in proba[:-1]]
						proba += [1-sum(proba)]
						valPoss = [i for i in range(len(proba))]
						Vals[nodeid] = np.random.choice(valPoss,1, p = proba)[0]
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
							proba = [p for p in proba[:-1]]
							proba += [1-sum(proba)]
							valPoss = [i for i in range(len(proba))]
							Vals[nodeid] = np.random.choice(valPoss,1, p = proba)[0]				

		if I>0:
			CSV.write('\n')
		for j in range(len(Vals)):
			CSV.write(str(Vals[j]))
			if j<5:
				CSV.write(',')
	CSV.close()
