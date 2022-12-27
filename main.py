# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np

def parse_graph(filepath):
	file = open(filepath, 'r')
	lines = file.readlines()
	# rien sur les 3 premières lignes, n et 2*m sur la 4e
	info = lines[3].replace('\n', '').split(' ')
	# nombre de sommets
	n = int(info[2])
	# nombre d'arêtes
	m = int(info[3])//2
	E = np.zeros((n,n))
	for i in range(4, len(lines)):
		line = lines[i].replace('\n', '').split(' ')
		nodes = [int(p) for p in line if p.isdigit()]
		# indices de 1 à n dans le fichier, 0 à n-1 dans le programme
		E[nodes[0]-1, nodes[1]-1]=1
	file.close()
	return E

def diff(x,y):
	return x!=y

def diag(x,y,i,j):
	return ((x-y)!=np.abs(i-j))&((x-y)!=-np.abs(i-j))

class csp:
	# classe représentant un problème

	def __init__(self):
		self.var = list()
		self.dom = dict()
		self.const = dict()
		self.inst = list()
		self.free_var = list()

	def add_alldiff(self):
		n = len(self.var)
		for i in range(n):
			for j in range(i+1,n):
				self.const[self.var[i], self.var[j]].append(diff)
	
	def n_queens(self, n):
		self.var = [i for i in range(1,n+1)]
		self.free_var = [i for i in range(1,n+1)]
		for x in self.var:
			self.dom[x] = np.arange(1,n+1)
		for i in range(1, n+1):
			for j in range(i+1,n+1):
				self.const[i, j] = list()
		for i in range(1,n+1):
			for j in range(i+1,n+1):
				self.const[i, j].append(lambda x, y : diag(x,y,i,j))
		self.add_alldiff()

	def colorability(self, E):
		n = E.shape[0]
		self.var = [i for i in range(n)]
		self.free_var = [i for i in range(n)]
		# peut être affiné par le degré max
		for x in self.var:
			self.dom[x] = np.arange(n)
		for i in range(n):
			for j in range(i+1,n):
				self.const[self.var[i], self.var[j]] = list()
				if E[i,j]==1:
					self.const[self.var[i], self.var[j]].append(diff)
	
	def inst_var(self, x, v):
		self.free_var.remove(x)
		self.inst.append((x,v))
	
	def choose_var(self, method='default'):
		if method=='default':
			return self.free_var[0]

	def test_inst(self):
		if len(self.inst)<2:
			return True
		last_var = self.inst[-1][0]
		last_val = self.inst[-1][1]
		for i in range(len(self.inst)-1):
			x = self.inst[i][0]
			x_val = self.inst[i][1]
			if x < last_var and len(self.const[x, last_var])>0:
				for constraint in self.const[x, last_var]:
					if (constraint(x_val, last_val)==False):
						return False
			elif x > last_var and len(self.const[last_var, x])>0:
				for constraint in self.const[last_var, x]:
					if (constraint(last_val, x_val)==False):
						return False
		return True

	def cancel(self):
		last_var = self.inst.pop()[0]
		self.free_var.append(last_var)


instance_type = "n_reines"

def build_domaines(instance):
	if instance_type == "n_reines":
		n = instance
		domaines = dict()
		for i in range(n):
			domaines[i] = (np.arange(1,n+1), n)
	return domaines

def build_constraints(instance):
	if instance_type == "n_reines":
		tab = build_constraints_n_reines(instance)
	if instance_type == "colorabilite":
		tab = build_constraints_color(instance)
	return tab

def build_constraints_color(n, E):
	tab_constraints = dict()
	for i in range(n):
		for j in range(n):
			if E[i,j] ==1:
				tab_constraints[i, j] = lambda val1, val2: alldiff(i, j, val1, val2)
	return tab_constraints


def build_constraints_n_reines(n):
	tab_constraints = dict()
	for i in range(n):
		for j in range(i+1, n):
			tab_constraints[i,j] = lambda val1, val2 : constraint_diag_1(i,j, val1, val2)
			tab_constraints[i,j] = lambda val1, val2 : constraint_diag_2(i,j, val1, val2)
			tab_constraints[i,j] = lambda val1, val2 : alldiff(i,j, val1, val2)
	return tab_constraints

def constraint_diag_1(i,j,val_i,val_j):
	return val_i - val_j != np.abs(i-j)

def constraint_diag_2(i,j,val_i,val_j):
	return val_i - val_j != -np.abs(i-j)

def alldiff(i, j, val_i, val_j):
	return val_i != val_j

def backtrack_test(problem):
	if problem.test_inst() == False:
		return False
	if len(problem.inst)==len(problem.var):
		return True
	next_var = problem.choose_var()
	dom = problem.dom[next_var]
	for next_val in dom:
		problem.inst_var(next_var, next_val)
		if backtrack_test(problem):
			return True
		problem.cancel()
	return False

def solver_test():
	problem=csp()
	E = parse_graph("david.col")
	problem.colorability(E)
	backtrack_test(problem)
	# check solution for colorability
	solution = problem.inst
	# transformation en dico parce que plus facile
	sol= dict()
	# for (x,v) in solution:
	# 	sol[x] = v
	# n = E.shape[0]
	# for i in range(n):
	# 	for j in range(n):
	# 		if (E[i][j]==1) and sol[i]==sol[j]:
	# 			print('aie aie aie')
	print(sol)


def backtrack(variables_instanciees, variables_non_instanciees,  domaines, contraintes):
	#domaines : dictionnaire de tuple (numpy array des valeurs possibles, indice de fin de domaine)
	#on donne une instanciation valide
	if len(variables_instanciees) >= 2:
		contrainte_violee = test_toutes_contraintes(variables_instanciees[:-1], variables_instanciees[-1][0], variables_instanciees[-1][1], contraintes)
		if contrainte_violee:
			print("pb contrainte")
			return False, None
	if len(variables_instanciees) == len(domaines):
		return True, variables_instanciees
	print(variables_instanciees, variables_non_instanciees)
	index_variable = choose_var_non_instanciee(variables_non_instanciees)
	valeurs_domaine_order = order_values(domaines[index_variable])

	for valeur in valeurs_domaine_order:
		print(index_variable, valeur)
		variables_instanciees_temp = variables_instanciees.copy()
		variables_non_instanciees_temp = variables_non_instanciees.copy()
		variables_instanciees_temp.append((index_variable, valeur))
		variables_non_instanciees_temp.remove(index_variable)
		backtrack_val = backtrack(variables_instanciees_temp,variables_non_instanciees_temp, domaines, contraintes)
		if backtrack_val[0]:
			print("backtrack")
			return backtrack_val
	return False, None

def choose_var_non_instanciee(variables_non_instanciees):
	return variables_non_instanciees[0]

def order_values(domaines):
	return domaines[0]

def test_toutes_contraintes(variables_instanciees, index_variable, valeur, contraintes):
	for (var_1, val_1) in variables_instanciees:
		for fonction in contraintes[var_1, index_variable]:
			if(not fonction(val_1, valeur)):
				return True
	return False

def AC3(domaines, contraintes):
	aTester = list(contraintes.keys()).copy()
	while len(aTester)!=0:
		x,y = aTester.pop()
		isSupportee = True
		for val_x in domaines[x][0]:
			value_isSupportee = checkSupport(x, val_x, y, domaines, contraintes[x,y])
			if not value_isSupportee:
				#domaine x <- domaine  de x - valeur val_x
				#########TO DO
				for elem in contraintes.keys():
					if elem[0]==x and elem[1]!=y:
						aTester.append((elem[1],x))

def checkSupport(x, val_x, y, domaines, function):
	value_isSupportee = False
	for val_y in domaines[y][0]:
		value_isSupportee = value_isSupportee or function(val_x, val_y)
	return value_isSupportee


def solveur():
	instance = 8
	domaines = build_domaines(instance)
	contraintes = build_constraints(instance)
	print(backtrack([], list(domaines.keys()), domaines, contraintes))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	solver_test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
