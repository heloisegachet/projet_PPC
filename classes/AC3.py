
def AC3(problem, infos=False):
	print("   AC3")
	aTester = list(problem.const.keys()).copy() #liste des tuples de variables de chacune des contraintes
	while len(aTester)!=0:
		x,y = aTester.pop()
		if infos:
			print("test variables", x, "et", y)
		for i,val_x in enumerate(problem.current_dom(x)):
			value_isSupportee = problem.checkSupport(x, val_x, y)
			if infos:
				print("valeur", val_x)
				print("supportée" if value_isSupportee else "non supportée")
			if not value_isSupportee:
				print(problem.dom[x])
				index_domaine = problem.dom[x][1]
				while i < index_domaine:
					problem.dom[x][0][i],problem.dom[x][0][i+1] = problem.dom[x][0][i+1],problem.dom[x][0][i]
					i = i+1
				problem.dom[x][1] = index_domaine - 1
				print(problem.dom[x])
				for elem in problem.const.keys():
					if elem[0]==x and elem[1]!=y:
						aTester.append((elem[1],x))
	print("   fin AC3")
