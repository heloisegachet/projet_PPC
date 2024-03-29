def AC4(problem, var):
	Q, S, count = initAC4(problem, var)
	while len(Q) != 0:
		y, b = Q.pop()
		for (x, a) in S.get((y, b), []):
			count[x, y, a] = count.get((x, y, a), 0) - 1
			if count[x, y, a] == 0 and a in problem.current_dom(x):
				problem.remove_val_from_dom(x, a)
				if var != None:
					problem.AC_domain_deletion[var].append((x,a))
				if len(problem.current_dom(x)) == 0:
					return False
				Q.append((x, a))
	for y in problem.var:
		if len(problem.current_dom(y)) == 0:
			return False
	return True

def initAC4(problem, var):
	Q = []
	S = dict()
	count = dict()
	for (x, y), funct in problem.const.items():
		if x in problem.free_var:
			dom = problem.current_dom(x).copy()
			for a in dom:
				total = 0
				for b in problem.current_dom(y):
					if funct(a, b):
						total += 1
						S.setdefault((y, b), []).append((x, a))
				count[x, y, a] = total
				if count[x, y, a] == 0:
					if var != None:
						problem.AC_domain_deletion[var].append((x, a))
					problem.remove_val_from_dom(x, a)
					Q.append((x, a))
	return Q, S, count
