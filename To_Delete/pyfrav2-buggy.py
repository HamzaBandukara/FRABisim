# !/usr/bin/env python
# coding: utf-8
#
# In[5]:


MAXREG = 100   # maximum number of registers
MAXPROC= 1000  # maximum number of processes

# for lists or dictionaries
def strOfCollection(s):
    d = isinstance(s,dict)
    if d: dL,dR = "{","}"
    else: dL,dR = "[","]"        
    if len(s)==0: return dL+dR
    c = 0
    st = dL
    for x in s:
        if d:
            st+=str(x)+":"+str(s[x])
        else:
            st+=str(x)
        if c<len(s)-1:
            st+=","
            c+=1
    return st+dR

class Name:
    counter = 0
    
    def __init__(self, n=None):
        if n==None:
            self.n = Name.counter
            Name.counter+=1
        else:
            self.n = n
            if Name.counter <= n:
                Name.counter = n+1
                
    def __hash__(self):
        return self.n
    
    def __eq__(self,other):
        return self.n == other.n
    
    def __cmp__(self,other):
        return cmp(self.n,other.n)
            
    def __str__(self):
        return "n"+str(self.n)
    
    # hack?
    def __repr__(self):
        return str(self)


# TODO*: not really sorted anymore
class TransitionSet:
    def __init__(self):
        self._t = set()
        self.inpK = {}
        self.inpF = {}
        self.outK = {}
        self.outF = {}
        self.size = 0
        self.tys = ("inpK","inpF","outK","outF")

    def __iter__(self):
        for t in self._t:
            return ("t", t)
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

    def __next__(self):
        for t in self._t:
            return ("t", t)
        print("FIRST")
        for t in self.inpK:
            for t2 in self.inpK[t]:
                return (("inpK", *t), t2)
        print("2ND")
        for t in self.inpF:
            for t2 in self.inpF[t]:
                return (("inpF", *t), t2)
        print("3RD")
        for t in self.outK:
            for t2 in self.outK[t]:
                return (("outK", *t), t2)
        print("4TH")
        for t in self.outF:
            for t2 in self.outF[t]:
                return (("outF", *t), t2)
        print("ITERATION STOPPED")
        raise StopIteration

        
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
            
    def update(self,other):
        self._t.update(other._t)
        self.size = len(self._t)
        for ty in self.tys:
            x = getattr(self,ty)
            y = getattr(other,ty)
            for (i1,i2) in y:
                if (i1,i2) not in x: 
                    x[(i1,i2)] = y[(i1,i2)].copy()
                else: 
                    x[(i1,i2)].update(y[(i1,i2)])
            for s in x.values(): self.size += len(s)
        
    def copyFrom(self,other):
        self._t = other._t.copy()
        for ty in self.tys:
            x = getattr(self,ty)
            y = getattr(other,ty)
            for k in y: x[k]=y[k].copy()
        self.size=other.size
                
#     def sortAll(self):
#         for ty in self.tys:
#             self.sort(ty)
        
#     def sort(self,ty):
#         getattr(self,ty).sort()
        
    def strArray(self):
        s = [None for _ in range(self.size)]
        i=0
        for p in self._t:
            s[i] = "(_t, {})".format(p.nform)
            i+=1
        for ty in self.tys:
            for (i1,i2),ps in getattr(self,ty).items():
                for x in ps:
                    s[i] = "({0},{1:d},{2:d}), {3}".format(ty,i1,i2,x.nform)
                    i+=1
        return s
        
class RawProcess:
    support = {}
    vardefn = {}

    @staticmethod
    def addDefinition(symb,nlist,proc):
        RawProcess.vardefn[symb] = (nlist,proc)
    
    def __init__(self, ty, args=None):
        self.ty=ty
        self.uid=None
        if ty=="zero":
            self.uid = str(self)
            self.nid = ["0"]
            RawProcess.support[self] = frozenset()
        elif ty=="inp":
            n1,n2,pnext = args
            self.n1=n1
            self.n2=n2
            self.pnext=pnext
            self.uid = str(self)
            self.nid = [self.n1,"(",self.n2,")."]+pnext.nid
            RawProcess.support[self] = RawProcess.support[pnext].union({n1})
        elif ty=="out":
            n1,n2,pnext = args
            self.n1=n1
            self.n2=n2
            self.pnext=pnext
            self.uid = str(self)
            self.nid = [self.n1,"!",self.n2,"."]+pnext.nid
            RawProcess.support[self] = RawProcess.support[pnext].union({n1,n2})
        elif ty=="neq":
            n1,n2,pnext = args
            self.n1=n1
            self.n2=n2
            self.pnext=pnext
            self.uid = str(self)
            self.nid = ["[",self.n1,"#",self.n2,"]"]+pnext.nid
            RawProcess.support[self] = RawProcess.support[pnext].union({n1,n2})
        elif ty=="sum":
            pL,pR = args
            self.pL=pL
            self.pR=pR
            self.uid = str(self)
            self.nid = ["("]+pL.nid+["+"]+pR.nid+[")"]
            RawProcess.support[self] = RawProcess.support[pL].union(RawProcess.support[pR])
        elif ty=="par":
            pL,pR = args
            self.pL=pL
            self.pR=pR
            self.uid = str(self)
            self.nid = ["("]+pL.nid+["|"]+pR.nid+[")"]
            RawProcess.support[self] = RawProcess.support[pL].union(RawProcess.support[pR])
        elif ty=="nu":
            n1,pnext = args
            self.n1=n1
            self.pnext=pnext
            self.uid = str(self)
            self.nid = ["$",n1," "]+pnext.nid
            RawProcess.support[self] = RawProcess.support[pnext] - {n1}
        elif ty=="var":
            s,ns = args
            self.symb = s
            self.nlist = ns
            # if s not in RawProcess.vardefn:
            #     print("Need to define process var",s)
            self.uid = str(self)
            self.nid = ["," for _ in range(2*(len(ns)+1))]
            self.nid[0]=s
            self.nid[1]="["
            self.nid[-1]="]"
            for i in range(len(ns)):
                self.nid[2*(i+1)]=ns[i]
            RawProcess.support[self] = frozenset(ns)
        # print("\nNew RawProcess",hash(self),self.uid,self)

    def copy(self):
        return self
    
    # returns self[n_new/n], creates it if needed
    # n_new is assumed to be fresh
    def substitute(self,n_new,n):
        if n not in RawProcess.support[self]: return self
        if self.ty=="zero": 
            raise Exception("something wrong in substitute [{}/{}] in {}".format(str(n1),str(n2),str(self)))
        elif self.ty in ("inp","out","neq"):
            pNext = self.pnext.substitute(n_new,n)
            new_n1,new_n2 = self.n1,self.n2
            if new_n1==n: new_n1=n_new
            if self.ty!="inp" and new_n2==n: new_n2=n_new
            return RawProcess(self.ty,(new_n1,new_n2,pNext))
        elif self.ty== "sum":
            return RawProcess("sum",(self.pL.substitute(n1,n2),self.pR.substitute(n1,n2)))
        elif self.ty== "var":
            new_ns = self.nlist[:]
            for i in range(len(new_ns)):
                if new_ns[i]==n: new_ns[i]=n_new
                return RawProcess("var",(self.symb,new_ns))
            
    def __str__(self):
        if self.uid!=None: return self.uid
        if self.ty=="zero": 
            return "0"
        elif self.ty== "inp":
            return str(self.n1)+"("+str(self.n2)+")."+str(self.pnext)
        elif self.ty=="out":
            return str(self.n1)+"!"+str(self.n2)+"."+str(self.pnext)
        elif self.ty=="neq":
            return "["+str(self.n1)+"#"+str(self.n2)+"]"+str(self.pnext)
        elif self.ty== "sum":
            return "("+str(self.pL)+"+"+str(self.pR)+")"
        elif self.ty== "var":
            return self.symb+strOfCollection(self.nlist)
        elif self.ty=="nu":
            return f"${self.n1} {self.pnext}"
        elif self.ty=="par":
            return f"{self.pL}|{self.pR}"
        
    def __hash__(self):
        return hash(self.uid)
    
    def __eq__(self,other):
        return self.uid == other.uid
    
    def __cmp__(self,other):
        return cmp(self.uid,other.uid)

    
class Process:
    lts = {}
    
    @staticmethod
    def printLTS(f=(lambda x,y : True)):
        c=0
        for k,v in Process.lts.items():
            if f(k,v): 
                print(k.nform,"-> {")
                for s in v.strArray():
                    print("  "+s)
                print("}")
                c+=1
        return c
    
    # returns a pair of RawProcess's q1,q2 and a fresh name n so that q1 = p1[n/n1] 
    # and q2=p2[n/n2], where n1,n2 the names corresponding to i1,i2
    @staticmethod
    def refreshPair(p1,p2,i1,i2):
        n1 = n2 = None
        for k,v in p1.nmap.items():
            if v == i1:
                n1 = k
                break
        for k,v in p2.nmap.items():
            if v == i2:
                n2 = k
                break
        if (n1 is None) and (n2 is None):
            return p1.proc,p2.proc,Name()
        if n1 is None:
            return p1.proc,p2.proc,n2
        if n2 is None:
            return p1.proc,p2.proc,n1
        n = Name()
        p1 = p1.proc.substitute(n,n1)
        p2 = p2.proc.substitute(n,n2)
        return p1,p2,n
        
    # process p = (set of integers, map of free names to integers, raw process with names)
    def __init__(self, s, m, p):
        self.iset = s
        self.nmap = m
        self.proc = p
        self.uid = str(self)
        self.nform = self.normal()
        # print("new process",self.uid,hash(self),self)
            
    def __str__(self):
        return "("+strOfCollection(self.nmap)+"|-"+str(self.proc)+")"

    def nmapInv(self, i):
        c = None
        for k, v in self.nmap.items():
            if v == i:
                if c == None:
                    c = k
                else:
                    raise Exception(
                        "was asked to invert nmap of {} on {} but there are two names mapping to it".format(str(self),
                                                                                                            str(i)))
        return c

    # TODO: include congruence rules
    def normal(self):
        nproc = self.proc.nid[:]
        for i in range(len(nproc)):
            if isinstance(nproc[i],Name):
                if nproc[i] in self.nmap: nproc[i]=str(self.nmap[nproc[i]])        
                else: nproc[i] = str(nproc[i])
        return "".join(nproc)
    
    def __hash__(self):
        return hash(self.nform)
    
    def __eq__(self,other):
        return self.nform == other.nform
    
    def __cmp__(self,other):
        return cmp(self.nform,other.nform)

    def copy(self):
        return Process(self.iset.copy(),self.nmap.copy(),self.proc)

    # assumes that support of proc is uncluded in support of self
    def copyDown(self,proc):
        p = self.copy()
        p.proc = proc
        p.restrict()
        p.rehash()
        return p    
    
    def rehash(self):
        self.uid = str(self)
        self.nform = self.normal()
        # print("new process",self.uid,hash(self),self)        
        
    # turns p into p[i/n]. TODO: a better name is needed
    def substitute(self,i,n):
        if n in self.nmap: # TODO: apply renaming 
            raise Exception("name clash ("+str(n)+") in "+str(self))
        if n in RawProcess.support[self.proc]:
            self.nmap[n]=i
            self.iset.add(i)


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
        while i<MAXREG:
            if i not in self.iset: return i
            i += 1
        raise Exception("MAXREG exceeded")
        
    def step(self):
        # print("nexts for ",self,self.proc.ty)
        if self in Process.lts:
            return Process.lts[self]
        acc = TransitionSet()    # TODO*: create this on demand
        ty = self.proc.ty
        if ty=="zero":
            pass
        elif ty == "par":
            pL,pR = self.proc.pL, self.proc.pR
            pL2,pR2 = self.copy(),self.copy()  # (exceptionally) make a copy of self
            pL2.proc = pL; pR2.proc = pR       # with raw process pL/pR 
            pL2.rehash(); pR2.rehash()         # and the support of self
            accL,accR = pL2.step(),pR2.step()  # and get its step (a transition set)
            # Case Left/Right:
            left = True
            for _ in range(2):
                if left: new_acc = accL
                else: new_acc = accR
                for elem in new_acc:
                    pnext = elem[1].proc
                    if elem[0] == "_t" or elem[0][0]=="inpK" or elem[0][0]=="outK":
                        # TODO: instead of creating the RawProcess, check first if  
                        # it already exists in RawProcess.support
                        if left: p = self.copyDown(RawProcess("par",(pnext,pR)))
                        else: p = self.copyDown(RawProcess("par",(pL,pnext)))
                        acc.add((elem[0], p))
                    elif elem[0][0] == "inpF" or elem[0][0] == "outF":
                        p = self.copy()
                        if left:
                            p.proc = RawProcess("par", (pnext, pR))
                        else:
                            p.proc = RawProcess("par", (pL, pnext))
                        i1, i2 = elem[0][1], elem[0][2]
                        p.restrict()
                        j = p.minIempty()
                        # find the name behind i2
                        n2 = elem[1].nmapInv(i2)
                        p.substitute(j, n2)
                        p.rehash()
                        acc.add(((elem[0][0], i1, j), p))
                left=False
            # Case CommL/R: 
            inL,inR   = accL.inpK,accR.inpK
            outL,outR = accL.outK,accR.outK
            iL=iR=0
            xL,xR = list(inL.keys()),list(outR.keys())
            xL.sort(); xR.sort()
            while iL<len(xL) and iR<len(xR):
                if xL[iL]<xR[iR]: iL+=1
                elif xL[iL]>xR[iR]: iR+=1
                else:
                    for pLnext in inL[xL[iL]]:
                        for pRnext in outR[xR[iR]]:
                            p = self.copyDown(RawProcess("par",(pLnext.proc,pRnext.proc)))
                            acc.add(("_t",p))
                    iL+=1; iR+=1
            # TODO: and same for outL,inR
            # Case CloseL/R: TODO
            inL,inR   = accL.inpF,accR.inpF
            outL,outR = accL.outF,accR.outF
            iL=iR=0
            xL,xR = list(inL.keys()),list(outR.keys())
            xL.sort(); xR.sort()
            while iL<len(xL) and iR<len(xR):
                if xL[iL][0]<xR[iR][0]: iL+=1
                elif xL[iL][0]>xR[iR][0]: iR+=1
                else:
                    for pLnext in inL[xL[iL]]:
                        for pRnext in outR[xR[iR]]:
                            pLnext,pRnext,new_n = Process.refreshPair(pLnext,pRnext,xL[iL][1],xR[iR][1])
                            # TODO: need to add "nu" RawProcess (and Process)
                            p = self.copyDown(RawProcess("nu",(new_n,RawProcess("par",(pLnext,pRnext)))))
                            acc.add(("_t",p))
                    iL+=1; iR+=1
            # TODO: and same for outL,inR
        elif ty=="inp":
            n1,n2,pnext = self.proc.n1,self.proc.n2,self.proc.pnext
            n1free = n1 in RawProcess.support[pnext]
            n1i = self.nmap[n1]
            for i in self.iset:
                p = self.copy()
                p.proc = pnext
                p.substitute(i,n2)
                if not n1free:
                    p.nmap.pop(n1)
                    if not n1i in p.nmap.values():
                        p.iset.remove(n1i)
                p.rehash()
                acc.add((("inpK",n1i,i),p))
            p = self.copy()
            p.proc = pnext
            i = p.minIempty()
            p.substitute(i,n2)  # NOTE: could have use restrict here
            if not n1free:      # but we know what the possible changes  
                p.nmap.pop(n1)  # in support are
                if not n1i in p.nmap.values():
                    p.iset.remove(n1i)
            p.rehash()
            acc.add((("inpF",n1i,i),p))
        elif ty=="out":
            n1,n2,pnext = self.proc.n1,self.proc.n2,self.proc.pnext
            n1free = n1 in RawProcess.support[pnext]
            n1i = self.nmap[n1]
            n2free = n2 in RawProcess.support[pnext]
            n2i = self.nmap[n2]
            p = self.copy()
            p.proc = pnext
            if not n1free:
                p.nmap.pop(n1)
                if not n1i in p.nmap.values():
                    p.iset.remove(n1i)
            if not n1 == n2:
                if not n2free:
                    p.nmap.pop(n2)
                    if not n2i in p.nmap.values():
                        p.iset.remove(n2i)
            p.rehash()
            acc.add((("outK",n1i,n2i),p))
        elif ty=="neq":
            n1,n2,pnext = self.proc.n1,self.proc.n2,self.proc.pnext
            if self.nmap[n1]!=self.nmap[n2]:
                n1free = n1 in RawProcess.support[pnext]
                n1i = self.nmap[n1]
                n2free = n2 in RawProcess.support[pnext]
                n2i = self.nmap[n2]
                p = self.copy()
                p.proc = pnext
                if not n1free:
                    p.nmap.pop(n1)
                    if not n1i in p.nmap.values():
                        p.iset.remove(n1i)
                if not n2free:
                    p.nmap.pop(n2)
                    if not n2i in p.nmap.values():
                        p.iset.remove(n2i)
                p.rehash()
                acc.copyFrom(p.step())
        elif ty=="sum":
            for x in self.proc.pL,self.proc.pR:
                p = self.copy()
                p.proc = x 
                p.restrict()
                p.rehash()
                acc.update(p.step())
        elif ty=="nu":
            n1,pnext=self.proc.n1,self.proc.pnext
            p = self.copy()
            p.proc=pnext
            if n1 not in p.nmap:
                n1i = p.minIempty()
                p.nmap[n1] = n1i
                p.iset.add(n1i)
            p.rehash()
            new_acc = p.step()
            for t in new_acc:
                flg = True
                if t[0][0] == "outK":
                    if t[0][2] == p.nmap[n1]:
                        n1i = t[1].minIempty()
                        t[1].nmap[n1] = n1i
                        t[1].rehash()
                        acc.add((("outF", t[0][1], n1i), t[1]))
                else: flg = False
                if not flg:
                    if t[0][0] == "inpK":
                        if t[0][2] == p.nmap[n1]:
                            continue
                    new_p = t[1].copy()
                    new_p.proc = RawProcess("nu", (n1, new_p.proc))
                    if n1 in new_p.nmap:
                        n1i = new_p.nmap[n1]
                        new_p.nmap.pop(n1)
                        if not n1i in p.nmap.values():
                            new_p.iset.remove(n1i)
                    new_p.rehash()
                    acc.add((t[0],new_p))
        elif ty=="var":
            p = self.copy()
            nlist,proc = RawProcess.vardefn[self.proc.symb]
            p.proc = proc
            p.nmap = {}

            for i in range(len(nlist)):
                p.nmap[nlist[i]] = self.nmap[self.proc.nlist[i]]
            p.rehash()
            acc = p.step()   # TODO*: initial creation not needed
        Process.lts[self] = acc
        # print("nexts for ",self,"are",acc)
        return acc
    
    def buildLTS(self):
        safety = MAXPROC
        reachable = set()
        queue = set()
        queue.add(self)
        while safety>0 and len(queue)>0:
            # print("queue",queue)
            p = queue.pop()
            reachable.add(p)
            # print(safety,p)
            nexts = p.step()
            # print("nexts",nexts)
            for p in nexts._t:
                if p not in Process.lts: 
                    queue.add(p)
            for ty in nexts.tys:
                for s in getattr(nexts,ty).values():
                    for p in s:
                        if p not in Process.lts: 
                            queue.add(p)
            safety -= 1
        if safety==0: print("reached process limit",MAXPROC)
        else: print("processes examined:",MAXPROC-safety)
        return reachable
        
    
# a=Name();b=Name();c=Name()
# p = RawProcess("inp",(a,b,RawProcess("var",("P",[b]))))
# #print(p)
# p = RawProcess("sum",(RawProcess("sum",(RawProcess("zero"),p)),RawProcess("inp",(a,b,RawProcess("inp",(b,c,RawProcess("zero")))))))
# #print(p)
# RawProcess.addDefinition("P",[a],p)

# q = Process({0},{a:0},p)
# print("\nBuilding LTS for",q)
# q.buildLTS()
# for k in Process.lts:
#     print(k,":",Process.lts[k])

# size = 21
# P = [None for _ in range(size)]
# V = ["P"+str(i) for i in range(size)]
# n = [Name() for _ in range(size)]
# for i in range(size):
#     if i==0:
#         P[i]=RawProcess("inp",(n[0],n[1],RawProcess("var",(V[1],[n[0],n[1]]))))
#     elif i==size-1:
#         P[i]=RawProcess("out",(n[0],n[size-1],RawProcess("var",(V[size-2],n[:size-1]))))
#         for j in range(i):
#             P[i]=RawProcess("neq",(n[i],n[j],P[i]))
#     else:
#         push = RawProcess("inp",(n[0],n[i+1],RawProcess("var",(V[i+1],n[:i+2]))))
#         pop = RawProcess("out",(n[0],n[i],RawProcess("var",(V[i-1],n[:i]))))
#         for j in range(i):
#             pop=RawProcess("neq",(n[i],n[j],pop))
#             push=RawProcess("neq",(n[i],n[j],push))
#         P[i] = RawProcess("sum",(push,pop))
#     RawProcess.addDefinition(V[i],n[:i+1],P[i])
#
# print("Definitions")
# for k,(ns,df) in RawProcess.vardefn.items(): print(k,ns,"=",df)
#
# print("LTS")
# P = Process({0},{n[0]:0},RawProcess("var",(V[0],[n[0]])))
# print(P)
# r = P.buildLTS()
# # c = 0
# # for k in Process.lts:
# #     if k in r and len(Process.lts[k]) > 0:
# #         print(k.nform,":",Process.lts[k])
# #         c+=1
# # c
# Process.printLTS(lambda k,v : (k in r and v.size>0))
# x = TransitionSet()
# for k in Process.lts:
#     x.update(Process.lts[k])
#
# Hamza's Tests
# size = 1
# P = [None for _ in range(size)]
# V = ["P"+str(i) for i in range(size)]
# n = [Name() for _ in range(3)]
# for i in range(size):
#     # P[i]=RawProcess("nu", (n[0],
#     #                       RawProcess("inp", (n[1], "n3",
#     #                                          RawProcess("out", (n[2], n[0], RawProcess("zero")))))))
#     #
#     # RawProcess.addDefinition(V[i],n[1:],P[i])
#     P[i] = RawProcess("nu", ("n1",
#                              RawProcess("out", ("n0", "n1",
#                                         RawProcess("var", ("P0", ["n1"]))))))
#     RawProcess.addDefinition(V[i], ["n0"], P[i])
#
# print("Definitions")
# for k,(ns,df) in RawProcess.vardefn.items(): print(k,ns,"=",df)
#
# print("LTS")
# # P = Process({0},{"n1": 0, "n2": 1},RawProcess("var",(V[0],["n1", "n2"])))
# P = Process({0},{"n0": 0},RawProcess("var",(V[0],["n0"])))
# print(P)
# r = P.buildLTS()
# # c = 0
# # for k in Process.lts:
# #     if k in r and len(Process.lts[k]) > 0:
# #         print(k.nform,":",Process.lts[k])
# #         c+=1
# # c
# Process.printLTS(lambda k,v : (k in r and v.size>0))
# x = TransitionSet()
# for k in Process.lts:
#     x.update(Process.lts[k])


# ###TESTS 2 - Comm
# size = 1
# P = [None for _ in range(size)]
# V = ["P"+str(i) for i in range(size)]
# n = [Name() for _ in range(3)]
# for i in range(size):
#     P[i] = RawProcess("par", (
#         RawProcess("inp", (n[0], n[1], RawProcess("zero")))
#     ,
#         RawProcess("out", (n[0], n[2], RawProcess("zero"))))
#                       )
#     RawProcess.addDefinition(V[i], [n[0], n[2]], P[i])
#
# print("Definitions")
# for k,(ns,df) in RawProcess.vardefn.items(): print(k,ns,"=",df)
#
# print("LTS")
# P = Process({0, 1},{n[0]: 0, n[2]: 1},RawProcess("var",(V[0],[n[0], n[2]])))
# print(P)
# r = P.buildLTS()
# Process.printLTS(lambda k,v : (k in r and v.size>0))
# x = TransitionSet()
# for k in Process.lts:
#     x.update(Process.lts[k])

# ###TESTS 3 - Close
# size = 1
# P = [None for _ in range(size)]
# V = ["P"+str(i) for i in range(size)]
# n = [Name() for _ in range(4)]
# for i in range(size):
#     P[i] = RawProcess("par", (
#         # RawProcess("inp", (n[0], n[3], RawProcess("zero")))
#         RawProcess("inp", (n[0], n[3], RawProcess("out", (n[2], n[2], RawProcess("zero")))))
#     ,
#         # RawProcess("nu", (n[1], RawProcess("out", (n[0], n[1], RawProcess("zero")))))))
#         RawProcess("nu", (n[1], RawProcess("out", (n[0], n[1], RawProcess("out", (n[2], n[2], RawProcess("zero")))))))))
#
#     RawProcess.addDefinition(V[i], [n[0], n[2]], P[i])
#
# print("Definitions")
# for k,(ns,df) in RawProcess.vardefn.items(): print(k,ns,"=",df)
#
# print("LTS")
# P = Process({0, 1},{n[0]: 0, n[2]: 1},RawProcess("var",(V[0],[n[0], n[2]])))
# print(P)
# r = P.buildLTS()
# Process.printLTS(lambda k,v : (k in r and v.size>0))
# x = TransitionSet()
# for k in Process.lts:
#     x.update(Process.lts[k])


# ###TESTS 4 - P0 [n0, n2] = n0(n3).n3!n3.0|$n1 n0!n1.n2!n2.0
size = 1
P = [None for _ in range(size)]
V = ["P"+str(i) for i in range(size)]
n = [Name() for _ in range(4)]
for i in range(size):
    P[i] = RawProcess("par", (
        # RawProcess("inp", (n[0], n[3], RawProcess("zero")))
        RawProcess("inp", (n[0], n[3], RawProcess("out", (n[3], n[3], RawProcess("zero")))))
    ,
        # RawProcess("nu", (n[1], RawProcess("out", (n[0], n[1], RawProcess("zero")))))))
        RawProcess("nu", (n[1], RawProcess("out", (n[0], n[1], RawProcess("out", (n[2], n[2], RawProcess("zero")))))))))

    RawProcess.addDefinition(V[i], [n[0], n[2]], P[i])

print("Definitions")
for k,(ns,df) in RawProcess.vardefn.items(): print(k,ns,"=",df)

print("LTS")
P = Process({0, 1},{n[0]: 0, n[2]: 1},RawProcess("var",(V[0],[n[0], n[2]])))
print(P)
r = P.buildLTS()
Process.printLTS(lambda k,v : (k in r and v.size>0))
x = TransitionSet()
for k in Process.lts:
    x.update(Process.lts[k])