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

    def newSymbolName(name):
        CFGrammar.__symbolID += 1
        return "%s#%i" % (name, CFGrammar.__symbolID)
