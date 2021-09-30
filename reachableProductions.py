from CFGrammar import CFGrammar

def computeReachableProductions(G):
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

def removeUnreachableProductions(G):
    n = frozenset(computeReachableProductions(G))
    p = {lhs: rhss for (lhs, rhss) in G.productions.items() if lhs in n}
    return CFGrammar(n, G.terminals, p, G.start)

G = CFGrammar(
        frozenset(["A", "B", "C"]), 
        frozenset(["a", "b"]), 
        {
            "A" : frozenset([("a",), ("B",)]),
            "B" : frozenset([("b", "A"), ()]),
            "C" : frozenset([("A",)])
        },
        "A"
)

print(removeUnreachableProductions(G).productions)
