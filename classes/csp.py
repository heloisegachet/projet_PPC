import numpy as np

from classes.generic_constraints import diff, diag
import networkx as nx
import matplotlib.pyplot as plt

class csp:
    # classe représentant un problème

    def __init__(self):
        self.var = list() #liste des variables du CSP
        self.dom = dict() #dictionnaire (clé = variable, valeur = liste de valeurs possibles de la variable examinée)
        self.const = dict() #dictionnaire (clé = tuple(variable1, variable2), valeur = fonction)
        self.inst = list() #liste de tuples (nom de la variable instanciée, valeur)
        self.free_var = list() #liste des variables qui ne sont pas instanciées
        self.FC_domain_deletion = dict()
        self.AC_domain_deletion = dict()
        self.params = dict()

    def n_queens(self, n, params):
        self.params = dict()
        self.params = params.copy()
        self.var = [i for i in range(1, n + 1)]
        self.free_var = [i for i in range(1, n + 1)]
        for x in self.var:
            self.dom[x] = {"dom":np.arange(1, n + 1),"index":n}
        for x in self.var:
            self.FC_domain_deletion[x] = []
            self.AC_domain_deletion[x] = []
        def make_closure(x, y):
            return lambda i, j: (diff(x, y, i, j) and diag(x, y, i, j))
        for x in self.var:
            for y in self.var:
                if x != y:
                    self.const[x,y]=make_closure(x,y)


    def colorability(self, E, colors, params): # E = matrice d'adjacence
        self.params = dict()
        self.params = params.copy()
        n = E.shape[0]
        self.var = [i for i in range(n)]
        self.free_var = [i for i in range(n)]
        # peut être affiné par le degré max
        for x in self.var:
            self.dom[x] = {"dom":np.arange(colors),"index":colors}
        for x in self.var:
            self.FC_domain_deletion[x] = []
            self.AC_domain_deletion[x] = []
        def make_closure(x, y):
            return lambda i, j: (diff(x, y, i, j))
        for x in self.var:
            for y in self.var:
                if E[x, y] == 1:
                    self.const[x, y] = make_closure(x,y)

    def is_FC(self):
        return self.params["is_FC"]

    def is_MAC(self):
        return self.params["is_MAC"]

    def AC(self):
        return self.params["AC"]

    def remove_val_from_dom(self, x, a):
        #print(self.dom[x])
        i = np.where(self.dom[x]["dom"]==a)[0][0]
        index_domaine = self.dom[x]["index"]
        while i < index_domaine - 1:
            self.dom[x]["dom"][i], self.dom[x]["dom"][i + 1] = self.dom[x]["dom"][i + 1], self.dom[x]["dom"][i]
            i = i + 1
        self.dom[x]["index"] = index_domaine - 1
        #print(self.dom[x])

    def inst_var(self, x, v): #instanciation de la variable x à la valeur v
        self.free_var.remove(x)
        self.inst.append((x, v))

    def choose_var(self):
        method = self.params["choose_var"]
        if method == 'default':
            return min(self.free_var)
        if method == 'random':
            return np.random.choice(self.free_var)
        if method == "smallest_dom":
            elem = ([(len(self.current_dom(y)), y) for y in self.free_var])
            elem.sort()
            return elem[0][1]
        if method == "biggest_const":
            elem = [(len([x for x,z in self.const.keys() if z==y]), -y) for y in self.free_var]
            elem.sort(reverse=True)
            return -elem[0][1]
        if method == "biggest_const_non_inst":
            elem = [(len([x for x,z in self.const.keys() if x in self.free_var and z==y]), -y) for y in self.free_var]
            elem.sort(reverse=True)
            return -elem[0][1]

    def ordered(self, var, dom):
        method = self.params["choose_val"]
        if method == 'default':
            dom = np.sort(dom)
            return dom
        if method == "const_max":
            support = dict()
            for val in self.current_dom(var):
                support[val] = 0
                for (x, y), funct in self.const.items():
                    if x == var and y in self.free_var:
                        for b in self.current_dom(y):
                            if funct(val, b):
                                support[val] = support[val] + 1
            dom = sorted(dom, key=lambda x:support[x], reverse=True)
            return dom


    def current_dom(self,x):
        domaine, index = self.dom[x].values()
        for (y,b) in self.inst:
            if x==y:
                return [b]
        return domaine[:index]

    def test_inst(self): #vérifie que la dernière variable instanciée est compatible avec
                        # toutes les valeurs des variables précédentes
        if len(self.inst) < 2:
            return True
        last_var = self.inst[-1][0] #dernière variable instanciée
        last_val = self.inst[-1][1]
        for i in range(len(self.inst) - 1):
            x = self.inst[i][0]
            x_val = self.inst[i][1]
            if (x, last_var) in self.const:
                if (self.const[x,last_var](x_val, last_val) == False):
                    print("constraint FALSE")
                    return self.const[x,last_var](x_val, last_val)
        return True

    def test_inst_var(self, var, val, infos=False): #vérifie que la variable instanciée est compatible avec
                        # toutes les valeurs des variables précédentes
        if len(self.inst) < 1:
            return True
        for i in range(len(self.inst)):
            x = self.inst[i][0]
            x_val = self.inst[i][1]
            if (x, var) in self.const:
                if (self.const[x,var](x_val, val) == False):
                    if infos:
                        print("constraint FALSE")
                    return self.const[x,var](x_val, val)
        return True

    def cancel_AC(self, last_var):
        incr_index = dict()
        for (x, a) in self.AC_domain_deletion[last_var]:
            if not a in self.current_dom(x):
                incr_index[x] = incr_index.get(x, 0) + 1
        for x in incr_index.keys():
            self.dom[x]["index"] += incr_index[x]
        self.AC_domain_deletion[last_var] = []

    def cancel_FC(self, last_var):
        incr_index = dict()
        for (x, a) in self.FC_domain_deletion[last_var]:
            if not a in self.current_dom(x):
                incr_index[x] = incr_index.get(x, 0) + 1
        for x in incr_index.keys():
            self.dom[x]["index"] += incr_index[x]
        self.FC_domain_deletion[last_var] = []

    def cancel(self): #revenir en arrière sur la dernière instanciation
        # et ajout de la variable anciennement instanciée aux variables non instanciées
        last_var = self.inst.pop()[0]
        #self.dom[last_var]["index"] = len(self.dom[last_var]["dom"])
        self.cancel_AC(last_var)
        self.cancel_FC(last_var)
        self.free_var.append(last_var)

    def empty_dom(self):
        for x in self.var:
            if self.dom[x]["index"]==0:
                return True
        return False

    def checkSupport(self, x, val_x, y):
        value_isSupportee = False
        for val_y in self.current_dom(y):
            value_isSupportee = value_isSupportee or self.const[x,y](val_x, val_y)
        return value_isSupportee

    def n_queens_solution(self,n):
        sol= dict()
        for (x,v) in self.inst:
            sol[x] = v
        print(sol)
        for i in range(1,n+1):
            for j in range(1,n+1):
                if (i !=j and (sol[i]==sol[j] or sol[i]-sol[j]==np.abs(i-j) or sol[i]-sol[j]== -np.abs(i-j))):
                    print(i,j,sol[i], sol[j])
                    print('aie aie aie')
        for i in range(1,n+1):
            for j in range(sol[i]-1):
                print(" - ", end = "")
            print(" o ", end="")
            for j in range(sol[i],n):
                print(" - ", end = "")
            print()

    def colorability_solution(self,E):
        sol= dict()
        for (x,v) in self.inst:
        	sol[x] = v
        #     print("sommet",x,"couleur",v)
        n = E.shape[0]
        # for i in range(n):
        # 	for j in range(n):
        # 		if (E[i][j]==1) and sol[i]==sol[j]:
        # 			print('aie aie aie')
        G = nx.DiGraph()
        G.add_edges_from(
            [(i,j) for i in range(n) for j in range(n) if E[i,j]==1])
        values = [sol.get(node) for node in G.nodes()]
        # Need to create a layout when doing
        # separate calls to draw nodes and edges
        plt.figure(figsize=(15,15))
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos,
                               node_color=values)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, arrows=True)
        plt.show()
