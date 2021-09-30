from CFGrammar import CFGrammar
from epsilonProductions import removeEpsilonProductions
from functools import reduce

def computeChainProductions(G):
    chainProductions = {} 
    for n in G.nonterminals:
        chainProductions[n] = {n}.union({rhs[0] for rhs in G.productions[n] 
                                        if len(rhs) == 1 and rhs[0] in G.nonterminals})

    oldChainProductions = {}
    while chainProductions != oldChainProductions:
        oldChainProductions = chainProductions
        for n, cs in chainProductions.items():
            chainProductions[n] = reduce(lambda a, c: a.union(chainProductions[c]), cs, set())

    return chainProductions

def removeChainProductions(G):
    p = {}
    chainProductions = computeChainProductions(G)
    for n in G.nonterminals:
        rules = reduce(lambda a, b: a.union(G.productions[b]), chainProductions[n], set())
        p[n] = frozenset([r for r in rules if not (len(r) == 1 and r[0] in G.nonterminals)])

    return CFGrammar(G.nonterminals, G.terminals, p, G.start)

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
print(G.productions)
G_ = removeChainProductions(removeEpsilonProductions(G))
print(G_.productions)
