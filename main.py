# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
from classes.csp import csp
from classes.backtrack import solve
import time
import matplotlib.pyplot as plt

def parse_graph(filepath):
	file = open(filepath, 'r')
	lines = file.readlines()
	# rien sur les 3 premières lignes, n et 2*m sur la 4e
	info = lines[3].replace('\n', '').split(' ')
	# nombre de sommets
	n = int(info[2])
	# nombre d'arêtes
	m = int(info[3]) // 2
	E = np.zeros((n, n))
	for i in range(4, len(lines)):
		line = lines[i].replace('\n', '').split(' ')
		nodes = [int(p) for p in line if p.isdigit()]
		# indices de 1 à n dans le fichier, 0 à n-1 dans le programme
		E[nodes[0] - 1, nodes[1] - 1] = 1
		E[nodes[1] - 1, nodes[0] - 1] = 1
	file.close()
	return E


def solver_test(type_instance, instance, params, plot_table):
	if type_instance == "n_queens":
		problem = csp()
		problem.n_queens(instance, params)
		solve(problem, infos=False)
		print("solution finale pour ",instance, problem.inst)
		print(problem.params)
		plot_table["time"].append(problem.params["time"])
		plot_table["nb_nodes"].append(problem.params["noeuds tot"])
	if type_instance == "colorability":
		start = time.time()
		colors = int(np.max(np.sum(instance, axis=0))) + 1
		while colors > 0:
			problem = csp()
			problem.colorability(instance, colors, params)
			solve(problem, infos=False)
			if len(problem.inst) == 0:
				pb_vide_params = problem.params.copy()
				break
			colors -= 1
			sol = problem.inst.copy()
			sol_params = problem.params.copy()
		stop = time.time()
		print("nb colors", colors+1)
		print("sol", sol)
		# problem.colorability_solution(E)
		print(sol_params)
		print("not colorable", colors)
		print("params", pb_vide_params)
		print("time tot : ", stop - start)
	else:
		print("problem")

def test_with_params(params, type_instance):
	if type_instance == "colorability":
		instance = parse_graph("myciel4.col")
		solver_test(type_instance, instance, params)
	if type_instance == "n_queens":
		solver_test(type_instance, instance, params)

def test_n_queen_best_method():
	plot_dict = dict()
	for key in ["backtrack", "rootAC3", "rootAC4", "FC", "MAC3", "MAC4"]:
		plot_dict[key] = {"time":[], "nb_nodes":[]}
	range_n = range(4,17)
	for n in range_n:
		type_instance = "n_queens"
		params = {"is_FC": False, "is_MAC": False, "AC": "AC3", "root_AC": False, "choose_var": "default",
				  "choose_val": "default"}
		solver_test(type_instance, n, params, plot_dict["backtrack"])
		print()
		for AC in ["AC3", "AC4"]:
			params = {"is_FC": False, "is_MAC": False, "AC": AC, "root_AC": True, "choose_var": "default",
					  "choose_val": "default"}
			solver_test(type_instance, n, params, plot_dict["root"+AC])
			print()
		print("TEST FC")
		params = {"is_FC": True, "is_MAC": False, "AC": AC, "root_AC": False, "choose_var": "default",
				  "choose_val": "default"}
		solver_test(type_instance, n, params, plot_dict["FC"])
		print()
		for AC in ["AC4", "AC3"]:
			print("TEST MAC ",AC)
			params = {"is_FC": False, "is_MAC": True, "AC": AC, "root_AC": False, "choose_var": "default",
					  "choose_val": "default"}
			solver_test(type_instance, n, params, plot_dict["M"+AC])
			print()

	plt.figure()
	for key in plot_dict.keys():
		print(plot_dict[key])
		plt.plot([n for n in range_n], plot_dict[key]["time"], label=key)
	plt.legend(loc="upper left")
	plt.show()
	plt.figure()
	for key in plot_dict.keys():
		plt.plot([n for n in range_n], plot_dict[key]["nb_nodes"], label=key)
	plt.legend(loc="upper left")
	plt.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	test_n_queen_best_method()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
