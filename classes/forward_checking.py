
def forward_checking(problem):
	var,val = problem.inst[-1]
	for y in problem.free_var:
		if (var, y) in problem.const:
			dom = problem.current_dom(y).copy()
			for b in dom:
				if not problem.const[var, y](val, b):
					problem.FC_domain_deletion[var].append((y, b))
					problem.remove_val_from_dom(y, b)
			if len(problem.current_dom(y)) == 0:
				return False
	return True

