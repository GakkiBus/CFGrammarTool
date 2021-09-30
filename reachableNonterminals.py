from CFGrammar import CFGrammar

def computeReachableNonterminals(G):
    reachable = {G.start}

    oldReachable = set()
    while reachable != oldReachable:
        oldReachable = reachable.copy()
        reachable |= {a for n in reachable
                        for rhss in G.productions[n] 
                        for rhs in rhss
                        for a in rhs
                        if a in G.nonterminals}
    return reachable

def removeUnreachableNonterminals(G):
    n = frozenset(computeReachableNonterminals(G))
    p = {lhs: rhss for (lhs, rhss) in G.productions.items() if lhs in n}
    return CFGrammar(n, G.terminals, p, G.start)
