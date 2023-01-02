def AC4(problem, infos=False):
    print("   AC4")
    Q, S, count = initAC4(problem, infos)
    while len(Q) != 0:
        y, b = Q.pop()
        if infos:
            print("test variable", y, "valeur", b)
        for (x, a) in S.get((y, b), []):
            count[x, y, a] = count.get((x, y, a), 0) - 1
            if infos:
                print("avec var", x, "val", a)
                print("count", count[x, y, a])
                print("dom x", problem.current_dom(x))
            if count[x, y, a] == 0 and a in problem.current_dom(x):
                if infos:
                    print("remove val", a, "from var", x)
                problem.remove_val_from_dom(x, a)
                problem.AC_domain_deletion.append((x,a))
                Q.append((x, a))
    print("   fin AC4")


def initAC4(problem, infos):
    print("      begin init AC4")
    Q = []
    S = dict()
    count = dict()
    for (x, y), funct in problem.const.items():
        i = 0
        while i < problem.dom[x]["index"]:
            a = problem.dom[x]["dom"][i]
            total = 0
            for b in problem.current_dom(y):
                if funct(a, b):
                    total += 1
                    S.setdefault((y, b), []).append((x, a))
            count[x, y, a] = total
            if count[x, y, a] == 0:
                if infos:
                    print("var", x, "val", a, "non supportee par var", y)
                problem.AC_domain_deletion.append((x, a))
                problem.remove_val_from_dom(x, a)
                Q.append((x, a))
            else:
                i+=1
    print("      end init AC4")
    return Q, S, count
