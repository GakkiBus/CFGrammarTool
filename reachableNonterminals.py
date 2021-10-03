from CFGrammar import CFGrammar

def computeReachableNonterminals(G):
    reachable = frozenset((G.start,))

    oldReachable = frozenset()
    while reachable != oldReachable:
        oldReachable = reachable
        reachable |= {a for n in reachable
                        for rhs in G.productions[n] 
                        for a in rhs
                        if a in G.nonterminals}
    return reachable

def removeUnreachableNonterminals(G):
    n = computeReachableNonterminals(G)
    p = {lhs: rhss for (lhs, rhss) in G.productions.items() if lhs in n}
    return CFGrammar(n, G.terminals, p, G.start)
