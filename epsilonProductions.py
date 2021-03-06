from CFGrammar import CFGrammar
from functools import reduce

def nullables(G):
    null = set()
    for lhs, rhss in G.productions.items():
        if () in rhss:
            null.add(lhs)

    oldNull = set()
    while null != oldNull:
        oldNull = null.copy()
        for lhs, rhss in G.productions.items():
            if any(set(rhs).issubset(null) for rhs in rhss):
                null.add(lhs)

    return null

def nullDerivables(null, alpha):
    if alpha == ():
        return {()} 

    nullDrv = nullDerivables(null, alpha[1:])
    if alpha[0] in null:
        return nullDrv | set(map(lambda t: (alpha[0],) + t, nullDrv))
    else:
        return set(map(lambda t: (alpha[0],) + t, nullDrv))

def removeEpsilonProductions(G):
    null = nullables(G)

    p = {}
    for lhs, rhss in G.productions.items():
        r = reduce(lambda a, rhs: a | nullDerivables(null, rhs), rhss, frozenset())
        p[lhs] = r - {()}

    name = CFGrammar.newSymbolName(G.start)
    n = frozenset([name]) | G.nonterminals
    p[name] = frozenset([(G.start,), ()]) if G.start in null else frozenset([(G.start,)])
    return CFGrammar(n, G.terminals, p, name)
