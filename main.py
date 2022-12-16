# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np

instance_type = "n_reines"

def build_domaines(instance):
    if instance_type == "n_reines":
        n = instance
        domaines = dict()
        for i in range(n):
            domaines[i] = (np.arange(1,n+1), n)
    return domaines

def build_constraints(instance):
    if instance_type == "n_reines":
        tab = build_constraints_n_reines(instance)
    if instance_type == "colorabilite":
        tab = build_constraints_color(instance)
    return tab

def build_constraints_color(n, E):
    tab_constraints = dict()
    for i in range(n):
        for j in range(n):
            if E[i,j] ==1:
                tab_constraints[i, j] = lambda val1, val2: alldiff(i, j, val1, val2)
    return tab_constraints


def build_constraints_n_reines(n):
    tab_constraints = dict()
    for i in range(n):
        for j in range(i+1, n):
            tab_constraints[i,j] = lambda val1, val2 : constraint_diag_1(i,j, val1, val2)
            tab_constraints[i,j] = lambda val1, val2 : constraint_diag_2(i,j, val1, val2)
            tab_constraints[i,j] = lambda val1, val2 : alldiff(i,j, val1, val2)
    return tab_constraints

def constraint_diag_1(i,j,val_i,val_j):
    return val_i - val_j != np.abs(i-j)

def constraint_diag_2(i,j,val_i,val_j):
    return val_i - val_j != -np.abs(i-j)

def alldiff(i, j, val_i, val_j):
    return val_i != val_j

def backtrack(variables_instanciees, variables_non_instanciees,  domaines, contraintes):
    #domaines : dictionnaire de tuple (numpy array des valeurs possibles, indice de fin de domaine)
    #on donne une instanciation valide
    if len(variables_instanciees) >= 2:
        contrainte_violee = test_toutes_contraintes(variables_instanciees[:-1], variables_instanciees[-1][0], variables_instanciees[-1][1], contraintes)
        if contrainte_violee:
            print("pb contrainte")
            return False, None
    if len(variables_instanciees) == len(domaines):
        return True, variables_instanciees
    print(variables_instanciees, variables_non_instanciees)
    index_variable = choose_var_non_instanciee(variables_non_instanciees)
    valeurs_domaine_order = order_values(domaines[index_variable])

    for valeur in valeurs_domaine_order:
        print(index_variable, valeur)
        variables_instanciees_temp = variables_instanciees.copy()
        variables_non_instanciees_temp = variables_non_instanciees.copy()
        variables_instanciees_temp.append((index_variable, valeur))
        variables_non_instanciees_temp.remove(index_variable)
        backtrack_val = backtrack(variables_instanciees_temp,variables_non_instanciees_temp, domaines, contraintes)
        if backtrack_val[0]:
            print("backtrack")
            return backtrack_val
    return False, None

def choose_var_non_instanciee(variables_non_instanciees):
    return variables_non_instanciees[0]

def order_values(domaines):
    return domaines[0]

def test_toutes_contraintes(variables_instanciees, index_variable, valeur, contraintes):
    for (var_1, val_1) in variables_instanciees:
        for fonction in contraintes[var_1, index_variable]:
            if(not fonction(val_1, valeur)):
                return True
    return False

def AC3(domaines, contraintes):
    aTester = list(contraintes.keys()).copy()
    while len(aTester)!=0:
        x,y = aTester.pop()
        isSupportee = True
        for val_x in domaines[x][0]:
            value_isSupportee = checkSupport(x, val_x, y, domaines, contraintes[x,y])
            if not value_isSupportee:
                #domaine x <- domaine  de x - valeur val_x
                #########TO DO
                for elem in contraintes.keys():
                    if elem[0]==x and elem[1]!=y:
                        aTester.append((elem[1],x))

def checkSupport(x, val_x, y, domaines, function):
    value_isSupportee = False
    for val_y in domaines[y][0]:
        value_isSupportee = value_isSupportee or function(val_x, val_y)
    return value_isSupportee


def solveur():
    instance = 8
    domaines = build_domaines(instance)
    contraintes = build_constraints(instance)
    print(backtrack([], list(domaines.keys()), domaines, contraintes))




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    solveur()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
