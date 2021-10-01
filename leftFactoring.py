from CFGrammar import CFGrammar

def longestPrefix(w1, w2):
    for i in range(min(len(w1), len(w2))):
        if w1[i] != w2[i]:
            return w1[:i]

    return w1 if len(w1) < len(w2) else w2 

def longestPrefixGroup(words):
    group = set()
    maxPrefix = () 
    for i in range(len(words)):
        for j in range(i+1, len(words)):
            prefix = longestPrefix(words[i], words[j])
            if len(prefix) > len(maxPrefix):
                maxPrefix = prefix
                group = {words[i], words[j]}
            elif words[j][:len(maxPrefix)] == maxPrefix:
                group.add(words[j])

    return group, maxPrefix 

def leftFactoring(G):
    addedNonterminals = set()
    p = {}

    for lhs, rhss in G.productions.items():
        group, prefix = longestPrefixGroup(list(rhss))
        while len(prefix) > 0:
            name = CFGrammar.newSymbolName(lhs + "_LF")
            addedNonterminals.add(name)
            rhss = (rhss - group) | {prefix + (name,)}
            p[name] = frozenset([rhs[len(prefix):] for rhs in group])

            group, prefix = longestPrefixGroup(list(rhss))
        p[lhs] = rhss

    return CFGrammar(G.nonterminals | addedNonterminals, G.terminals, p, G.start)
