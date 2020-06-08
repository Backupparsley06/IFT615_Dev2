# -*- coding: utf-8 -*-

#####
# VotreNom (VotreMatricule) .~= À MODIFIER =~.
###

import math

#####
# reviser: Fonction utilisée par AC3 afin de réduire le domaine de Xi en fonction des contraintes de Xj.
#
# Xi: Variable (tuple (Y,X)) dont ses domaines seront réduit, si possible.
#
# Xj: Variable (tuple (Y,X)) dont ses domaines seront réduit, si possible.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku.
#      Pour plus d'information, voir doc de la fonction 'backtracking_search'.
#
# retour: Un tuple contenant un booléen indiquant si il y a eu des changements et le csp.
###



def reviser(Xi, Xj, csp):
    change = False
    for x in csp.domaines[Xi]:
        if len(csp.domaines[Xj]) == 1 and csp.domaines[Xj][0] == x:
            csp.domaines[Xi].remove(x)
            change = True

    return change, csp


#####
# AC3: Fonction s'occupant de réduire les domaines des variables selon l'algorithme AC3.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku.
#      Pour plus d'information, voir doc de la fonction 'backtracking_search'.
#
# retour: Un tuple contenant le csp optimisé et un booléen indiquant si aucune contrainte n'est violée.
###
def AC3(csp):
    file_arcs = csp.arcs()
    while len(file_arcs) > 0:
        Xi, Xj = file_arcs.pop(0)
        change, csp = reviser(Xi, Xj, csp)
        if change:
            if len(csp.domaines[Xi]) == 0:
                return None, False
            for Xk in csp.contraintes[Xi]:
                if Xk != Xj:
                    y = (Xk, Xi)
                    file_arcs.append(y)
    return csp, True


#####
# est_compatible: Fonction vérifiant la légalité d'une affectation.
#
# X: Tuple contenant la position en y et en x de la case concernée par l'affectation.
#
# v: String représentant la valeur (entre [1-9]) concernée par l'affectation.
#
# assignations: dict mappant les cases (tuple (Y,X)) vides à une valeur.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku.
#      Pour plus d'information, voir doc de la fonction 'backtracking_search'.
#
# retour: Un booléean indiquant si l'affectation de la valeur v à la case X est légale.
###
def est_compatible(X, v, assignations, csp):
    for k in csp.contraintes[X]:
        if k in assignations.keys() and assignations[k] == v:
            return False
    return True

def var_non_assigne(assignations, csp):
    for var in csp.variables:
        if var not in assignations.keys():
            return var
    return None

#####
# backtrack : Fonction s'occupant de trouver les assignations manquantes de la grille de Sudoku
#             en utilisant l'algorithme de Backtracking Search.
#
# assignations: dict mappant les cases (tuple (Y,X)) vides à une valeur.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku.
#      Pour plus d'information, voir doc de la fonction 'backtracking_search'.
#
# retour: Le dictionnaire des assignations (case => valeur)
###
def backtrack(assignations, csp):
    if len(assignations.keys()) == 81:
        return assignations
    X = var_non_assigne(assignations, csp)
    for v in csp.domaines[X]:
        if est_compatible(X, v, assignations, csp):
            assignations[X] = v
            cspEtoile = csp.copy()
            cspEtoile.domaines[X] = [v]
            cspEtoile, ok = AC3(cspEtoile)
            if ok:
                resultat = backtrack(assignations, cspEtoile)
                if resultat is not None:
                    return resultat
            assignations.pop(X)
    return None


#####
# backtracking_search : Fonction coquille pour la fonction 'backtrack'.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku. Les variables membres sont
#      'variables'   : list de cases (tuple (Y,X)) vides
#      'domaines'    : dict mappant une case à une liste des valeurs possibles
#      'contraintes' : dict mappant une case à une liste de cases dont leur valeur doivent être différentes
#
# retour: Le dictionnaire des assignations (case => valeur)
###
def backtracking_search(csp):
    return backtrack({}, csp)
