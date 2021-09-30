from functools import reduce

class CFGrammar():
    __symbolID = 0

    def __init__(self, n, t, p, s):
        self._nonterminals = n
        self._terminals = t
        self._productions = p
        self._start = s

    @property
    def nonterminals(self):
        return self._nonterminals

    @property
    def terminals(self):
        return self._terminals

    @property
    def productions(self):
        return self._productions

    @property
    def start(self):
        return self._start

    def getRules(self, n):
        return self._productions[n]

    def newSymbolName(name):
        CFGrammar.__symbolID += 1
        return "%s#%i" % (name, CFGrammar.__symbolID)

    # def nullables(self):
    #     nullables = set()
    #     for lhs, rhss in self.productions.items():
    #         if () in rhss:
    #             nullables.add(lhs)

    #     oldNullables = set()
    #     while nullables != oldNullables:
    #         oldNullables = nullables
    #         for lhs, rhss in self.productions.items():
    #             if any(set(rhs).issubset(nullables) for rhs in rhss):
    #                 nullables.add(lhs)

    #     return nullables

    # def chainProductions(self):
    #     chainProductions = {} 
    #     for n in self.nonterminals:
    #         chainProductions[n] = {n}.union({rhs[0] for rhs in self.productions[n] 
    #                                         if len(rhs) == 1 and rhs[0] in self.nonterminals})

    #     oldChainProductions = {}
    #     while chainProductions != oldChainProductions:
    #         oldChainProductions = chainProductions
    #         for n, cs in chainProductions.items():
    #             chainProductions[n] = reduce(lambda a, b: a.union(chainProductions[b]), cs, set())

    #     return chainProductions


# def nullDerivables(nullables, alpha):
    # if alpha == ():
    #     nullDrv = set()
    #     nullDrv.add(tuple())
    #     return nullDrv 

    # nullDrv = nullDerivables(nullables, alpha[1:])
    # if alpha[0] in nullables:
    #     return nullDrv.union(set(map(lambda t: (alpha[0],) + t, nullDrv)))
    # else:
    #     return set(map(lambda t: (alpha[0],) + t, nullDrv))

# def removeEpsilonProductions(G):
#     nullables = G.nullables()

#     p = {}
#     for lhs, rhss in G.productions.items():
#         r = set()
#         for rhs in rhss:
#             r = r.union(nullDerivables(nullables, rhs))
#         r.remove(())
#         p[lhs] = r

#     name = CFGrammar.newSymbolName(G.start)
#     n = G.nonterminals
#     n.add(name)
#     p[name] = {(G.start,), ()} if G.start in nullables else {(G.start,)}
#     return CFGrammar(n, G.terminals, p, name)

# def removeChainProductions(G):
#     p = {}
#     nonterminals = G.nonterminals
#     chainProductions = G.chainProductions()

#     for n in nonterminals:
#         rules = reduce(lambda a, b: a.union(G.getRules(b)), chainProductions[n], set())
#         p[n] = {r for r in rules if not (len(r) == 1 and r[0] in nonterminals)} 

#     return CFGrammar(nonterminals, G.terminals, p, G.start)


# G = CFGrammar(
#         {"A", "B", "C"}, 
#         {"a", "b"}, 
#         {
#             "A" : {("a",), ("B",)},
#             "B" : {("b", "A"), ()},
#             "C" : {("A",)}
#         },
#         "A"
# )
# G_ = removeEpsilonProductions(G)
# print(G.productions)
# print(removeChainProductions(G).productions)

