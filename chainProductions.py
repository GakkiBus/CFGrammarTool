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
            chainProductions[n] = reduce(lambda a, c: a | chainProductions[c], cs, set())

    return chainProductions

def removeChainProductions(G):
    p = {}
    chainProductions = computeChainProductions(G)
    for n in G.nonterminals:
        rules = reduce(lambda a, b: a | G.productions[b], chainProductions[n], set())
        p[n] = frozenset([r for r in rules if not (len(r) == 1 and r[0] in G.nonterminals)])

    return CFGrammar(G.nonterminals, G.terminals, p, G.start)
