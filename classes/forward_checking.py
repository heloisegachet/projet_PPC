
def forward_checking(problem, var, val, infos=True):
    print("   begin checking")
    incr_index = dict()
    for (y,b) in problem.FC_domain_deletion[var]:
        if not b in problem.current_dom(y):
            incr_index[y] = incr_index.get(y,0)+1
    for y in incr_index.keys():
        problem.dom[y]["index"] += incr_index[y]
    problem.FC_domain_deletion[var] = []
    for y in problem.free_var:
        if infos:
            print("var", y, "domaine", problem.current_dom(y))
        if (var, y) in problem.const:
            i = 0
            while i < problem.dom[y]["index"]:
                b = problem.current_dom(y)[i]
                problem.FC_domain_deletion[var].append((y,b))
                if not problem.const[var, y](val, b):
                    index_domaine = problem.dom[y]["index"]
                    j = i
                    while j < index_domaine-1:
                        problem.dom[y]["dom"][j], problem.dom[y]["dom"][j + 1] = problem.dom[y]["dom"][j + 1], problem.dom[y]["dom"][j]
                        j+=1
                    problem.dom[y]["index"] = index_domaine - 1
                else:
                    i += 1
            if len(problem.current_dom(y)) == 0:
                if infos:
                    print("EMPTY DOMAIN")
                return False
        if infos:
            print("end var", y, "domaine", problem.current_dom(y))
    print("   end checking")
    return True

