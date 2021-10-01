from CFGrammar import CFGrammar

def computeProductiveNonterminals(G):
    productive = set() 
    for n, rhss in G.productions.items():
        if any(set(rhs).issubset(G.terminals) for rhs in rhss):
            productive.add(n)

    oldProductive = set()
    while productive != oldProductive:
        oldProductive = productive.copy()
        for n, rhss in G.productions.items():
            if any(set(rhs).issubset(G.terminals | productive) for rhs in rhss):
                productive.add(n)

    return productive

def removeNonproductiveNonterminals(G):
    productive = computeProductiveNonterminals(G)
    p = {}
    for n in G.nonterminals:
        if n in productive:
            p[n] = frozenset([rhs for rhs in G.productions[n] 
                                  if all(a in (G.terminals | productive) for a in rhs)])

    return CFGrammar(productive, G.terminals, p, G.start)

