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

def debprint(*args):
    flag = False
    if flag:
        s = ""
        for a in args:
            s += str(a)
            s += " "
        print(s)

def issubmap(a,b):
    for x in a:
        try:
            if a[x] != b[x]: return False
        except: return False
    return True

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
            yield ("_t", t)
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

    def add(self,t):
        if len(t[0])==2:
            if t[1] not in self._t:
                self._t.add(t[1])
                self.size += 1
                return
        (ty,i1,i2),pnext = t
        x = getattr(self,ty) 
        if (i1,i2) not in x: x[(i1,i2)] = set()
        if pnext not in x[(i1,i2)]:
            x[(i1,i2)].add(pnext)
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
            #     debprint("Need to define process var",s)
            self.uid = str(self)
            nid1 = (f"{s}[",) + tuple("," for _ in range(len(ns) - 1)) + ("]",)
            nid2 = tuple(x for x in ns)
            self.nid = (1, nid1, nid2)
            RawProcess.support[self] = frozenset(ns)
        # debprint("\nNew RawProcess",hash(self),self.uid,self)

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
        # debprint(self,ns1,ns2)
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

#     # returns m(self), refreshing all bound names of self
#     # m is a map of names, whose domain contains the support of self
#     def refresh(self, m):
#     - if needed, can be implemented using code from substitutes            
            
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

    # DEPRECATED
    @staticmethod
    def checkLTS(f=(lambda x, y: True)):
        c = 0
        for (k,s), opts in Process.lts.items():
            for nmap, acc in opts:
                # strict ones should have just one option
                if s and f(k,s) and len(opts)>1:
                    for nmap, acc in opts:
                        print("with",strOfCollection(nmap),k,"-> {")
                        for t in acc.strArray():
                            print("  " + t)
                        print("}")
                    raise(Exception("more than one transition sets"+str(len(opts))))
    
    @staticmethod
    def printLTS(f=(lambda x, y: True)):
        c = 0
        for (k,s), opts in Process.lts.items():
            for nmap, acc in opts:
                if s and f(k, acc):
                    print(k.nform, "-> {")
                    for t in acc.strArray():
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
            debprint("look for",k,k.nform)
            opts = Process.lts[(k,True)]
            for nmap, acc in opts:
                if f(k, acc) and nmap==k.nmap:
                    print(k.nform, "-> {")
                    for t,p in acc.strArray2():
                        print("  " + t)
                        if p not in vis:
                            q.append(p)
                            vis.add(p)
                    print("}")
                    c += 1
                    break
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
        self.uid = None
        self.nform = self.normal()
        self.hash = hash(self.nform)

    def __str__(self):
        if self.uid is None:
            self.uid = "(" + strOfCollection(self.nmap) + "|-" + str(self.proc) + ")"
        return self.uid
            
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
            x = "".join(nproc)
            return x
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

    def copyUp(self, nmap, p=None):
        debprint("upping",self,nmap)
        p = self.copy(p)
        for n in nmap:
            p.nmap[n] = nmap[n]
        p.restrict()
        p.rehash()
        debprint("TO",p)
        return p
    
    def rehash(self):
        self.nform = self.normal()
        self.hash = hash(self.nform)
        self.uid = None

    # turns p into p[i/n]. TODO: a better name is needed
    def substitute(self, i, n):
        if n in self.nmap:  
            raise Exception("name clash (" + str(n) + ") in " + str(self))
        if n in RawProcess.support[self.proc]:
            self.nmap[n] = i
            self.iset.add(i)
            
    # replaces with n all names in p that have the same i as n 
    def fuse(self, n):
        debprint("fuse",self,n)
        ni = self.nmap[n]
        ms = [m for (m,i) in self.nmap.items() if i==ni and m!=n]
        if len(ms)==0: return 
        ns = [n for _ in ms]
        for m in ms: del self.nmap[m]
        self.proc = self.proc.substitutes(ns,ms)
        self.rehash()
        return

    # fuses all names in p that have value i, and returns the fusion 
    # returns None if there is no such name
    def ifuse(self, i):
        debprint("ifuse",self,i)
        ms = [m for (m,j) in self.nmap.items() if i==j]
        if len(ms)==0: return None
        n = ms.pop(-1)
        ns = [n for _ in ms]
        for m in ms: del self.nmap[m]
        self.proc = self.proc.substitutes(ns,ms)
        self.rehash()
        return n
    
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
    
    # All steps are strict, but nmap may contain more names than the support
    def step(self, strict=True):
        if not strict: raise(Exception("non strict step"),self)
        debprint("calling",self,strict)
        if (self, strict) in Process.lts: 
            opts = Process.lts[(self,strict)]
            for (nmap,acc) in opts:
                if nmap==self.nmap: return acc
        # continue if not in memo
        debprint("stepping",self,strict)
        acc = TransitionSet()
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
            accL, accR = pL2.step(), pR2.step()  # and get its step (a transition set)
            # Case Left/Right:
            left = True
            for _ in range(2):
                if left:
                    new_acc = accL
                else:
                    new_acc = accR
                for elem in new_acc:
                    pnext = elem[1].proc
                    if elem[0] == "_t" or elem[0][0] in ("outK","inpK"): # case Par1
                        # TODO*: instead of creating the RawProcess, check first if
                        # it already exists in RawProcess.support
                        if left:
                            p = elem[1].copyUp(self.nmap,RawProcess("par", (pnext, pR)))
                        else:
                            p = elem[1].copyUp(self.nmap,RawProcess("par", (pL, pnext)))
                        acc.add((elem[0], p))
                    else: # case Par2
                        if left:
                            p = elem[1].copyUp(self.nmap,RawProcess("par", (pnext, pR)))
                        else:
                            p = elem[1].copyUp(self.nmap,RawProcess("par", (pL, pnext)))
                        i1, i2 = elem[0][1], elem[0][2]
                        debprint(elem[0],elem[1])
                        # find the name behind i2
                        n2 = elem[1].nmapInv(i2)
                        ifr = self.minIempty()
                        debprint("new",n2,i2,ifr,self,self.nform)
                        if n2 is not None:
                            p.nmap[n2] = ifr
                            p.iset.discard(i2); p.iset.add(ifr) # FIXED
                        p.rehash()
                        acc.add(((elem[0][0], i1, i2), p))
                        debprint("Par2",pnext,pR,(elem[0][0],i1,i2),p)
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
                                if left:
                                    p = pLnext
                                else:
                                    p = pRnext
                                p = p.copyUp(self.nmap,RawProcess("par", (pLnext.proc, pRnext.proc)))
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
                                # TODO: could simply fuse the two fresh names
                                pLnext, pRnext, new_n = Process.refreshPair(pLnext, pRnext, xL[iL][1], xR[iR][1])
                                p = self.copyDown(RawProcess("nu", (new_n, RawProcess("par", (pLnext, pRnext)))))
                                acc.add(("_t", p))
                        iL += 1;
                        iR += 1
                left = False
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
            if strict: i = p.minIfree()
            else: i = p.minIempty()
            debprint("min chosen",i,p)
            p.substitute(i, n2)
            debprint("we get",p)
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
                acc = p.step()
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
                acc = p.step()
        elif ty == "sum":
            for x in self.proc.pL, self.proc.pR:
                p = self.copy(x)
                new_acc = p.step()
                for elem in new_acc:
                    acc.add((elem[0],elem[1].copyUp(self.nmap)))
        elif ty == "nu":
            n1, pnext = self.proc.n1, self.proc.pnext
            p = self.copy()
            p.proc = pnext
            if n1 not in RawProcess.support[pnext]:  # $n.P equivalent to P when n not in P
                p.rehash()
                acc = p.step()
            else:
                if n1 not in p.nmap:
                    n1i = p.minIempty()
                    p.nmap[n1] = n1i
                    p.iset.add(n1i)
                else:
                    raise Exception("nu bound name already in nmap for", self)
                p.rehash()
                new_acc = p.step()
                for t in new_acc:
                    notTau = not TransitionSet.isTau(t)
                    if notTau  and t[0][1] == n1i:
                        continue
                    elif notTau and t[0][0] == "inpK" and t[0][2] == n1i:
                        continue
                    elif notTau and t[0][0] == "outK" and t[0][2] == n1i:
                        # TODO select the min free index
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
                        new_n = new_p.ifuse(n1i)
                        t0 = t[0]
                        if new_n is not None:
                            new_ni = new_p.nmap[new_n]
                            new_p.nmap.pop(new_n)
                            new_p.iset.discard(new_ni)
                            # the fol. code ensures the least i is picked for inpF,outF
                            # as so far the least such was picked for n1
                            # could help with register economy, but not essential
                            if notTau and t[0][0] in ("inpF","outF") and new_ni < t[0][2]:
                                t0 = (t[0][0], t[0][1], new_ni)
                                if t[0][2] in new_p.iset:
                                    new_p.iset.discard(t[0][2])
                                    new_p.iset.add(new_ni)
                                    new_p.nmap[new_p.nmapInv(t[0][2])] = new_ni
                            new_p.proc = RawProcess("nu", (new_n, new_p.proc))
                            new_p.rehash()
                        acc.add((t0, new_p))
        elif ty == "var":
            p = self.copy()
            nlist, proc = RawProcess.vardefn[self.proc.symb]
            p.proc = proc
            debprint(self,nlist,self.nmap)
            for i in range(len(nlist)):
                p.nmap[nlist[i]]=self.nmap[self.proc.nlist[i]]
            p.rehash()
            acc = p.step()  # TODO*: initial creation not needed            
            debprint("for",self,False)
            for (x,y) in acc: debprint("===> adding",x,y,y.nform)
        try: Process.lts[(self,strict)].append((self.nmap,acc))
        except: Process.lts[(self,strict)] = [(self.nmap,acc)]
        debprint("for",self,strict)
        for e in acc: debprint("-> adding",e[0],e[1],e[1].nform)
        return acc

    def buildLTS(self):
        safety = MAXPROC
        root = self
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
        return reachable, registers, root

    @staticmethod
    def gen_FRA(f=(lambda x, y: True), ra=None, r=None):
        if ra is None:
            ra = RegisterAutomata()
            char = "s"
        else:
            char = "q"
        ra.initial = "s0"
        c = 0
        state_map = {}
        i_map = r.nmap
        state_map[r.nform] = char + "0"
        ra.s_map[state_map[r.nform]] = r.iset
        for k, v in Process.lts.items():
            # print(k[0], v)
            k = k[0]
            for x in v:
                v = x[1]
                if f(k, v):
                    if k.nform not in state_map:
                        state_map[k.nform] = char + str(len(state_map))
                        ra.s_map[state_map[k.nform]] = k.iset
                    src = state_map[k.nform]
                    for t in v:
                        if len(t[0]) == 1:  # Tau Transition
                            k = t[1]
                            if k.nform not in state_map:
                                state_map[k.nform] = char + str(len(state_map))
                                ra.s_map[state_map[k.nform]] = k.iset
                            tgt = state_map[k.nform]
                            tag = "TAU"
                            lbl = -1
                            t_type = "TAU"
                            ra.transitions.add(Transition(src, tag, lbl, t_type, tgt))
                        elif "inp" in t[0][0]:
                            k = t[1]
                            if k.nform not in state_map:
                                state_map[k.nform] = char + str(len(state_map))
                                ra.s_map[state_map[k.nform]] = k.iset
                            tgt = state_map[k.nform]
                            int_state = f"{src}inp{t[0][1]}"
                            if not int_state in ra.s_map:
                                ra.s_map[int_state] = ra.s_map[src]
                            ra.transitions.add(Transition(src, "inp1", t[0][1], "K", int_state))
                            t_type = "L"
                            if "K" in t[0][0]:
                                t_type = "K"
                            ra.transitions.add(Transition(int_state, "inp2", t[0][2], t_type, tgt))
                        elif "out" in t[0][0]:
                            k = t[1]
                            if k.nform not in state_map:
                                state_map[k.nform] = char + str(len(state_map))
                                ra.s_map[state_map[k.nform]] = k.iset
                            tgt = state_map[k.nform]
                            int_state = f"{src}out{t[0][1]}"
                            if not int_state in ra.s_map:
                                ra.s_map[int_state] = ra.s_map[src]
                            ra.transitions.add(Transition(src, "out1", t[0][1], "K", int_state))
                            t_type = "G"
                            if "K" in t[0][0]:
                                t_type = "K"
                            ra.transitions.add(Transition(int_state, "out2", t[0][2], t_type, tgt))
                # print("}")
                c += 1
        ra.complete_setup()
        return i_map, ra
if __name__ == '__main__':


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

    # Stacks^2, blows up
    # size = 2
    # P = [None for _ in range(size)]
    # V = ["P" + str(i) for i in range(size)]
    # n = [Name() for _ in range(size)]
    # Q = [None for _ in range(size)]
    # U = ["Q" + str(i) for i in range(size)]
    # m = [Name() for _ in range(size)]
    # m[0] = n[0]

    # for i in range(size):
    #     if i == 0:
    #         P[i] = RawProcess("inp", (n[0], n[1], RawProcess("var", (V[1], [n[0], n[1]]))))
    #         Q[i] = RawProcess("inp", (m[0], m[1], RawProcess("var", (U[1], [m[0], m[1]]))))
    #     elif i == size - 1:
    #         Ppop = RawProcess("out", (n[0], n[i], RawProcess("var", (V[i - 1], n[:i]))))
    #         Qpop = RawProcess("out", (m[0], m[i], RawProcess("var", (U[i - 1], m[:i]))))
    #         for j in range(i):
    #             Ppop = RawProcess("neq", (n[i], n[j], Ppop))
    #             Qpop = RawProcess("neq", (m[i], m[j], Qpop))
    #         P[i] = Ppop
    #         Q[i] = Qpop
    #     else:
    #         Ppop = RawProcess("out", (n[0], n[i], RawProcess("var", (V[i - 1], n[:i]))))
    #         Ppush = RawProcess("inp", (n[0], n[i + 1], RawProcess("var", (V[i + 1], n[:i + 2]))))
    #         Qpop = RawProcess("out", (m[0], m[i], RawProcess("var", (U[i - 1], m[:i]))))
    #         Qpush = RawProcess("inp", (m[0], m[i + 1], RawProcess("var", (U[i + 1], m[:i + 2]))))
    #         for j in range(i):
    #             Ppop = RawProcess("neq", (n[i], n[j], Ppop))
    #             Ppush = RawProcess("neq", (n[i], n[j], Ppush))
    #             Qpop = RawProcess("neq", (m[i], m[j], Qpop))
    #             Qpush = RawProcess("neq", (m[i], m[j], Qpush))
    #         P[i] = RawProcess("sum", (Ppush, Ppop))
    #         Q[i] = RawProcess("sum", (Qpush, Qpop))
    #     RawProcess.addDefinition(V[i], n[:i + 1], P[i])
    #     RawProcess.addDefinition(U[i], m[:i + 1], Q[i])

    # Stack
    size = 6
    P = [None for _ in range(size)]
    V = ["P" + str(i) for i in range(size)]
    n = [Name() for _ in range(size)]

    for i in range(size):
        if i == 0:
            P[i] = RawProcess("inp", (n[0], n[1], RawProcess("var", (V[1], [n[0], n[1]]))))
        elif i == size - 1:
            Ppop = RawProcess("out", (n[0], n[i], RawProcess("var", (V[i - 1], n[:i]))))
            for j in range(i):
                Ppop = RawProcess("neq", (n[i], n[j], Ppop))
            P[i] = Ppop
        else:
            Ppop = RawProcess("out", (n[0], n[i], RawProcess("var", (V[i - 1], n[:i]))))
            Ppush = RawProcess("inp", (n[0], n[i + 1], RawProcess("var", (V[i + 1], n[:i + 2]))))
            for j in range(i):
                Ppop = RawProcess("neq", (n[i], n[j], Ppop))
                Ppush = RawProcess("neq", (n[i], n[j], Ppush))
            P[i] = RawProcess("sum", (Ppush, Ppop))
        RawProcess.addDefinition(V[i], n[:i + 1], P[i])

    # push-only Stack
    # size = 2
    # P = [None for _ in range(size)]
    # V = ["P" + str(i) for i in range(size)]
    # n = [Name() for _ in range(size)]

    # for i in range(size):
    #     if i == 0:
    #         P[i] = RawProcess("inp", (n[0], n[1], RawProcess("var", (V[1], [n[0], n[1]]))))
    #     elif i == size - 1:
    #         P[i] = RawProcess("zero")
    #     else:
    #         Ppush = RawProcess("inp", (n[0], n[i + 1], RawProcess("var", (V[i + 1], n[:i + 2]))))
    #         for j in range(i):
    #             Ppush = RawProcess("neq", (n[i], n[j], Ppush))
    #         P[i] = Ppush
    #     RawProcess.addDefinition(V[i], n[:i + 1], P[i])


    # generator

    m = Name()
    G = RawProcess("nu",(m,(RawProcess("out",(n[0],m,RawProcess("var",("Gen",[n[0]])))))))
    RawProcess.addDefinition("Gen",[n[0]],G)

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

    # n = ["push", "pop", "empty", "x1", "x2", "y", "r"]
    # n = {n[i]: Name() for i in range(len(n))}

    # P1 = RawProcess("inp",(n["push"],n["y"],RawProcess("var",("P",[n["push"],n["pop"],n["empty"],n["y"],n["x1"]]))))
    # P2 = RawProcess("inp",(n["pop"],n["r"],RawProcess("out",(n["r"],n["x1"],RawProcess("var",("P",[n["push"],n["pop"],n["empty"],n["x2"],n["empty"]]))))))
    # P = RawProcess("sum",(P1,P2))

    # RawProcess.addDefinition("P",[n["push"],n["pop"],n["empty"],n["x1"],n["x2"]],P)
    # P = Process({0,1}, {n["push"]:0,n["pop"]:1}, RawProcess("nu",(n["empty"],RawProcess("var",("P",[n["push"],n["pop"],n["empty"],n["empty"],n["empty"]])))))

    print("Definitions")
    for k, (ns, df) in RawProcess.vardefn.items(): print(k, ns, "=", df)

    print("LTS")
    P0= RawProcess("var",(V[0],[n[0]]))
    G0= RawProcess("var",("Gen",[n[0]]))

    P = Process({0}, {n[0]: 0}, RawProcess("par",(P0,G0)))

    print(P)
    print(P.nform)
    # print(P.proc.nid)

    c1 = 0
    r, reg = P.buildLTS()
    # Process.checkLTS()
    def foo(k,v):
        global c1
        if k in r: c1+=1
        return k in r and v.size>0
    c2 = Process.printLTSBFS(P,foo)
    # x = TransitionSet()
    # for k in Process.lts:
    #     x.update(Process.lts[k])
    print("states:",c1,c2,"\nregisters:",reg)
