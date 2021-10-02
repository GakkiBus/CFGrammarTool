from CFGrammar import CFGrammar
from functools import reduce

def computeFirstSetRelations(G):
    firstSets = {t : frozenset([t]) for t in G.terminals}
    relations = {}
    for n in G.nonterminals:
        relations[n] = frozenset([rhs for rhs in G.productions[n] 
                                         if len(rhs) > 0 and rhs[0] in G.nonterminals])
        firstSets[n] = frozenset(map(lambda a: "" if a == () else a[0], G.productions[n] - relations[n]))

    return firstSets, relations

def firstSetWord(alpha, firstSets):
    if alpha == ():
        return frozenset(("",))
    elif "" in firstSets[alpha[0]]:
        return (firstSets[alpha[0]] - frozenset(("",))) | firstSetWord(alpha[1:], firstSets)
    else:
        return firstSets[alpha[0]]
        
def computeFirstSets(G):
    firstSets, relations = computeFirstSetRelations(G) 
    oldFirstSets = {}
    while firstSets != oldFirstSets:
        oldFirstSets = firstSets.copy()
        for n, rs in relations.items():
            firstSets[n] |= reduce(lambda a, b: a | firstSetWord(b, firstSets), rs, frozenset())

    return firstSets

def computeFollowSetRelations(G):
    followSets = {n : frozenset() for n in G.nonterminals}
    relations = {n : frozenset() for n in G.nonterminals}
    firstSets = computeFirstSets(G)

    for lhs, rhss in G.productions.items():
        for rhs in rhss:
            for i in range(len(rhs)):
                if rhs[i] in G.nonterminals:
                    f = firstSetWord(rhs[i+1:], firstSets)
                    followSets[rhs[i]] |= f - frozenset(("",))
                    if "" in f:
                        relations[rhs[i]] |= frozenset(lhs)

    followSets[G.start] |= frozenset("$")
    return followSets, relations

def computeFollowSets(G):
    followSets, relations = computeFollowSetRelations(G)
    oldFollowSets = {}
    while followSets != oldFollowSets:
        oldFollowSets = followSets.copy()
        for n, rs in relations.items():
            followSets[n] |= reduce(lambda a, b: a | followSets[b], rs, frozenset())

    return followSets

def computeParseTable(G):
    parseTable = {(A, a) : frozenset() for A in G.nonterminals for a in (G.terminals | frozenset("$"))}
    firstSets = computeFirstSets(G)
    followSets = computeFollowSets(G)

    for lhs, rhss in G.productions.items():
        for rhs in rhss:
            f = firstSetWord(rhs, firstSets)
            for a in (G.terminals & f):
                parseTable[lhs, a] |= frozenset(((lhs, rhs),))
            if "" in f:
                for a in followSets[lhs]:
                    parseTable[lhs, a] |= frozenset(((lhs, rhs),))

    return parseTable
