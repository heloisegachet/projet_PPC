import numpy as np
from classes.csp import csp
from classes.backtrack import solve
import time
import matplotlib.pyplot as plt
import os

def parse_graph(filepath):
	file = open(filepath, 'r')
	lines = file.readlines()
	info = lines[3].replace('\n', '').split(' ')
	n = int(info[2])
	m = int(info[3]) // 2
	E = np.zeros((n, n))
	for i in range(4, len(lines)):
		line = lines[i].replace('\n', '').split(' ')
		nodes = [int(p) for p in line if p.isdigit()]
		E[nodes[0] - 1, nodes[1] - 1] = 1
		E[nodes[1] - 1, nodes[0] - 1] = 1
	file.close()
	return E


def solver_test(type_instance, instance, params, plot_table):
	if type_instance == "n_queens":
		problem = csp()
		problem.n_queens(instance, params)
		solve(problem)
		print("solution finale pour ",instance, problem.inst)
		print(problem.params)
		plot_table["time"].append(problem.params["time"])
		plot_table["nb_nodes"].append(problem.params["noeuds tot"])
		return problem
	if type_instance == "colorability":
		start = time.time()
		colors = int(np.max(np.sum(instance, axis=0))) + 1
		while colors > 0:
			problem = csp()
			problem.colorability(instance, colors, params)
			solve(problem)
			if len(problem.inst) == 0:
				pb_vide_params = problem.params.copy()
				break
			colors -= 1
			sol = problem.inst.copy()
			sol_params = problem.params.copy()
		stop = time.time()
		print("nb colors", colors+1)
		print("sol", sol)
		print(sol_params)
		print("not colorable", colors)
		print("params", pb_vide_params)
		print("time tot : ", stop - start)
		plot_table["time_sol"].append(sol_params["time"])
		plot_table["nb_nodes_sol"].append(sol_params["noeuds tot"])
		plot_table["time_last"].append(pb_vide_params["time"])
		plot_table["nb_nodes_last"].append(pb_vide_params["noeuds tot"])
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
	times = dict()
	range_n = range(4,24)
	plot_dict["backtrack"] = {"n":[],"time":[], "nb_nodes":[]}
	times["backtrack"] = 0
	plot_dict["FC"] = {"n": [], "time": [], "nb_nodes": []}
	times["FC"] = 0
	freq_table = [1,2,5,10]
	for key in ["MAC3"]:#, "MAC4"]:
		for freq in freq_table:
			times[key+"-"+str(freq)] = 0
			plot_dict[key+"-"+str(freq)] = {"n": [], "time": [], "nb_nodes": []}
	time_max = 10
	for n in range_n:
		if times["backtrack"]<time_max:
			type_instance = "n_queens"
			params = {"is_FC": False, "is_MAC": False, "AC": "AC3", "root_AC": True, "choose_var": "default",
				  "choose_val": "default", "MAC_freq":1}
			problem = solver_test(type_instance, n, params, plot_dict["backtrack"])
			times["backtrack"] = problem.params["time"]
			plot_dict["backtrack"]["n"].append(n)
			print()
		#for AC in ["AC3", "AC4"]:
		#	params = {"is_FC": False, "is_MAC": False, "AC": AC, "root_AC": True, "choose_var": "default",
		#			  "choose_val": "default"}
		#	solver_test(type_instance, n, params, plot_dict["root"+AC])
		#	print()
		print("TEST FC")
		if times["FC"]<time_max:
			params = {"is_FC": True, "is_MAC": False, "AC": "AC3", "root_AC": True, "choose_var": "default",
				  "choose_val": "default", "MAC_freq":1}
			problem = solver_test(type_instance, n, params, plot_dict["FC"])
			print()
			times["FC"] = problem.params["time"]
			plot_dict["FC"]["n"].append(n)

		for AC in ["AC3"]:#, "AC4"]:
			for freq in freq_table:
				if times["M"+AC+"-"+str(freq)] < time_max:
					print("TEST MAC ",AC, "freq",freq)
					params = {"is_FC": False, "is_MAC": True, "AC": AC, "root_AC": True, "choose_var": "default",
					  "choose_val": "default", "MAC_freq":freq}
					problem = solver_test(type_instance, n, params, plot_dict["M"+AC+"-"+str(freq)])
					times["M"+AC+"-"+str(freq)] = problem.params["time"]
					print()
					plot_dict["M"+AC+"-"+str(freq)]["n"].append(n)

	plt.figure(figsize = (15,15))
	for key in plot_dict.keys():
		plt.plot(plot_dict[key]["n"], plot_dict[key]["time"], label=key)
	plt.legend(loc="upper left")
	plt.ylabel("Solving time")
	plt.xlabel("n")
	plt.show()
	plt.figure(figsize=(15,15))
	for key in plot_dict.keys():
		plt.plot(plot_dict[key]["n"], plot_dict[key]["nb_nodes"], label=key)
	plt.legend(loc="upper left")
	plt.ylabel("Number of nodes")
	plt.xlabel("n")
	plt.show()


def test_n_queen_heuristic():
	plot_dict = dict()
	times = dict()
	range_n = range(4,24)
	for choose_var in ['random', "smallest_dom"]:
		for choose_val in ["default", "const_max"]:
			plot_dict[choose_var+" "+choose_val] = {"n":[],"time":[], "nb_nodes":[]}
			times[choose_var+" "+choose_val] = 0
	time_max = 10
	for n in range_n:
		for choose_var in ['random', "smallest_dom"]:
			for choose_val in ["default", "const_max"]:
				if times[choose_var+" "+choose_val]<time_max:
					type_instance = "n_queens"
					params = {"is_FC": True, "is_MAC": False, "AC": "AC3", "root_AC": True, "choose_var": choose_var,
					  "choose_val": choose_val, "MAC_freq":1}
					problem = solver_test(type_instance, n, params, plot_dict[choose_var+" "+choose_val])
					times[choose_var+" "+choose_val] = problem.params["time"]
					plot_dict[choose_var+" "+choose_val]["n"].append(n)
					print()

	plt.figure()
	for key in plot_dict.keys():
		plt.plot(plot_dict[key]["n"], plot_dict[key]["time"], label=key)
	plt.legend(loc="upper left")
	plt.ylabel("Solving time")
	plt.xlabel("n")
	plt.show()
	plt.figure()
	for key in plot_dict.keys():
		plt.plot(plot_dict[key]["n"], plot_dict[key]["nb_nodes"], label=key)
	plt.legend(loc="upper left")
	plt.ylabel("Number of nodes")
	plt.xlabel("n")
	plt.show()



def test_colorability_best_method():
	plot_dict = dict()
	filenames = []
	plot_dict["FC"] = {"file": [], "time_sol": [], "nb_nodes_sol": [], "time_last": [], "nb_nodes_last": []}
	freq_table = [1,3]
	for key in ["MAC3","MAC4"]:
		for freq in freq_table:
			plot_dict[key+"-"+str(freq)] = {"file": [], "time_sol": [], "nb_nodes_sol": [], "time_last": [], "nb_nodes_last": []}
	for file in os.listdir("Instances"):
		print(file)
		instance = "Instances/"+file
		filenames.append(file)
		E = parse_graph(instance)
		type_instance = "colorability"

		print("TEST FC")
		params = {"is_FC": True, "is_MAC": False, "AC": "AC3", "root_AC": True, "choose_var": "default",
			  "choose_val": "default", "MAC_freq":1}
		solver_test(type_instance, E, params, plot_dict["FC"])
		print()
		plot_dict["FC"]["file"].append(file)

		for AC in ["AC3", "AC4"]:
			for freq in freq_table:
				print("TEST MAC ",AC, "freq",freq)
				params = {"is_FC": False, "is_MAC": True, "AC": AC, "root_AC": True, "choose_var": "default",
				  "choose_val": "default", "MAC_freq":freq}
				solver_test(type_instance, E, params, plot_dict["M"+AC+"-"+str(freq)])
				plot_dict["M"+AC+"-"+str(freq)]["file"].append(file)
				print()

	plt.figure(figsize=(15, 15))
	for key in plot_dict.keys():
		plt.plot(filenames, plot_dict[key]["time_sol"], label=key)
	plt.legend(loc="upper left")
	plt.ylabel("Solving time best coloration")
	plt.xlabel("Instance")
	plt.show()

	plt.figure(figsize=(15, 15))
	for key in plot_dict.keys():
		plt.plot(filenames, plot_dict[key]["time_last"], label=key)
	plt.legend(loc="upper left")
	plt.ylabel("Solving time verify optimality")
	plt.xlabel("Instance")
	plt.show()

	plt.figure(figsize=(15, 15))
	for key in plot_dict.keys():
		plt.plot(filenames, plot_dict[key]["nb_nodes_sol"], label=key)
	plt.legend(loc="upper left")
	plt.ylabel("Number of nodes best coloration")
	plt.xlabel("Instance")

	plt.figure(figsize=(15, 15))
	for key in plot_dict.keys():
		plt.plot(filenames, plot_dict[key]["nb_nodes_last"], label=key)
	plt.legend(loc="upper left")
	plt.ylabel("Number of nodes verify optimality")
	plt.xlabel("Instance")

	plt.show()

def test_color_heuristic_var():
	plot_dict = dict()
	filenames = []
	for choose_var in ["default", "smallest_dom", "biggest_const", "biggest_const_non_inst"]:
		plot_dict[choose_var] = {"time_sol":[], "nb_nodes_sol":[],"time_last":[], "nb_nodes_last":[]}
	for file in os.listdir("Instances"):
		print(file)
		instance = "Instances/"+file
		filenames.append(file)
		E = parse_graph(instance)
		type_instance = "colorability"
		for choose_var in ["default", "smallest_dom", "biggest_const", "biggest_const_non_inst"]:
			print(choose_var)
			params = {"is_FC": True, "is_MAC": False, "AC": "AC3", "root_AC": True, "choose_var": choose_var,
				  "choose_val": "default", "MAC_freq":1}
			solver_test(type_instance, E, params, plot_dict[choose_var])
			print()
	plt.figure()
	for key in plot_dict.keys():
		plt.plot(filenames, plot_dict[key]["time_sol"], label=key)
	plt.legend(loc="upper left")
	plt.ylabel("Solving time best coloration")
	plt.xlabel("Instance")
	plt.show()

	plt.figure()
	for key in plot_dict.keys():
		plt.plot(filenames, plot_dict[key]["time_last"], label=key)
	plt.legend(loc="upper left")
	plt.ylabel("Solving time verify optimality")
	plt.xlabel("Instance")
	plt.show()

	plt.figure()
	for key in plot_dict.keys():
		plt.plot(filenames, plot_dict[key]["nb_nodes_sol"], label=key)
	plt.legend(loc="upper left")
	plt.ylabel("Number of nodes best coloration")
	plt.xlabel("Instance")

	plt.figure()
	for key in plot_dict.keys():
		plt.plot(filenames, plot_dict[key]["nb_nodes_last"], label=key)
	plt.legend(loc="upper left")
	plt.ylabel("Number of nodes verify optimality")
	plt.xlabel("Instance")
	plt.show()

def test_color_heuristic_val():
	plot_dict = dict()
	filenames = []
	for choose_var in ["smallest_dom"]:
		for choose_val in ["default", "const_max"]:
			plot_dict[choose_val+" "+choose_var] = {"time_sol":[], "nb_nodes_sol":[],"time_last":[], "nb_nodes_last":[]}
	for file in os.listdir("Instances"):
		print(file)
		instance = "Instances/"+file
		filenames.append(file)
		E = parse_graph(instance)
		type_instance = "colorability"
		for choose_var in ["smallest_dom"]:
			for choose_val in ["default", "const_max"]:
				print(choose_val)
				params = {"is_FC": True, "is_MAC": False, "AC": "AC3", "root_AC": True, "choose_var": choose_var,
					  "choose_val": choose_val, "MAC_freq":1}
				solver_test(type_instance, E, params, plot_dict[choose_val+" "+choose_var])
				print()
	plt.figure()
	for key in plot_dict.keys():
		plt.plot(filenames, plot_dict[key]["time_sol"], label=key)
	plt.legend(loc="upper left")
	plt.ylabel("Solving time best coloration")
	plt.xlabel("Instance")
	plt.show()

	plt.figure()
	for key in plot_dict.keys():
		plt.plot(filenames, plot_dict[key]["time_last"], label=key)
	plt.legend(loc="upper left")
	plt.ylabel("Solving time verify optimality")
	plt.xlabel("Instance")
	plt.show()

	plt.figure()
	for key in plot_dict.keys():
		plt.plot(filenames, plot_dict[key]["nb_nodes_sol"], label=key)
	plt.legend(loc="upper left")
	plt.ylabel("Number of nodes best coloration")
	plt.xlabel("Instance")

	plt.figure()
	for key in plot_dict.keys():
		plt.plot(filenames, plot_dict[key]["nb_nodes_last"], label=key)
	plt.legend(loc="upper left")
	plt.ylabel("Number of nodes verify optimality")
	plt.xlabel("Instance")

	plt.show()

def test_n_queen():
	range_n = range(4, 71)
	params = {"is_FC": True, "is_MAC": False, "AC": "AC3", "root_AC": True, "choose_var": "smallest_dom",
			  "choose_val": "default", "MAC_freq": 1}
	plot_table = {"time":[], "nb_nodes":[], "n":[]}
	for n in range_n:
		problem = csp()
		problem.n_queens(n, params)
		ended = solve(problem, max_time=30)
		if not ended:
			print(n, "NOPE")
		plot_table["time"].append(problem.params["time"])
		plot_table["nb_nodes"].append(problem.params["noeuds tot"])
		plot_table["n"].append(n)

	plt.figure()
	plt.plot(plot_table["n"], plot_table["time"])
	plt.ylabel("Solving time")
	plt.xlabel("n")
	plt.show()

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.plot(plot_table["n"], plot_table["nb_nodes"])
	plt.ylabel("Number of nodes")
	ax.set_yscale('log')
	plt.xlabel("n")
	plt.show()


def test_colorability():
	filenames = []
	params = {"is_FC": True, "is_MAC": False, "AC": "AC3", "root_AC": True, "choose_var": "smallest_dom",
			  "choose_val": "default", "MAC_freq": 1}
	for file in os.listdir("Instances 500/"):
		print(file)
		instance = "Instances 500/" + file
		filenames.append(file)
		E = parse_graph(instance)
		colors = int(np.max(np.sum(E, axis=0))) + 1
		while colors > 0:
			problem = csp()
			problem.colorability(E, colors, params)
			ended = solve(problem, max_time=30)
			if not ended:
				print("NOT ENDED")
				break
			if len(problem.inst) == 0:
				print("optimality found")
				break
			colors -= 1
			sol_params = problem.params.copy()
		print("best color", colors+1, "branches",sol_params["noeuds internes"])


if __name__ == '__main__':
	#test_n_queen_best_method()
	#test_colorability_best_method()
	#test_n_queen_heuristic()
	#test_color_heuristic_var()
	#test_color_heuristic_val()
	#test()
	test_colorability()
