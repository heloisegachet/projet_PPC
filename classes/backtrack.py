from classes.AC3 import AC3
from classes.forward_checking import forward_checking
from classes.AC4 import AC4

def backtrack(problem, infos=True):
	if problem.empty_dom():
		return False
	if len(problem.inst)==len(problem.var): #toutes les variables sont instanciées (et instanciation réalisable)
		if infos:
			print("solution réalisable")
		return True
	next_var = problem.choose_var() #choisir la prochaine variable à instancier
	dom = problem.current_dom(next_var)
	index = 0
	while index < problem.dom[next_var]["index"]:
		next_val = problem.current_dom(next_var)[index]
		problem.params["noeuds tot"] = problem.params.get("noeuds tot", 0)+1
		if infos:
			print("next var", next_var, "next value :", next_val)
		if problem.test_inst_var(next_var, next_val, infos):
			problem.inst_var(next_var, next_val) #tester l'instanciation de la variable à valeur et
												 #explorer le sous arbre avec cette instanciation
			if infos:
				print("instanciation", problem.inst)
			if problem.is_FC():
				if not forward_checking(problem):
					return False
			if problem.is_MAC:
				 AC4(problem)
			problem.params["noeuds internes"] = problem.params.get("noeuds internes", 0)+1
			if backtrack(problem):
				index+=1
				return True
			if infos:
				print("backtrack : ", problem.inst)
			problem.cancel() #si le sous arbre n'a pas d'instanciation valide, on remonte en supprimant
						 #l'instanciation choisie pour la variable en cours
	return False
