import time

from classes.AC3 import AC3
from classes.forward_checking import forward_checking
from classes.AC4 import AC4
import time


def solve(problem, infos=True, max_time = 3600):
    start = time.time()
    if problem.params["root_AC"]:
        if problem.params["AC"] == "AC4":
            AC4(problem, None, infos)
        if problem.params["AC"] == "AC3":
            AC3(problem, None, infos)
    sol, ended = backtrack(problem, 0, infos=infos, max_time = max_time)
    stop = time.time()
    problem.params["time"] = stop - start
    return ended

def backtrack(problem, depth, infos=True, max_time=3600):
    start = time.time()
    if max_time <= 0:
        return False, False
    if len(problem.inst) == len(problem.var):  # toutes les variables sont instanciées (et instanciation réalisable)
        if infos:
            print("solution réalisable")
        return True, True
    next_var = problem.choose_var()  # choisir la prochaine variable à instancier
    dom = problem.ordered(next_var, problem.current_dom(next_var).copy())
    for next_val in dom:
        problem.params["noeuds tot"] = problem.params.get("noeuds tot", 0) + 1
        if infos:
            print("next var", next_var, "next value :", next_val, )
        if problem.test_inst_var(next_var, next_val, infos):
            problem.inst_var(next_var, next_val)  # tester l'instanciation de la variable à valeur et
            # explorer le sous arbre avec cette instanciation
            if infos:
                print("instanciation", problem.inst)
            if (problem.is_MAC() and depth%problem.params["MAC_freq"]!=0) or (not problem.is_MAC() and problem.is_FC()):
                if not forward_checking(problem, infos=infos):
                    problem.cancel()  # si le sous arbre n'a pas d'instanciation valide, on remonte en supprimant
                    # l'instanciation choisie pour la variable en cours
                    continue
            if depth%problem.params["MAC_freq"]==0 and problem.is_MAC():
                if (problem.AC() == "AC3" and not AC3(problem, next_var, infos=infos)) or (
                        problem.AC() == "AC4" and not AC4(problem, next_var, infos=infos)):
                    problem.cancel()  # si le sous arbre n'a pas d'instanciation valide, on remonte en supprimant
                    # l'instanciation choisie pour la variable en cours
                    continue
            problem.params["noeuds internes"] = problem.params.get("noeuds internes", 0) + 1
            sol, ended = backtrack(problem, depth + 1, infos, max_time-time.time()+start)
            #print(sol, ended)
            if sol:
                return True, ended
            if infos:
                print("backtrack : ", problem.inst)
            problem.cancel()  # si le sous arbre n'a pas d'instanciation valide, on remonte en supprimant
            # l'instanciation choisie pour la variable en cours
    return False, max_time-time.time()+start >= 0
