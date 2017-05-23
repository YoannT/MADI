#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils.utils import *

from copy import deepcopy as dc
import pyAgrum as gum
import numpy as np



# Algorithme EM dans un CNB

def learn(nomBIF, nomCSV, nomSave, nbIter):
	"""
	nomBIF: nom du fichier bif du BN
	nomCSV: nom de la base de donnees
	nomSave: nom a donner au fichier bif du BN apres apprentissage
	nbIter: Nombre maximum d'iterations
	"""
	
	bn = gum.BayesNet()
	bn.loadBIF(nomBIF)
	
	CSV = open(nomCSV, 'r')
	lignes = CSV.readlines()
	CSV.close()
	
	iters = 0
	
	# Initialisation aleatoire des parametres
	bn.generateCPTs()
	
	Y = bn.topologicalOrder()[0]
	nomY = bn.variable(Y).name()
	
	while iters < nbIter:
		
		# E sert a stocker des valeurs pendant l'etape E
		E = gum.BayesNet()
		E.loadBIF(nomBIF)
		
		oldcpt = [dc(bn.cpt(n)[:].tolist()) for n in bn.topologicalOrder()]
		print('--------------' + '\n' + 'ITERATION ' + str(iters))
		
		ie = gum.LazyPropagation(bn)
		
		# ETAPE E
		for num, lig in enumerate(lignes):
			l = lig.strip('\n').split(',')
			l = [int(l[i]) for i in range(len(l))]
				
			ie.eraseAllTargets()
			ie.eraseAllEvidence()
			
			# Targets
			targets = set([nomY])
			
			# Evidence
			hard = {bn.variable(i).name(): l[i] for i in bn.topologicalOrder()[1:]}
			
			evidence = dc(hard)
			# Update evidence, set targets, makeInference
			try:
				ie.updateEvidence(evidence)
			except:
				print(num + 1, evidence)
				
			ie.setTargets(targets)
			
			ie.makeInference()
			
			post = ie.posterior(Y)
			
			# Stockage du posterior dans E
			dicos = dico_cpt(post)
			
			for dico in dicos:
				E.cpt(Y)[dico] += post[dico]
				dic = dc(dico)
				dic.update(evidence)
				for nodeid in bn.topologicalOrder()[1:]:
					E.cpt(nodeid)[dic] += post[dico]
				
		print("FIN ETAPE E")
		# ETAPE M
		for nodeid in bn.topologicalOrder():
			if nodeid == Y:
				dics = iter_cpt(bn, nodeid)
				for dic in dics:
					bn.cpt(Y)[dic] = (1.0/len(lignes)) * E.cpt(Y)[dic]
			else:
				dics = iter_cpt(bn, nodeid)
				for dic in dics:
					dicpar = dc(dir)
					dicpar = dc(dic)
					del dicpar[bn.variable(nodeid).name()]
					bn.cpt(nodeid)[dic] = E.cpt(nodeid)[dic] / E.cpt(Y)[dicpar]
		print("FIN ETAPE M")
		
		newcpt = [dc(bn.cpt(n)[:].tolist()) for n in bn.topologicalOrder()]
		
		if oldcpt == newcpt:
			print("CONVERGENCE")
			break
		iters += 1
	printBN(bn)
	
	try:
		# On s'assure que les probas somment a 1
		for nodeid in bn.topologicalOrder():
			dics = iter_parents(bn, nodeid)
			for dic in dics:
				bn.cpt(nodeid)[dic] = np.append(bn.cpt(nodeid)[dic][:-1], [1.0 - sum(bn.cpt(nodeid)[dic][:-1])])
	except:
		pass
	
	bn.saveBIF(nomSave)
	
	# Remplacement d'une chaine de caracteres provoquant un bug a la lecture du .bif
	replace(nomSave,"\"aGrUM_BN\"", "aGrUM_BN")
	
	
	
