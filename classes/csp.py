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
        self.params = dict()

    def n_queens(self, n, is_FC):
        self.params["is_FC"] = is_FC
        self.var = [i for i in range(1, n + 1)]
        self.free_var = [i for i in range(1, n + 1)]
        for x in self.var:
            self.dom[x] = {"dom":np.arange(1, n + 1),"index":n}
        for x in self.var:
            self.FC_domain_deletion[x] = []
        def make_closure(x, y):
            return lambda i, j: (diff(x, y, i, j) and diag(x, y, i, j))
        for x in self.var:
            for y in self.var:
                if x != y:
                    self.const[x,y]=make_closure(x,y)


    def colorability(self, E, is_FC): # E = matrice d'adjacence
        self.params["is_FC"] = is_FC
        n = E.shape[0]
        self.var = [i for i in range(n)]
        self.free_var = [i for i in range(n)]
        # peut être affiné par le degré max
        for x in self.var:
            self.dom[x] = {"dom":np.arange(n),"index":n}
        for x in self.var:
            self.FC_domain_deletion[x] = []
        def make_closure(x, y):
            return lambda i, j: (diff(x, y, i, j))
        for x in self.var:
            for y in self.var:
                if E[x, y] == 1:
                    self.const[x, y] = make_closure(x,y)
    def is_FC(self):
        return self.params["is_FC"]


    def inst_var(self, x, v): #instanciation de la variable x à la valeur v
        print(x)
        print(self.free_var)
        self.free_var.remove(x)
        self.inst.append((x, v))

    def choose_var(self, method='smallest_dom'):
        if method == 'default':
            return self.free_var[0]
        if method == "smallest_dom":
            i = np.argmin([len(self.current_dom(y)) for y in self.free_var])
            return self.free_var[i]

    def current_dom(self,x):
        domaine, index = self.dom[x].values()
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
            print("variables ", last_var, x, " valeurs", last_val, x_val)
            if (x, last_var) in self.const:
                print("check constraint")
                if (self.const[x,last_var](x_val, last_val) == False):
                    print("FALSE")
                    return self.const[x,last_var](x_val, last_val)
        return True

    def test_inst_var(self, var, val, infos=True): #vérifie que la variable instanciée est compatible avec
                        # toutes les valeurs des variables précédentes
        if len(self.inst) < 1:
            return True
        for i in range(len(self.inst)):
            x = self.inst[i][0]
            x_val = self.inst[i][1]
            print("variables ", var, x, " valeurs", val, x_val)
            if (x, var) in self.const:
                print("check constraint")
                if (self.const[x,var](x_val, val) == False):
                    print("FALSE")
                    return self.const[x,var](x_val, val)
        return True

    def cancel(self): #revenir en arrière sur la dernière instanciation
        # et ajout de la variable anciennement instanciée aux variables non instanciées
        last_var = self.inst.pop()[0]
        self.dom[last_var]["index"] = len(self.dom[last_var]["dom"])#self.dom[last_var]["index"] + 1
        self.free_var.append(last_var)

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
