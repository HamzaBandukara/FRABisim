#!/usr/bin/env python
# coding: utf-8

# In[104]:


#!/usr/bin/env python
# coding: utf-8

# In[109]:
from DataStructures.RA_SF_A import RegisterAutomata, Transition

MAXREG = 100  # maximum number of registers
MAXPROC = 100000  # maximum number of processes


# for lists or dictionaries
def strOfCollection(s):
    d = isinstance(s, dict)
    if d:
        dL, dR = "{", "}"
    else:
        dL, dR = "[", "]"
    if len(s) == 0: return dL + dR
    c = 0
    st = dL
    for x in s:
        if d:
            st += str(x) + ":" + str(s[x])
        else:
            st += str(x)
        if c < len(s) - 1:
            st += ","
            c += 1
    return st + dR


class Name:
    counter = 0

    def __init__(self, s=None):
        self.n = Name.counter
        Name.counter += 1
        if s is not None:
            self.uid = s
        else:
            self.uid = f"n{self.n}"
        self.hash = hash(self.uid)

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        return self.uid == other.uid

    def __cmp__(self, other):
        return cmp(self.n, other.n)

    def __str__(self):
        return self.uid

    # hack?
    def __repr__(self):
        return str(self)


# TODO*: not really sorted anymore
class TransitionSet:
    @staticmethod
    def isTau(t):  # relies on "_t" type of tau transitions
        return len(t[0]) == 2

    def __init__(self):
        self._t = set()
        self.inpK = {}
        self.inpF = {}
        self.outK = {}
        self.outF = {}
        self.size = 0
        self.tys = ("inpK", "inpF", "outK", "outF")

    def __iter__(self):
        for t in self._t:
            yield ("t", t)
        for t in self.inpK:
            for t2 in self.inpK[t]:
                yield (("inpK", *t), t2)
        for t in self.inpF:
            for t2 in self.inpF[t]:
                yield (("inpF", *t), t2)
        for t in self.outK:
            for t2 in self.outK[t]:
                yield (("outK", *t), t2)
        for t in self.outF:
            for t2 in self.outF[t]:
                yield (("outF", *t), t2)
        return

    def add(self, t):
        if TransitionSet.isTau(t):
            if t[1] not in self._t:
                self._t.add(t[1])
                self.size += 1
                return
        (ty, i1, i2), pnext = t
        x = getattr(self, ty)
        if (i1, i2) not in x: x[(i1, i2)] = set()
        if pnext not in x[(i1, i2)]:
            x[(i1, i2)].add(pnext)
            self.size += 1

    def update(self, other):
        self._t.update(other._t)
        self.size = len(self._t)
        for ty in self.tys:
            x = getattr(self, ty)
            y = getattr(other, ty)
            for (i1, i2) in y:
                if (i1, i2) not in x:
                    x[(i1, i2)] = y[(i1, i2)].copy()
                else:
                    x[(i1, i2)].update(y[(i1, i2)])
            for s in x.values(): self.size += len(s)

    # TODO: is there need to copy here?
    def copyFrom(self, other):
        self._t = other._t.copy()
        for ty in self.tys:
            x = getattr(self, ty)
            y = getattr(other, ty)
            for k in y: x[k] = y[k].copy()
        self.size = other.size

    #     def sortAll(self):
    #         for ty in self.tys:
    #             self.sort(ty)

    #     def sort(self,ty):
    #         getattr(self,ty).sort()

    def strArray(self):
        s = [None for _ in range(self.size)]
        i = 0
        for p in self._t:
            s[i] = "(_t, {})".format(p.nform)
            i += 1
        for ty in self.tys:
            for (i1, i2), ps in getattr(self, ty).items():
                for x in ps:
                    s[i] = "({0},{1:d},{2:d}), {3}".format(ty, i1, i2, x.nform)
                    i += 1
        return s

    def strArray2(self):
        s = [None for _ in range(self.size)]
        i = 0
        for p in self._t:
            s[i] = ("(_t, {})".format(p.nform),p)
            i += 1
        for ty in self.tys:
            for (i1, i2), ps in getattr(self, ty).items():
                for x in ps:
                    s[i] = ("({0},{1:d},{2:d}), {3}".format(ty, i1, i2, x.nform),x)
                    i += 1
        return s
    

class RawProcess:
    support = {}
    vardefn = {}

    @staticmethod
    def addDefinition(symb, nlist, proc):
        RawProcess.vardefn[symb] = (nlist, proc)

    def __init__(self, ty, args=None):
        self.ty = ty
        self.uid = None
        if ty == "zero":
            self.uid = str(self)
            self.nid = (1, ("0"), ())
            RawProcess.support[self] = frozenset()
        elif ty == "inp":
            n1, n2, pnext = args
            self.n1 = n1
            self.n2 = n2
            self.pnext = pnext
            self.uid = str(self)
            nid0, nid1, nid2 = pnext.nid
            if nid0 == 1:
                self.nid = (2, ("(", f").{nid1[0]}") + nid1[1:], (self.n1, self.n2) + nid2)
            else:
                self.nid = (2, ("(", ").") + nid1, (self.n1, self.n2) + nid2)
            RawProcess.support[self] = RawProcess.support[pnext].union({n1}) - {n2}
        elif ty == "out":
            n1, n2, pnext = args
            self.n1 = n1
            self.n2 = n2
            self.pnext = pnext
            self.uid = str(self)
            nid0, nid1, nid2 = pnext.nid
            if nid0 == 1:
                self.nid = (2, ("<", f">.{nid1[0]}") + nid1[1:], (self.n1, self.n2) + nid2)
            else:
                self.nid = (2, ("<", ">.") + nid1, (self.n1, self.n2) + nid2)
            RawProcess.support[self] = RawProcess.support[pnext].union({n1, n2})
        elif ty == "neq":
            n1, n2, pnext = args
            self.n1 = n1
            self.n2 = n2
            self.pnext = pnext
            self.uid = str(self)
            nid0, nid1, nid2 = pnext.nid
            if nid0 == 1:
                self.nid = (1, ("[", "#", f"]{nid1[0]}") + nid1[1:], (self.n1, self.n2) + nid2)
            else:
                self.nid = (1, ("[", "#", "]") + nid1, (self.n1, self.n2) + nid2)
            RawProcess.support[self] = RawProcess.support[pnext].union({n1, n2})
        elif ty == "eq":
            n1, n2, pnext = args
            self.n1 = n1
            self.n2 = n2
            self.pnext = pnext
            self.uid = str(self)
            nid0, nid1, nid2 = pnext.nid
            if nid0 == 1:
                self.nid = (1, ("[", "=", f"]{nid1[0]}") + nid1[1:], (self.n1, self.n2) + nid2)
            else:
                self.nid = (1, ("[", "=", "]") + nid1, (self.n1, self.n2) + nid2)
            RawProcess.support[self] = RawProcess.support[pnext].union({n1, n2})
        elif ty == "sum":
            pL, pR = args
            self.pL = pL
            self.pR = pR
            self.uid = str(self)
            nidL0, nidL1, nidL2 = pL.nid
            nidR0, nidR1, nidR2 = pR.nid
            if nidL0 == nidR0 == 1:
                nid1 = (f"({nidL1[0]}",) + nidL1[1:-1] + (f"{nidL1[-1]}+{nidR1[0]}",) + nidR1[1:-1] + (f"{nidR1[-1]})",)
            elif nidL0 == 1:
                nid1 = (f"({nidL1[0]}",) + nidL1[1:-1] + (f"{nidL1[-1]}+",) + nidR1[:-1] + (f"{nidR1[-1]})",)
            elif nidL0 == nidR0 == 2:
                nid1 = ("(",) + nidL1[:-1] + (f"{nidL1[-1]}+",) + nidR1[:-1] + (f"{nidR1[-1]})",)
            else:  # 2,1
                nid1 = ("(",) + nidL1[:-1] + (f"{nidL1[-1]}+{nidR1[0]}",) + nidR1[1:-1] + (f"{nidR1[-1]})",)
            self.nid = (1, nid1, nidL2 + nidR2)
            RawProcess.support[self] = RawProcess.support[pL].union(RawProcess.support[pR])
        elif ty == "par":
            pL, pR = args
            self.pL = pL
            self.pR = pR
            self.uid = str(self)
            nidL0, nidL1, nidL2 = pL.nid
            nidR0, nidR1, nidR2 = pR.nid
            if nidL0 == nidR0 == 1:
                nid1 = (f"({nidL1[0]}",) + nidL1[1:-1] + (f"{nidL1[-1]}|{nidR1[0]}",) + nidR1[1:-1] + (f"{nidR1[-1]})",)
            elif nidL0 == 1:
                nid1 = (f"({nidL1[0]}",) + nidL1[1:-1] + (f"{nidL1[-1]}|",) + nidR1[:-1] + (f"{nidR1[-1]})",)
            elif nidL0 == nidR0 == 2:
                nid1 = ("(",) + nidL1[:-1] + (f"{nidL1[-1]}|",) + nidR1[:-1] + (f"{nidR1[-1]})",)
            else:  # 2,1
                nid1 = ("(",) + nidL1[:-1] + (f"{nidL1[-1]}|{nidR1[0]}",) + nidR1[1:-1] + (f"{nidR1[-1]})",)
            self.nid = (1, nid1, nidL2 + nidR2)
            RawProcess.support[self] = RawProcess.support[pL].union(RawProcess.support[pR])
        elif ty == "nu":
            n1, pnext = args
            self.n1 = n1
            self.pnext = pnext
            self.uid = str(self)
            nid0, nid1, nid2 = pnext.nid
            if nid0 == 1:
                self.nid = (1, ("$", f" {nid1[0]}") + nid1[1:], (self.n1,) + nid2)
            else:
                self.nid = (1, ("$", " ") + nid1, (self.n1,) + nid2)
            RawProcess.support[self] = RawProcess.support[pnext] - {n1}
        elif ty == "var":
            s, ns = args
            self.symb = s
            self.nlist = ns
            # if s not in RawProcess.vardefn:
            #     print("Need to define process var",s)
            self.uid = str(self)
            nid1 = (f"{s}[",) + tuple("," for _ in range(len(ns) - 1)) + ("]",)
            nid2 = tuple(x for x in ns)
            self.nid = (1, nid1, nid2)
            RawProcess.support[self] = frozenset(ns)
        # print("\nNew RawProcess",hash(self),self.uid,self)

    def copy(self):
        return self

    # returns self[new_n/n], creates it if needed
    # new_n is assumed to be fresh
    def substitute(self, new_n, n):
        if n not in RawProcess.support[self]: return self
        if self.ty == "zero":
            raise Exception("something wrong in substitute [{}/{}] in {}".format(str(new_n), str(n), str(self)))
        elif self.ty in ("inp", "out", "neq", "eq"):
            pNext = self.pnext.substitute(new_n, n)
            new_n1, new_n2 = self.n1, self.n2
            if new_n1 == n: new_n1 = new_n
            if self.ty != "inp" and new_n2 == n: new_n2 = new_n
            return RawProcess(self.ty, (new_n1, new_n2, pNext))
        elif self.ty in ("par", "sum"):
            return RawProcess(self.ty, (self.pL.substitute(new_n, n), self.pR.substitute(new_n, n)))
        elif self.ty == "nu":
            return RawProcess("nu", (self.n1, self.pnext.substitute(new_n, n)))
        elif self.ty == "var":
            new_ns = self.nlist[:]
            for i in range(len(new_ns)):
                if new_ns[i] == n: new_ns[i] = new_n
            return RawProcess("var", (self.symb, new_ns))
        else: raise Exception("missing case substitute",self)
            
    # returns self[ns1/ns2], creates it if needed
    # ns1 and ns2 are lists of same length, ns2 contains distinct elements
    # If ns1 contains any bound names of self, these are refreshed
    def substitutes(self, ns1, ns2):
        # print(self,ns1,ns2)
        if len(ns1)!=len(ns2):
            raise Exception("wrong call to substitutes!",self,ns1,ns2)
        supp = RawProcess.support[self]
        m0 = {ns2[i]:ns1[i] for i in range(len(ns1)) if ns2[i] in supp}
        m = {n:m0[n] if n in m0 else n for n in supp}
        if len(m) == 0: return self
        if self.ty == "zero":
            raise Exception("something wrong in substitutes [{}/{}] in {}".format(str(ns1), str(ns2), str(self)))
        elif self.ty in ("out", "neq", "eq"):
            pNext = self.pnext.substitutes(ns1, ns2)
            new_n1, new_n2 = m[self.n1], m[self.n2]
            return RawProcess(self.ty, (new_n1, new_n2, pNext))
        elif self.ty in ("par", "sum"):
            return RawProcess(self.ty, (self.pL.substitutes(ns1,ns2), self.pR.substitutes(ns1,ns2)))
        elif self.ty == "var":
            new_ns = [m[n] for n in self.nlist]
            return RawProcess("var", (self.symb, new_ns))        
        elif self.ty == "nu":
            if self.n1 in ns1:
                new_n = Name()
                return RawProcess("nu", (new_n, self.pnext.substitutes(ns1+[new_n], ns2+[self.n1])))
            return RawProcess("nu", (self.n1, self.pnext.substitutes(ns1, ns2)))
        elif self.ty == "inp":
            new_n1 = m[self.n1]
            if self.n2 in ns1:
                new_n2 = Name()
                return RawProcess("inp", (new_n1, new_n2, self.pnext.substitutes(ns1+[new_n2], ns2+[self.n2])))
            return RawProcess("inp", (new_n1, self.n2, self.pnext.substitutes(ns1, ns2)))
        else: raise Exception("missing case substitutes",self)

    def newFreeOf(self, other):
        s1 = RawProcess.support[self]
        s2 = RawProcess.support[other]
        c = None
        for k in s1:
            if k not in s2:
                if c is None:
                    c = k
                else:
                    raise Exception(
                        "was asked to find new free name of {} from {} but there more than one such".format(str(self),
                                                                                                            str(other)))
        return c

    def to_piet(self):
        if self.ty == "zero": return "0"
        if self.ty == "inp": return f"{self.n1}({self.n2}).{self.pnext.to_piet()}"
        if self.ty == "out": return f"{self.n1}<{self.n2}>.{self.pnext.to_piet()}"
        if self.ty == "neq": return f"[{self.n1}#{self.n2}]{self.pnext.to_piet()}"
        if self.ty == "eq": return f"[{self.n1}={self.n2}]{self.pnext.to_piet()}"
        if self.ty == "sum": return f"({self.pL.to_piet()}+{self.pR.to_piet()})"
        if self.ty == "par": return f"({self.pL.to_piet()}|{self.pR.to_piet()})"
        if self.ty == "nu": return f"^{self.n1} {self.pnext.to_piet()}"
        if self.ty == "var": return f"{self.symb}({('{},' * len(self.nlist)).format(*self.nlist)[:-1]})"

    def __str__(self):
        if self.uid != None: return self.uid
        if self.ty == "zero":
            return "0"
        elif self.ty == "inp":
            return f"{self.n1}({self.n2}).{self.pnext}"
        elif self.ty == "out":
            return f"{self.n1}<{self.n2}>.{self.pnext}"
        elif self.ty == "neq":
            return f"[{self.n1}#{self.n2}]{self.pnext}"
        elif self.ty == "eq":
            return f"[{self.n1}={self.n2}]{self.pnext}"
        elif self.ty == "sum":
            return f"({self.pL}+{self.pR})"
        elif self.ty == "var":
            s = ",".join([str(x) for x in self.nlist])
            return f"{self.symb}[{s}]"
        elif self.ty == "nu":
            return f"${self.n1} {self.pnext}"
        elif self.ty == "par":
            return f"({self.pL}|{self.pR})"
        else:
            return f"UNKNOWN TYPE {self.ty}"

    def __hash__(self):
        return hash(self.uid)

    def __eq__(self, other):
        return self.uid == other.uid

    def __cmp__(self, other):
        return cmp(self.uid, other.uid)


class Process:
    lts = {}

    @staticmethod
    def printLTS(f=(lambda x, y: True)):
        c = 0
        for (k,s), v in Process.lts.items():
            if s and f(k, v):
                print(k.nform, "-> {")
                for t in v.strArray():
                    print("  " + t)
                print("}")
                c += 1
        return c
    
    @staticmethod
    def printLTSBFS(root, f=(lambda x, y: True)):
        c = 0
        q = [root]
        vis = {root}
        while len(q) > 0:
            k = q.pop(0)
            v = Process.lts[(k,True)]
            if f(k, v):
                print(k.nform, "-> {")
                for t,p in v.strArray2():
                    print("  " + t)
                    if p not in vis:
                        q.append(p)
                        vis.add(p)
                print("}")
                c += 1
        return c

    # returns a pair of RawProcess's q1,q2 and a fresh name n so that q1 = p1[n/n1]
    # and q2=p2[n/n2], where n1,n2 the names corresponding to i1,i2
    @staticmethod
    def refreshPair(p1, p2, i1, i2):
        n1 = n2 = None
        for k, v in p1.nmap.items():
            if v == i1:
                n1 = k
                break
        for k, v in p2.nmap.items():
            if v == i2:
                n2 = k
                break
        if (n1 is None) and (n2 is None):
            return p1.proc, p2.proc, Name()
        if n1 is None:
            return p1.proc, p2.proc, n2
        if n2 is None:
            return p1.proc, p2.proc, n1
        n = Name()
        p1 = p1.proc.substitute(n, n1)
        p2 = p2.proc.substitute(n, n2)
        return p1, p2, n
    
    # process p = (set of integers, map of free names to integers, raw process with names)
    def __init__(self, s, m, p):
        self.iset = s
        self.nmap = m
        self.proc = p
        self.root = None
        # self.uid = str(self)
        self.nform = self.normal()
        self.hash = hash(self.nform)

    def __str__(self):
        return "(" + strOfCollection(self.nmap) + "|-" + str(self.proc) + ")"

    def nmapInv(self, i):
        c = None
        for k, v in self.nmap.items():
            if v == i:
                if c is None:
                    c = k
                else:
                    raise Exception(
                        "was asked to invert nmap of {} on {} but there are two names mapping to it".format(str(self),
                                                                                                            str(i)))
        return c

    # TODO: include congruence rules
    def normal(self):
        nid0, nid1, nid2 = self.proc.nid
        nproc = [None for _ in range(len(nid1) + len(nid2))]
        iset2 = self.iset.copy()
        i1 = i2 = 0
        for i in range(len(nproc)):
            if nid0 == 1:
                nproc[i] = nid1[i1]
                i1 += 1
            else:
                if nid2[i2] in self.nmap:
                    x = self.nmap[nid2[i2]]
                    iset2 -= {x}
                    nproc[i] = str(x)
                else:
                    nproc[i] = str(nid2[i2])
                i2 += 1
            nid0 = 3 - nid0
        if len(iset2) == 0:
            return "".join(nproc)
        iset2 = list(iset2)
        iset2.sort()
        return str(iset2) + "".join(nproc)

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        return self.nform == other.nform

    def __cmp__(self, other):
        return cmp(self.nform, other.nform)

    def copy(self, p=None):
        if p is None: p = self.proc
        return Process(self.iset.copy(), self.nmap.copy(), p)

    # assumes that support of proc is uncluded in support of self
    def copyDown(self, proc):
        p = self.copy()
        p.proc = proc
        p.restrict()
        p.rehash()
        return p

    def rehash(self):
        self.nform = self.normal()
        self.hash = hash(self.nform)

    # turns p into p[i/n]. TODO: a better name is needed
    def substitute(self, i, n):
        if n in self.nmap:  
            raise Exception("name clash (" + str(n) + ") in " + str(self))
        if n in RawProcess.support[self.proc]:
            self.nmap[n] = i
            self.iset.add(i)
            
    # replaces with n all names in p that have the same i as n 
    def fuse(self, n):
        ni = self.nmap[n]
        ms = [m for (m,i) in self.nmap.items() if i==ni and m!=n]
        if len(ms)==0: return 
        ns = [n for _ in ms]
        for m in ms: del self.nmap[m]
        self.proc = self.proc.substitutes(ns,ms)
        self.rehash()
        return
    
    # restrict nmap to free names, and iset accordingly
    def restrict(self):
        s = RawProcess.support[self.proc]
        iters = list(self.nmap.keys())
        for n in iters:
            if n not in s:
                self.nmap.pop(n)
        iters = list(self.iset)
        for i in iters:
            if i not in self.nmap.values():
                self.iset.remove(i)

    def minIempty(self):
        i = 0
        while i < MAXREG:
            if i not in self.iset: return i
            i += 1
        raise Exception("MAXREG exceeded")

    # for non-strict processes, find the least i that is either empty
    # or contains a name not in the proc support
    def minIfree(self):
        s = RawProcess.support[self.proc]
        m = {n:self.nmap[n] for n in s if n in self.nmap}
        i = 0
        while i < MAXREG:
            if i not in m.values(): return i
            i += 1
        raise Exception("MAXREG exceeded")

        
    # for s |- P | Q: consider s |- P (non strict) step
    # for each non-strict step to s' |- P', form s' |- P' | Q
    # -> if strict steps were considered then names of Q could be lost
    # e.g. (P1+P2) | Q, take a step in P1, can lose all names in P2 
    
    # If strict holds then self is strict, and the targets are strict
    # If strict does not hold then the target may be non-strict (there is no garbage collection)
    def step(self, strict=True):
        if (self, strict) in Process.lts:
            return Process.lts[(self, strict)]
        acc = TransitionSet()  
        if (self, False) in Process.lts: # so, strict holds
            acc2 = Process.lts[(self, False)]
            for elem in acc2:
                p = elem[1]
                acc.add((elem[0],p.copyDown(p.proc)))
            Process.lts[(self,strict)] = acc
            return acc
        # continue if not in memo and not strict
        ty = self.proc.ty
        if ty == "zero":
            pass
        elif ty == "par":
            pL, pR = self.proc.pL, self.proc.pR
            pL2, pR2 = self.copy(), self.copy()  # make a copy of self
            pL2.proc = pL
            pR2.proc = pR  # with raw process pL/pR
            pL2.rehash()
            pR2.rehash()  # and the support of self
            accL, accR = pL2.step(False), pR2.step(False)  # and get its non-strict step (a transition set)
            # Case Left/Right:
            left = True
            for _ in range(2):
                if left:
                    new_acc = accL
                else:
                    new_acc = accR
                for elem in new_acc:
                    pnext = elem[1].proc
                    if elem[0] == "_t" or elem[0][0] in ("outK","inK"): # case Par1
                        # TODO*: instead of creating the RawProcess, check first if
                        # it already exists in RawProcess.support
                        if left:
                            p = elem[1].copy(RawProcess("par", (pnext, pR)))
                        else:
                            p = elem[1].copy(RawProcess("par", (pL, pnext)))
                        acc.add((elem[0], p))
                    else: # case Par2
                        if left:
                            p = self.copy(RawProcess("par", (pnext, pR)))
                        else:
                            p = self.copy(RawProcess("par", (pL, pnext)))
                        i1, i2 = elem[0][1], elem[0][2]
                        # find the name behind i2
                        n2 = elem[1].nmapInv(i2)
                        ifr = p.minIfree()
                        if n2 is not None:
                            p.nmap[n2] = ifr
                            p.iset.discard(i2).add(ifr)
                        p.rehash()
                        acc.add(((elem[0][0], i1, i2), p))
                # Case CommL/R:
                if left:
                    theL = accL.inpK
                    theR = accR.outK
                else:
                    theR = accR.inpK
                    theL = accL.outK
                xL, xR = list(theL.keys()), list(theR.keys())
                iL = iR = 0
                xL.sort();
                xR.sort()
                while iL < len(xL) and iR < len(xR):
                    if xL[iL] < xR[iR]:
                        iL += 1
                    elif xL[iL] > xR[iR]:
                        iR += 1
                    else:
                        for pLnext in theL[xL[iL]]:
                            for pRnext in theR[xR[iR]]:
                                p = self.copy(RawProcess("par", (pLnext.proc, pRnext.proc)))
                                acc.add(("_t", p))
                        iL += 1;
                        iR += 1
                # Case CloseL/R:
                if left:
                    theL = accL.inpF
                    theR = accR.outF
                else:
                    theR = accR.inpF
                    theL = accL.outF
                xL, xR = list(theL.keys()), list(theR.keys())
                iL = iR = 0
                xL.sort();
                xR.sort()
                while iL < len(xL) and iR < len(xR):
                    if xL[iL][0] < xR[iR][0]:
                        iL += 1
                    elif xL[iL][0] > xR[iR][0]:
                        iR += 1
                    else:
                        for pLnext in theL[xL[iL]]:
                            for pRnext in theR[xR[iR]]:
                                pLnext, pRnext, new_n = Process.refreshPair(pLnext, pRnext, xL[iL][1], xR[iR][1])
                                p = self.copy(RawProcess("nu", (new_n, RawProcess("par", (pLnext, pRnext)))))
                                acc.add(("_t", p))
                        iL += 1;
                        iR += 1
                left = False
            # note we calculated the non-strict step
            Process.lts[(self,False)] = acc
            if strict: return self.step(strict)
            return acc
        elif ty == "inp":
            n1, n2, pnext = self.proc.n1, self.proc.n2, self.proc.pnext
            n1free = n1 in RawProcess.support[pnext]
            n1i = self.nmap[n1]
            for i in self.iset:
                p = self.copy()
                p.proc = pnext
                p.substitute(i, n2)
                if strict and not n1free:
                    p.nmap.pop(n1)
                    if n1i not in p.nmap.values():
                        p.iset.remove(n1i)
                p.rehash()
                acc.add((("inpK", n1i, i), p))
            p = self.copy()
            p.proc = pnext
            i = p.minIfree()
            p.substitute(i, n2)
            if strict and not n1free:
                p.nmap.pop(n1)
                if n1i not in p.nmap.values():
                    p.iset.remove(n1i)
            p.rehash()
            acc.add((("inpF", n1i, i), p))
        elif ty == "out":
            n1, n2, pnext = self.proc.n1, self.proc.n2, self.proc.pnext
            n1free = n1 in RawProcess.support[pnext]
            n1i = self.nmap[n1]
            n2free = n2 in RawProcess.support[pnext]
            n2i = self.nmap[n2]
            p = self.copy(pnext)
            if strict and not (n1free and n2free):
                if not n1free:
                    p.nmap.pop(n1)
                    if not n1i in p.nmap.values():
                        p.iset.remove(n1i)
                if n1 != n2 and not n2free:
                    p.nmap.pop(n2)
                    if not n2i in p.nmap.values():
                        p.iset.remove(n2i)
                p.rehash()
            acc.add((("outK", n1i, n2i), p))
        elif ty == "neq":
            n1, n2, pnext = self.proc.n1, self.proc.n2, self.proc.pnext
            if self.nmap[n1] != self.nmap[n2]:
                n1free = n1 in RawProcess.support[pnext]
                n1i = self.nmap[n1]
                n2free = n2 in RawProcess.support[pnext]
                n2i = self.nmap[n2]
                p = self.copy(pnext)
                if strict and not (n1free and n2free):
                    if not n1free:
                        p.nmap.pop(n1)
                        if not n1i in p.nmap.values():
                            p.iset.remove(n1i)
                    if n1 != n2 and not n2free:
                        p.nmap.pop(n2)
                        if not n2i in p.nmap.values():
                            p.iset.remove(n2i)
                    p.rehash()
                # TODO: why not simply return p.step(strict)?
                acc.copyFrom(p.step(strict))
        elif ty == "eq":
            n1, n2, pnext = self.proc.n1, self.proc.n2, self.proc.pnext
            if self.nmap[n1] == self.nmap[n2]:
                n1free = n1 in RawProcess.support[pnext]
                n1i = self.nmap[n1]
                n2free = n2 in RawProcess.support[pnext]
                n2i = self.nmap[n2]
                p = self.copy(pnext)
                if strict and not (n1free and n2free):
                    if not n1free:
                        p.nmap.pop(n1)
                        if not n1i in p.nmap.values():
                            p.iset.remove(n1i)
                    if n1 != n2 and not n2free:
                        p.nmap.pop(n2)
                        if not n2i in p.nmap.values():
                            p.iset.remove(n2i)
                    p.rehash()
                # TODO: why not simply return p.step(strict)?
                acc.copyFrom(p.step(strict))
        elif ty == "sum":
            for x in self.proc.pL, self.proc.pR:
                p = self.copy(x)
                new_acc = p.step(False)
                acc.update(new_acc)
            # note we calculated the non-strict step
            Process.lts[(self,False)] = acc
            if strict: return self.step(strict)
            return acc
        elif ty == "nu":
            n1, pnext = self.proc.n1, self.proc.pnext
            p = self.copy()
            p.proc = pnext
            if n1 not in RawProcess.support[pnext]:  # $n.P equivalent to P when n not in P
                p.rehash()
                return p.step(strict)
            if n1 not in p.nmap:
                n1i = p.minIempty()
                p.nmap[n1] = n1i
                p.iset.add(n1i)
            else:
                raise Exception("nu bound name already in nmap for", self)
            p.rehash()
            new_acc = p.step(strict)
            for t in new_acc:
                notTau = not TransitionSet.isTau(t)
                if notTau  and t[0][1] == n1i:
                    continue
                elif notTau and t[0][0] == "inpK" and t[0][2] == n1i:
                    continue
                    # raise Exception("fresh input register same as known register in", p, "->", t)
                elif notTau and t[0][0] == "outK" and t[0][2] == n1i:
                    # older, complicated, version, not sure if needed
                    # new_p = t[1].copy()
                    # ifr = new_p.minIfree()
                    # if n1 in new_p.nmap:
                    #    input("in")
                    #    new_p.nmap[n1] = n1i
                    #    new_p.iset.discard(n1i)
                    #    new_p.iset.add(ifr)
                    #    new_p.rehash()
                    acc.add((("outF", t[0][1], n1i), t[1]))
                else:
                    new_p = t[1].copy()
                    new_p.fuse(n1)
                    t0 = t[0]
                    if n1 in new_p.nmap:
                        n1i = new_p.nmap[n1]
                        new_p.nmap.pop(n1)
                        new_p.iset.discard(n1i)
                        # the fol. code ensures the least i is picked for inpF,outF
                        # as so far the least such was picked for n1
                        # could help with register economy, but not essential
                        if notTau and t[0][0] in ("inpF","outF") and n1i < t[0][2]:
                            t0 = (t[0][0], t[0][1], n1i)
                            if t[0][2] in new_p.iset:
                                new_p.iset.discard(t[0][2])
                                new_p.iset.add(n1i)
                                new_p.nmap[new_p.nmapInv(t[0][2])] = n1i
                        new_p.proc = RawProcess("nu", (n1, new_p.proc))
                        new_p.rehash()
                    acc.add((t0, new_p))
        elif ty == "var":
            p = self.copy()
            nlist, proc = RawProcess.vardefn[self.proc.symb]
            p.proc = proc
            p.nmap = {nlist[i]:self.nmap[self.proc.nlist[i]] for i in range(len(nlist))}
            p.rehash()
            acc = p.step()  # TODO*: initial creation not needed            
        Process.lts[(self,strict)] = acc
        return acc

    def buildLTS(self):
        safety = MAXPROC
        reachable = set()
        queue = {self}
        registers = set()
        while safety > 0 and len(queue) > 0:
            p = queue.pop()
            reachable.add(p)
            nexts = p.step()
            for p in nexts._t:
                if p not in reachable:
                    queue.add(p)
            for ty in nexts.tys:
                for pair in getattr(nexts, ty).keys():
                    registers.add(pair[0])
                    registers.add(pair[1])
                for s in getattr(nexts, ty).values():
                    for p in s:
                        if p not in reachable:
                            queue.add(p)
            safety -= 1
        if safety==0: print("WARNING: reached process limit",MAXPROC)
        # else: print("processes examined:",MAXPROC-safety)
        return reachable, registers


# ###TESTS 4 - P0 [n0, n2] = n0(n3).n3!n3.0|$n1 n0!n1.n2!n2.0
# size = 1
# P = [None for _ in range(size)]
# V = ["P"+str(i) for i in range(size)]
# n = [Name() for _ in range(4)]
# for i in range(size):
#     x = RawProcess("nu", (n[1], RawProcess("out", (n[0], n[1], RawProcess("out", (n[2], n[2], RawProcess("zero")))))))
#     y =         RawProcess("inp", (n[0], n[3], RawProcess("out", (n[3], n[3], RawProcess("zero")))))

#     P[i] = RawProcess("par", (x,y))
#         # RawProcess("inp", (n[0], n[3], RawProcess("zero")))
#         # RawProcess("nu", (n[1], RawProcess("out", (n[0], n[1], RawProcess("zero")))))))

#     RawProcess.addDefinition(V[i], [n[0], n[2]], P[i])

# Stacks
# size = 21
# P = [None for _ in range(size)]
# V = ["P" + str(i) for i in range(size)]
# n = [Name() for _ in range(size)]

# for i in range(size):
#     if i == 0:
#         P[i] = RawProcess("inp", (n[0], n[1], RawProcess("var", (V[1], [n[0], n[1]]))))
#     elif i == size - 1:
#         Ppop = RawProcess("out", (n[0], n[i], RawProcess("var", (V[i - 1], n[:i]))))
#         for j in range(i):
#             Ppop = RawProcess("neq", (n[i], n[j], Ppop))
#         P[i] = Ppop
#     else:
#         Ppop = RawProcess("out", (n[0], n[i], RawProcess("var", (V[i - 1], n[:i]))))
#         Ppush = RawProcess("inp", (n[0], n[i + 1], RawProcess("var", (V[i + 1], n[:i + 2]))))
#         for j in range(i):
#             Ppop = RawProcess("neq", (n[i], n[j], Ppop))
#             Ppush = RawProcess("neq", (n[i], n[j], Ppush))
#         P[i] = RawProcess("sum", (Ppush, Ppop))
#     RawProcess.addDefinition(V[i], n[:i + 1], P[i])

# print("Definitions")
# for k, (ns, df) in RawProcess.vardefn.items(): print(k, ns, "=", df)

# print("LTS")
# P = Process({0}, {n[0]: 0}, P[0])
# # print(P)
# print(P.nform)
# print(P.proc.nid)

# r, _, _ = P.buildLTS()
# Process.printLTS(lambda k, v: k in r and v.size > 0)
# x = TransitionSet()
# for k in Process.lts:
#     x.update(Process.lts[k])


# $n0. P[a, n0,n0]
# P[a,b,c] = a(d).c(d).0
# P[a,n0,n0] -> P[0,1,1] -00-> 1(0).0 = a:0,b:1,c:1,d:0 |- c(d).0
# $n0. P[0, n0,n0] -00-> $n0. c(0). 0
# $n0. 


# P(empty,x1,x2) = (push(y). P(empty, y, x1))
#                     + (pop(r). r'<x1>. P(empty, x2, empty))

# $empty. ( P(empty, empty, empty) )
                       
n = ["push", "pop", "empty", "x1", "x2", "y", "r"]
n = {n[i]: Name() for i in range(len(n))}

P1 = RawProcess("inp",(n["push"],n["y"],RawProcess("var",("P",[n["push"],n["pop"],n["empty"],n["y"],n["x1"]]))))
P2 = RawProcess("inp",(n["pop"],n["r"],RawProcess("out",(n["r"],n["x1"],RawProcess("var",("P",[n["push"],n["pop"],n["empty"],n["x2"],n["empty"]]))))))
P = RawProcess("sum",(P1,P2))

RawProcess.addDefinition("P",[n["push"],n["pop"],n["empty"],n["x1"],n["x2"]],P)
P = Process({0,1}, {n["push"]:0,n["pop"]:1}, RawProcess("nu",(n["empty"],RawProcess("var",("P",[n["push"],n["pop"],n["empty"],n["empty"],n["empty"]])))))

print("Definitions")
for k, (ns, df) in RawProcess.vardefn.items(): print(k, ns, "=", df)

print("LTS")
# P = Process({0}, {n[0]: 0}, P[0])
print(P)
print(P.nform)
# print(P.proc.nid)

c1 = 0
r, reg = P.buildLTS()
def foo(k,v):
    global c1
    if k in r: c1+=1
    return k in r and v.size>0
c2 = Process.printLTSBFS(P,foo)
# x = TransitionSet()
# for k in Process.lts:
#     x.update(Process.lts[k])
print("states:",c1,c2,"\nregisters:",reg)

