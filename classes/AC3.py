
def AC3(problem, var, infos=False):
	if infos:
		print("   AC3")
	aTester = list(problem.const.keys()).copy() #liste des tuples de variables de chacune des contraintes
	while len(aTester)!=0:
		x,y = aTester.pop()
		domain_init = problem.current_dom(x).copy()
		if x in problem.free_var:
			for a in domain_init:
				value_isSupportee = problem.checkSupport(x, a, y)
				if not value_isSupportee:
					problem.AC_domain_deletion[var].append((x, a))
					problem.remove_val_from_dom(x, a)
					if infos:
						print("remove ",x,"val",a)
					if len(problem.current_dom(x)) == 0:
						if infos:
							print("EMPTY DOMAIN")
						return False
					for elem in problem.const.keys():
						if elem[0]!=y and elem[0]==x:
							aTester.append((elem[1],x))
	if infos:
		print("   fin AC3")
	return True

