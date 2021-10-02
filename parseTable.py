from CFGrammar import CFGrammar
from functools import reduce

def computeFirstSetRelations(G):
    firstSets = {t : frozenset([t]) for t in G.terminals}
    relations = {}
    for n in G.nonterminals:
        relations[n] = frozenset([rhs for rhs in G.productions[n] 
                                         if len(rhs) > 0 and rhs[0] in G.nonterminals])
        firstSets[n] = frozenset(map(lambda a: a[:1], G.productions[n] - relations[n]))

    return firstSets, relations

def addToFirstSet(alpha, firstSets):
    if alpha == ():
        return frozenset("")
    elif "" in firstSets[alpha[0]]:
        return (firstSets[alpha[0]] - frozenset("")) | addToFirstSet(alpha[1:], firstSets)
    else:
        return firstSets[alpha[0]]
        
def computeFirstSets(G):
    firstSets, relations = computeFirstSetRelations(G) 
    oldFirstSets = {}
    while firstSets != oldFirstSets:
        oldFirstSets = firstSets.copy()
        for n, rs in relations.items():
            firstSets[n] |= reduce(lambda a, b: a | addToFirstSet(b, firstSets), rs, frozenset())

    return firstSets

