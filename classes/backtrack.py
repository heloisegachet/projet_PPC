from classes.AC3 import AC3
from classes.forward_checking import forward_checking


def backtrack(problem, infos=True):
	if len(problem.inst)==len(problem.var): #toutes les variables sont instanciées (et instanciation réalisable)
		if infos:
			print("solution réalisable")
		return True
	next_var = problem.choose_var() #choisir la prochaine variable à instancier
	dom = problem.current_dom(next_var)
	for next_val in dom:
		problem.params["noeuds tot"] = problem.params.get("noeuds tot", 0)+1
		if infos:
			print("next var", next_var, "next value :", next_val)
			print(problem.inst)
		if not problem.is_FC() and problem.test_inst_var(next_var, next_val, infos):
			problem.inst_var(next_var, next_val) #tester l'instanciation de la variable à valeur et
												 #explorer le sous arbre avec cette instanciation
			problem.params["noeuds internes"] = problem.params.get("noeuds internes", 0)+1
			if backtrack(problem):
				return True
			if infos:
				print("backtrack : ", problem.inst)
			problem.cancel() #si le sous arbre n'a pas d'instanciation valide, on remonte en supprimant
						 #l'instanciation choisie pour la variable en cours
		elif problem.is_FC() and forward_checking(problem, next_var, next_val) and problem.test_inst_var(next_var, next_val, infos):
			problem.inst_var(next_var, next_val)  # tester l'instanciation de la variable à valeur et
			# explorer le sous arbre avec cette instanciation
			problem.params["noeuds internes"] = problem.params.get("noeuds internes", 0) + 1
			if backtrack(problem):
				return True
			if infos:
				print("backtrack : ", problem.inst)
			problem.cancel()  # si le sous arbre n'a pas d'instanciation valide, on remonte en supprimant
			# l'instanciation choisie pour la variable en cours
	return False
