
def AC3(problem, infos=False):
	print("   AC3")
	aTester = list(problem.const.keys()).copy() #liste des tuples de variables de chacune des contraintes
	while len(aTester)!=0:
		x,y = aTester.pop()
		if infos:
			print("test variables", x, "et", y)
		for i,a in enumerate(problem.current_dom(x)):
			value_isSupportee = problem.checkSupport(x, a, y)
			if infos:
				print("valeur", a)
				print("supportée" if value_isSupportee else "non supportée")
			if not value_isSupportee:
				problem.MAC_domain_deletion.append((x, a))
				problem.remove_val_from_dom(x, a)
				for elem in problem.const.keys():
					if elem[0]==x and elem[1]!=y:
						aTester.append((elem[1],x))
	print("   fin AC3")


