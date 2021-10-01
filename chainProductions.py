from CFGrammar import CFGrammar
from functools import reduce

def computeChainProductions(G):
    chainProductions = {} 
    for n in G.nonterminals:
        chainProductions[n] = {n} | {rhs[0] for rhs in G.productions[n]
                                        if len(rhs) == 1 and rhs[0] in G.nonterminals}

    oldChainProductions = {}
    while chainProductions != oldChainProductions:
        oldChainProductions = chainProductions.copy()
        for n, cs in chainProductions.items():
            chainProductions[n] = reduce(lambda a, c: a | chainProductions[c], cs, frozenset())

    return chainProductions

def removeChainProductions(G):
    p = {}
    chainProductions = computeChainProductions(G)
    for n in G.nonterminals:
        p[n] = reduce(lambda a, b: a | ({rhs for rhs in G.productions[b] 
                                             if not (len(rhs) == 1 and rhs[0] in G.nonterminals)})
                        , chainProductions[n]
                        , frozenset())

    return CFGrammar(G.nonterminals, G.terminals, p, G.start)
