# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
from classes.csp import csp
from classes.backtrack import solve
from classes.AC3 import AC3
from classes.AC4 import AC4

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
		E[nodes[1] - 1, nodes[0] - 1] = 1
	file.close()
	return E


def solver_test(type_instance):
	is_FC = False
	is_MAC = True
	AC = "AC3"
	problem=csp()
	if type_instance == "n_queens":
		n=8
		problem.n_queens(n, is_FC, is_MAC, AC)
		solve(problem, infos=True)
		print("solution finale : ", problem.inst)
		problem.n_queens_solution(n)
		print(problem.params)
	if type_instance == "colorability":
		E = parse_graph("myciel4.col")
		colors = 0
		while True:
			problem.colorability(E, colors, is_FC, is_MAC, AC)
			solve(problem, infos=False)
			if len(problem.inst)!=0:
				print("nb colors", colors)
				print("solution finale : ", problem.inst)
				break
			colors += 1
		#problem.colorability_solution(E)
		print(problem.params)
	else:
		print("problem")
	#problem.colorability_solution(E)
	# check solution for colorability
	# transformation en dico parce que plus facile
	#sol= dict()
	# for (x,v) in solution:
	# 	sol[x] = v
	# n = E.shape[0]
	# for i in range(n):
	# 	for j in range(n):
	# 		if (E[i][j]==1) and sol[i]==sol[j]:
	# 			print('aie aie aie')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	solver_test("colorability")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
