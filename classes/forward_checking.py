
def forward_checking(problem, infos=True):
    if infos:
        print("   begin checking")
    var,val = problem.inst[-1]
    for y in problem.free_var:
        if infos:
            print("var", y, "domaine", problem.current_dom(y))
        if (var, y) in problem.const:
            dom = problem.current_dom(y).copy()
            for b in dom:
                if not problem.const[var, y](val, b):
                    problem.FC_domain_deletion[var].append((y, b))
                    problem.remove_val_from_dom(y, b)
            if len(problem.current_dom(y)) == 0:
                if infos:
                    print("EMPTY DOMAIN")
                return False
        if infos:
            print("end var", y, "domaine", problem.current_dom(y))
    if infos:
        print("   end checking")
    return True

