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
