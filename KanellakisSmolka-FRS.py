#!/usr/bin/env python
# coding: utf-8

# In[7]:


from re import findall
from itertools import permutations 

class Transition:
    def __init__(self, src, tag, reg, tp, tgt):
        self.tag = tag
        self.source = src
        self.reg = reg
        tp = tp.upper()
        if tp not in ["K", "L", "G"]:
            raise ValueError("Invalid Transition Kind \"" + tp + "\".")
        self.kind = tp
        self.target = tgt

    def __str__(self):
        return "{}-{}{}{}->{}".format(self.source, self.tag, self.reg, self.kind, self.target)
    
    
class FRS:
    def __init__(self, regs, tags, states, avails, ts):
        self.regs = regs           # a natural number
        self.tags = set(tags)      # a set of tags
        self.mu = {}               # a map, built from two lists
        for i in range(len(states)):
            self.mu[states[i]] = avails[i] # this needs to be an increasing list
        self.states = set(states)  # a set of states
        self.hmax = 2*regs+1
        self.transitions = ts      # a list of Transitions
        self.delta = {}
        self._set_delta()
        self._memo = {}
        self._i_map = {}
        for q in states:
            x = self.mu[q]
            for i in range(len(x)):
                self._i_map[(q,x[i])] = i

    def _set_delta(self):
        for q in self.states:
            self.delta[q] = {}
            for t in self.tags:
                self.delta[q][t] = []
        for t in self.transitions:
            self.delta[t.source][t.tag].append((t.reg,t.kind,t.target))

    def __str__(self):
        states = "{"
        for q in self.states:
            states += "("+str(q)+","+str(self.mu[q])+")"
        states += "}"
        registers = self.regs
        tags = self.tags
        transitions = ["{}".format(t) for t in self.transitions]
        return ("({}, {}, {}, {})".format(registers, tags, states, transitions)).replace("\'", "").replace("\"", "")

    def fromString(self, representation):
        return "TODO"

    # a configuration is a triple (q,rho,h)
    # - q: state 
    # - rho: bounded assignment, i.e. a tuple from {1,...,hmax}
    # - h: number in 0,1,...,hmax
    #
    # returns a list of sets of configurations [C0,C1,...,Chmax]
    # where Ci contains all confs (q,rho,h) with h = i
    #
    def all_configurations(self,hmin=0):
        ret = []
        for h in range(hmin,self.hmax+1):
            s = set()
            for q in self.states:
                avail = self.mu[q]
                if max(avail) <= h:
                    for rho in permutations(range(1,h+1),len(avail)):
                        s.add((q,rho,h))
            ret.append(s)
        return ret

    def _guard(self,q,reg,kind,rho,h,name):
        if name == "G":
            return kind == "G" or kind == "L"
        if kind == "K":
            return name == rho[self._i_map[(q,reg)]]
        elif kind == "L":
            return name not in rho
        elif kind == "G":
            if h < self.hmax: return name > h
            else: return False
        else: assert(0)
        
    def _step(self,config,reg,kind,name,target):
        q, rho, h = config
        new_rho = []
        new_h = h
        if kind == "K":
            for r in self.mu[target]:
                if r in self.mu[q]:
                    new_rho.append(rho[self._i_map[(q,r)]])
        else:
            if h < self.hmax and name > h: new_h = h+1
            for r in self.mu[target]:
                if r == reg:
                    new_rho.append(name)
                elif r in self.mu[q]:
                    new_rho.append(rho[self._i_map[(q,r)]])
        return (target,tuple(new_rho),new_h)
    
    # return the set of next configurations,
    # given source configuration, tag and name
    #
    def get_next(self,config,tag,name):
        if (config,tag,name) in self._memo: return self._memo[(config,tag,name)]
        all_next = set()
        cls_next = []
        q, rho, h = config
        nexts = self.delta[q][tag]
        for (reg,kind,target) in nexts:
            if self._guard(q,reg,kind,rho,h,name):
                if name == "G":
                    xs = set()
                    for name2 in range(1,A.hmax+1): 
                        if name2 not in rho:
                            x = self._step(config,reg,kind,name2,target)
                            xs.add(x)
                            all_next.add(x)
                    cls_next.append(xs)
                else:
                    all_next.add(self._step(config,reg,kind,name,target))
        ret = (cls_next,all_next) if name == "G" else all_next
        self._memo[(config,tag,name)] = ret
        return ret
    

# useful to have two representations of partitions:
# .map: as a map from configurations to block numbers
# .blocks: as a list of sets of configurations
#
class Partition:
    def __init__(self,configs):
        self.size = 0
        self.blocks = []
        self.map = {}
        for cs in configs:
            if len(cs) > 0:
                self.size += 1
                block = len(self.blocks)
                for c in cs:
                    self.map[c] = block
                self.blocks.append(cs)
        
    def split(self,i,B1,B2):
        for s in B2:
            self.map[s] = self.size
        self.blocks[i] = B1
        self.blocks.append(B2)
        self.size += 1
        
    def get_h(self,b):
        for c in self.blocks[b]:
            return c[2]
        
    def __str__(self):
        s = ""
        for b in range(len(self.blocks)):
            s += str(b)+":\n"
            for c in self.blocks[b]:
                s += "    "+str(c)+"\n"
        return s

def getNextBlocks(config,tag,name,A,pi):
    nexts = A.get_next(config,tag,name)
    if name != "G":
        ret = set()
        for d in nexts:
            ret.add(pi.map[d])
        return ret
    else:
        rets, ret = [], set()
        for xs in nexts[0]:
            ys = set()
            for d in xs:
                ys.add(pi.map[d])
            rets.append(ys)
        for d in nexts[1]:
            ret.add(pi.map[d])
        return (rets,ret)

def split(b,t,a,pi,delta):
    B = pi.blocks[b]
    c = B.pop()
    B1 = {c}
    cNexts = getNextBlocks(c,t,a,A,pi)
    # print("Nexts for ",c," with ",a,": ",cNexts)
    B2 = set()
    for d in B:
        dNexts = getNextBlocks(d,t,a,A,pi)
        # print("-> Nexts for ",d," with ",a,": ",dNexts)
        if a != "G":
            to_new = cNexts != dNexts
        else:
            # cNexts = (set of sets of nexts, set of all nexts)
            to_new = False
            i = 0
            while i < len(cNexts[0]) and not to_new:
                if not cNexts[0][i].intersection(dNexts[1]):
                    to_new = True
                i += 1
            i = 0
            while i < len(dNexts[0]) and not to_new:
                if not dNexts[0][i].intersection(cNexts[1]):
                    to_new = True
                i += 1
        if to_new: 
            B2.add(d)
            # print("--> to new block")
        else: B1.add(d)
    if B2: 
        pi.split(b,B1,B2)
        return True
    pi.blocks[b] = B1
    return False
    
# partition refinement algorithm, takes an FRS as input and 
# returns a final partition
# GFresh is a flag, if true then GFresh transitions should b econsidered
# hmin is the smallest history to consider
#
def partitionRefine(A,GFresh,hmin=0): 
    pi = Partition(A.all_configurations(hmin))
    print(pi)
    changed = True
    while changed:
        changed = False
        b = 0
        while b < pi.size:
            h = pi.get_h(b)
            amax = h+1 if h < A.hmax else h
            for t in A.tags:
                for a in range(1,amax+1):
                    if split(b,t,a,pi,A.delta):
                        changed = True
                if h == A.hmax and GFresh and split(b,t,"G",pi,A.delta):
                    changed = True                    
            b += 1
    return pi
                

if __name__ == '__main__':
    # Q = [1,2]
    # mu = [[1,2],[1,2]]
    # t = ""
    # ts = [Transition(1,t,1,"K",1),Transition(1,t,2,"K",1),Transition(1,t,1,"G",1),Transition(2,t,1,"K",2),Transition(2,t,2,"K",2),Transition(2,t,2,"L",2)]
    # A = FRS(2,[t],Q,mu,ts)
    Q = [1,2]
    mu = [[1],[1,2]]
    t = ""
    ts = [Transition(1,t,1,"K",1),
          Transition(1,t,2,"G",2),
          Transition(2,t,2,"K",2),
          Transition(2,t,1,"G",1)
          ]
    A = FRS(2,[t],Q,mu,ts)
    print(A)

    print(partitionRefine(A,True))

