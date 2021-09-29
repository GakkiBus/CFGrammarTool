class CFGrammar():
    __symbolID = 1

    def __init__(self, n, t, p, s):
        self._nonterminals = n
        self._terminals = t
        self._productions = p
        self._start = s

    @property
    def nonterminals(self):
        return self._nonterminals.copy()

    @property
    def terminals(self):
        return self._terminals.copy()

    @property
    def productions(self):
        return self._productions.copy()

    @property
    def start(self):
        return self._start

    def newSymbolName(name):
        name = "%s#%i" % (name, CFGrammar.__symbolID)
        CFGrammar.__symbolID += 1
        return name

    def nullables(self):
        nullables = set()
        for lhs, rhss in self.productions.items():
            if () in rhss:
                nullables.add(lhs)

        oldNullables = set()
        while (nullables != oldNullables):
            oldNullables = nullables
            for lhs, rhss in self.productions.items():
                if any(set(rhs).issubset(nullables) for rhs in rhss):
                    nullables.add(lhs)

        return nullables


def nullDerivables(nullables, alpha):
    if alpha == ():
        nullDrv = set()
        nullDrv.add(tuple())
        return nullDrv 

    nullDrv = nullDerivables(nullables, alpha[1:])
    if alpha[0] in nullables:
        return nullDrv.union(set(map(lambda t: (alpha[0],) + t, nullDrv)))
    else:
        return set(map(lambda t: (alpha[0],) + t, nullDrv))

def removeEpsilonProductions(G):
    nullables = G.nullables()

    p = {}
    for lhs, rhss in G.productions.items():
        r = set()
        for rhs in rhss:
            r = r.union(nullDerivables(nullables, rhs))
        r.remove(())
        p[lhs] = r

    name = CFGrammar.newSymbolName(G.start)
    n = G.nonterminals
    n.add(name)
    p[name] = {(G.start,), ()} if G.start in nullables else {(G.start,)}
    return CFGrammar(n, G.terminals, p, name)

# G = CFGrammar(
#         {"A", "B"}, 
#         {"a", "b"}, 
#         {
#             "A" : {("a",), ("B", "B")},
#             "B" : {("b", "A"), ()},
#         },
#         "A"
# )
# G_ = removeEpsilonProductions(G)
# print(G_.productions)

