from CFGrammar import CFGrammar
from collections import deque
from functools import reduce

def computeDirectLeftRecursion(n, rhss):
    name = CFGrammar.newSymbolName(n + "_LR")
    nonLeftRecursive = frozenset({rhs + (name,) for rhs in rhss if rhs == () or rhs[0] != n})
    leftRecursive = frozenset({rhs[1:] + (name,) for rhs in rhss if len(rhs) > 1 and rhs[0] == n} | {()})
    return (name, nonLeftRecursive, leftRecursive)

# warning: possible nontermination when derivation A =>* A in G
def eliminateLeftRecursion(G):
    done = set()
    p = G.productions.copy()
    deq = deque(G.nonterminals)

    while len(deq) > 0:
        n = deq.popleft()
        print(n)
        if n in p.keys():
            R = p[n]
            oldR = frozenset()
            while R != oldR:
               oldR = R
               R = reduce(lambda a, rhs: a | ({pre + rhs[1:] for pre in p[rhs[0]]} 
                                                if len(rhs) > 0 and rhs[0] in done else {rhs})
                        , p[n]
                        , frozenset()
                        )

            name, nLR, LR = computeDirectLeftRecursion(n, R)
            if len(LR) == 1:
                p[n] = R
            else:
                p[n] = nLR
                p[name] = LR
                deq.appendleft(name)
        done.add(n)

    return CFGrammar(frozenset(done), G.terminals, p, G.start)
