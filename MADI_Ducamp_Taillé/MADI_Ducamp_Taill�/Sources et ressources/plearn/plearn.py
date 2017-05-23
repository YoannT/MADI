#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
import pyAgrum as gum
from pyAgrum.lib.pretty_print import pretty_cpt
import numpy as np
import genere
import matplotlib.pyplot as plt

# Apprentissage a partir d'une base complete
def learn (nomBIF,nomCSV,nomSave):
	"""
	nomBIF: nom du fichier bif a lire
	nomCSV: nom du fichier csv a lire
	nomSave: nom du fichier bif ou sauvegarder le BN genere
	"""
	
	bn = gum.BayesNet()
	bn.loadBIF(nomBIF)
	CSV = open(nomCSV,'r')
	lignes = CSV.readlines()
	CSV.close()

	for lig in lignes:
		l = lig.strip('\n').split(',')
		for nodeid,c in enumerate(l):
			parents = bn.parents(nodeid)
			if len(bn.parents(nodeid)) == 0:
				bn.cpt(nodeid)[{bn.variable(nodeid).name():c}] += 1
			else:
				dico = {bn.variable(nodeid).name():c}
				for p in parents:
					dico[bn.variable(p).name()] = int(l[p])
				bn.cpt(nodeid)[dico] += 1

	for nodeid in range(bn.size()):
		bn.cpt(nodeid).normalize()
	
	bn.saveBIF(nomSave)
