#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pyAgrum as gum
import sys

from docutils.nodes import paragraph
from pyAgrum.lib.pretty_print import pretty_cpt

from tempfile import mkstemp
from shutil import move
from os import remove, close

# Distribution equirepartie
def normalDistrib(N):
	"""
	N: longueur de la liste de probabilites a generer
	"""
	res = [1.0/N for i in range(N-1)]
	res.append(1.0-sum(res))
	return res
	
# Distribution aleatoire
def randomDistrib(N):
	"""
	N: longueur de la liste de probabilites a generer
	"""
	res = []
	for i in range(N):
		if i > 0:
			if i == N - 1:
				res.append(1 - sum(res))
			else:
				res.append(round(np.random.uniform(0, 1 - sum(res)), 2))
		else:
			res.append(round(np.random.random(), 2))

	return res

# Fonction pour remplacer un string par un autre dans un fichier
def replace(file_path, pattern, subst):
	"""
	file_path: chemin du fichier ou remplacer
	pattern: string a remplacer
	subst: string de remplacement
	"""
	#Create temp file
	fh, abs_path = mkstemp()
	with open(abs_path,'w') as new_file:
		with open(file_path) as old_file:
			for line in old_file:
				new_file.write(line.replace(pattern, subst))
	close(fh)
	#Remove original file
	remove(file_path)
	#Move new file
	move(abs_path, file_path)

# Fonction retournant le nombre de cas ou une variable a une valeur dans un fichier
def nbCas(nomFic,variable,valeur):
	"""
	nomFic: nom du fichier csv a lire
	variable: variable a observer
	valeur: valeur a observer
	"""
	CSV = open(nomFic, 'r')
	lignes = CSV.readlines()
	CSV.close()
	
	res = 0
	
	for num,lig in enumerate(lignes):
		l = lig.strip('\n').split(',')
		l = [int(l[i]) for i in range(len(l))]
		res += 1 if l[variable] == valeur else 0
	print(res)
	return res

# Affiche un BN
def printBN(bn):
	for nodeid in range(bn.size()):
		print(pretty_cpt(bn.cpt(nodeid)))

# Retourne les dictionnaires des parents d'un nodeid dans le bn
def iter_parents(bn, nodeid):
	"""
	bn: BN a lire
	nodeid: ID de la variable
	"""
	I = gum.Instantiation(bn.cpt(nodeid))
	I.setFirst()
	
	res = []
	
	I.setFirst()
	
	while not I.end():
		lenI = 0
		for i in range(1, I.domainSize()):
			try:
				r = I.variable(i)
				lenI += 1
			except:
				pass
		res.append({I.variable(kk).name(): I.variable(kk).label(I.val(kk)) for kk in range(1, lenI + 1)})
		I.incNotVar(I.variable(0))
	
	return res

# Retourne les dictionnaires associes a un cpt
def dico_cpt(cpt):
	"""
	cpt: cpt a lire
	"""
	I = gum.Instantiation(cpt)
	I.setFirst()
	
	res = []
	
	I.setFirst()
	
	while not I.end():
		lenI = 0
		for i in range(1, I.domainSize()):
			try:
				r = I.variable(i)
				lenI += 1
			except:
				pass
		res.append({I.variable(kk).name(): I.variable(kk).label(I.val(kk)) for kk in range(lenI + 1)})
		I.inc()
	
	return res

# Retourne les dictionnaires associes a un nodeid
def iter_cpt(bn, nodeid):
	"""
	bn: BN a lire
	nodeid: ID de la variable
	"""
	I = gum.Instantiation(bn.cpt(nodeid))
	I.setFirst()
	
	res = []
	
	I.setFirst()
	
	while not I.end():
		lenI = 0
		for i in range(1, I.domainSize()):
			try:
				r = I.variable(i)
				lenI += 1
			except:
				pass
		res.append({I.variable(kk).name(): I.variable(kk).label(I.val(kk)) for kk in range(lenI + 1)})
		I.inc()
	
	return res
