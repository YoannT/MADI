#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import deepcopy as dc

from utils.utils import *

import numpy as np
import pyAgrum as gum
import sys

from pyAgrum.lib.pretty_print import pretty_cpt

from tempfile import mkstemp
from shutil import move
from os import remove, close


# Algorithme EM pour valeurs cachees et variables cachees

def learn(nomBIF, nomCSV, nomSave, nbIter):
	"""
	nomBIF: nom du fichier bif du BN
	nomCSV: nom de la base de donnees
	nomSave: nom a donner au fichier bif du BN apres apprentissage
	nbIter: Nombre maximum d'iterations
	"""
	
	bn = gum.BayesNet()
	bn.loadBIF(nomBIF)
	
	# cp sert pour le comptage
	cp = gum.BayesNet()
	cp.loadBIF(nomBIF)
	
	CSV = open(nomCSV, 'r')
	lignes = CSV.readlines()
	CSV.close()
	
	iters = 0
	
	valInconnue = [0 for i in range(bn.size())]
	parInconnu = [0 for i in range(bn.size())]
	# Premier parcours des lignes de la base
	# MLE pour les variables sans valeur manquante
	
	for nodeid, cache in enumerate(valInconnue):
		parinc = 0
		for lig in lignes:
			l = lig.strip('\n').split(',')
			l = [int(i) for i in l]
			c = l[nodeid]
			parents = bn.parents(nodeid)
			if c != 100:
				if len(bn.parents(nodeid)) == 0:
					cp.cpt(nodeid)[{bn.variable(nodeid).name(): c}] += 1
				else:
					valP = [l[p] for p in parents]
					if all(vp != 100 for vp in valP):
						dico = {bn.variable(nodeid).name(): c}
						for p in parents:
							dico[bn.variable(p).name()] = l[p]
						cp.cpt(nodeid)[dico] += 1
					else:
						parinc += 1
			else:
				if valInconnue[nodeid] == 0:
					valInconnue[nodeid] = 1
				if len(bn.parents(nodeid)) == 0:
					valP = [l[p] for p in parents]
					if not all(vp != 100 for vp in valP):
						parinc += 1
		if parinc >= len(lignes):
			parInconnu[nodeid] = 1
			

	print("CACHE", valInconnue)
	print("PARENTS INCONNUS", parInconnu)
			
	print("FIN MLE")
	
	# Normalisation des cpts
	for nodeid in range(bn.size()):
		dics = iter_cpt(bn, nodeid)
		for dic in dics:
			dicpar = dc(dic)
			del dicpar[bn.variable(nodeid).name()]
			dividende = np.sum(cp.cpt(nodeid)[dicpar])
			if dividende != 0:
				bn.cpt(nodeid)[dic] = cp.cpt(nodeid)[dic] / dividende
			else:
				bn.cpt(nodeid)[dic] = 0
	
	while iters < nbIter:
		
		# E sert a stocker des valeurs pendant l'etape E
		E = gum.BayesNet()
		E.loadBIF(nomBIF)
		
		oldcpt = [dc(bn.cpt(n)[:].tolist()) for n in bn.topologicalOrder()]
		print('--------------' + '\n' + 'ITERATION ' + str(iters))
		if iters == 0:
			# Initialisation aleatoire et remplissage de cp avec les cas connus pour les variables:
			# - ayant une valeur inconnue
			# - cachees
			# - dont l'un des parents est une variable cachee
			for nodeid in bn.topologicalOrder():
				
				if valInconnue[nodeid] == 1 or parInconnu[nodeid] == 1:
					parents = bn.parents(nodeid)
					if len(parents) == 0:
						bn.cpt(nodeid)[:] = randomDistrib(len(bn.cpt(nodeid)[:]))
						cp.cpt(nodeid)[:] = [0 for i in range(len(cp.cpt(nodeid)[:]))]
						for ligne in lignes:
							li = ligne.strip('\n').split(',')
							li = [int(li[i]) for i in range(len(li))]
							if li[nodeid] != 100:
								cp.cpt(nodeid)[li[nodeid]] += 1
					else:
						dicosP = iter_parents(bn, nodeid)
						
						for dico in dicosP:
							bn.cpt(nodeid)[dico] = randomDistrib(len(bn.cpt(nodeid)[dico]))
							cp.cpt(nodeid)[dico] = [0 for i in range(len(cp.cpt(nodeid)[dico]))]
							
							tabsum = [0 for i in range(len(cp.cpt(nodeid)[dico]))]
							
							for ligne in lignes:
								li = ligne.strip('\n').split(',')
								li = [int(li[i]) for i in range(len(li))]
								if li[nodeid] != 100 and all(li[cp.idFromName(d)] == int(dico[d]) for d in dico):
									tabsum[li[nodeid]] += 1
							cp.cpt(nodeid)[dico] = tabsum
			print("INITIALISATION FINIE")
		
		ie = gum.LazyPropagation(bn)
		
		# ETAPE E
		for num, lig in enumerate(lignes):
			l = lig.strip('\n').split(',')
			l = [int(l[i]) for i in range(len(l))]
			if 100 in l:
				unk = [i for i, x in enumerate(l) if x == 100]
				unk.extend([i for i in bn.topologicalOrder() if parInconnu[i] == 1])
				unk = list(set(unk))
				if len(unk) < 4:
					ie.eraseAllTargets()
					ie.eraseAllEvidence()
				
					# Targets
					unknames = [bn.variable(i).name() for i in unk]
					targets = set(unknames)
				
					# Evidence
					k = [i for i, x in enumerate(l) if x != 100]
					hard = {bn.variable(i).name(): l[i] for i in k}
				
					soft = {}
					for i in unk:
						if not isinstance(bn.cpt(i)[hard][0], list) and not isinstance(bn.cpt(i)[hard][:][0],np.ndarray):
							soft[bn.variable(i).name()] = bn.cpt(i)[hard]
						
					evidence = hard
					# Update evidence, set targets, makeInference
					try:
						ie.updateEvidence(evidence)
					except:
						print(num + 1, evidence)
					
					ie.setTargets(targets)
				
					ie.eraseAllJointTargets()

					if len(unk) > 1:
						ie.addJointTarget(unk)
					ie.makeInference()
					if len(unk) > 1:
						post = ie.jointPosterior(unk)
					else:
						post = ie.posterior(unk[0])
					
					# Stockage du posterior dans E
				
					dicos = dico_cpt(post)
					for u in unk:
						for dico in dicos:
							E.cpt(u)[dico] += post[dico]
						
		print("FIN ETAPE E")
		# ETAPE M
		for nodeid in bn.topologicalOrder():
			if valInconnue[nodeid] == 1 or parInconnu[nodeid] == 1:
				dics = iter_cpt(bn, nodeid)
				for dic in dics:
					dicpar = dc(dic)
					del dicpar[bn.variable(nodeid).name()]
					dividende = np.sum(E.cpt(nodeid)[dicpar]) + np.sum(cp.cpt(nodeid)[dicpar])
					if dividende != 0:
						bn.cpt(nodeid)[dic] = (E.cpt(nodeid)[dic] + cp.cpt(nodeid)[dic]) / dividende
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
	
	replace(nomSave,"\"aGrUM_BN\"", "aGrUM_BN")
	
