from antlr4 import *
from pi2fra.parser.dist.PiLexer import PiLexer
from pi2fra.parser.dist.PiListener import PiListener
from pi2fra.parser.dist.PiParser import PiParser
from pi2fra.pyfra import *
import sys

class HelloPrintListener(PiListener):
    def enterProcess(self, ctx):
        return


def main(txt):
    lexer = PiLexer(InputStream(txt))
    stream = CommonTokenStream(lexer)
    parser = PiParser(stream)
    tree = parser.root()
    printer = HelloPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    return process_tree(tree)


def process_tree(tree):
    nms = {}
    flag = [True]
    num = tree.getChildCount()
    if not num % 2: num -= 1
    for i in range(num):
        child = tree.getChild(i)
        if child.getText() == "\n": continue
        process_line(child, nms, flag)
    return flag[0]


def process_line(child, nms, flag):
    num = child.getChildCount()
    for i in range(num):
        c = child.getChild(i)
        if c.getText() == "\n": continue
        if c.getRuleIndex() == 2:
            process_def(c, nms, flag)


def process_def(definition, nms, flag):
    num = definition.getChildCount()
    name = definition.getChild(0).getText()
    process = definition.getChild(num - 1)
    children = []
    for i in range(2, num-2, 2):
        c = definition.getChild(i).getText()
        if c not in nms:
            nms[c] = Name(c)
        children.append(nms[c])
    # print(f"DEFINITION: {name.getText()}({[c.getText() for c in children]})={process.getText()}")
    rp = examine_process(process, nms)
    RawProcess.addDefinition(name, children, rp)
    if isinstance(flag[0], bool):
        ints = [i for i in range(len(children))]
        nmap = {children[i]: i for i in range(len(children))}
        flag[0] = Process(set(ints), nmap, RawProcess("var", (name, children)))


def examine_process(process, nms=None):
    if nms is None:
        nms = dict()
    root = 0
    line = 1
    definition = 2
    proc = 3
    zero = 4
    write = 5
    read = 6
    nu = 7
    eq = 8
    neq = 9
    defined = 10

    if process.getChildCount() == 1:
        if process.getRuleIndex() == proc:
            child = process.getChild(0)
            if child.getRuleIndex() == nu:
                name = child.getChild(1).getText()
                if name not in nms:
                    nms[name] = Name(name)
                rp = RawProcess("nu", (nms[name], examine_process(child.getChild(3), nms)))
                return rp
            if child.getRuleIndex() == write:
                n1,n2=child.getChild(0).getText(),child.getChild(2).getText()
                if n1 not in nms:
                    nms[n1] = Name(n1)
                if n2 not in nms:
                    nms[n2] = Name(n2)
                rp = RawProcess("out", (nms[n1], nms[n2], examine_process(child.getChild(4), nms)))
                return rp
            if child.getRuleIndex() == read:
                n1,n2=child.getChild(0).getText(),child.getChild(2).getText()
                if n1 not in nms:
                    nms[n1] = Name(n1)
                if n2 not in nms:
                    nms[n2] = Name(n2)
                next_p = examine_process(child.getChild(4), nms)
                rp = RawProcess("inp", (nms[n1], nms[n2], next_p))
                return rp
            if child.getRuleIndex() == neq:
                n1,n2=child.getChild(1).getText(),child.getChild(3).getText()
                if n1 not in nms:
                    nms[n1] = Name(n1)
                if n2 not in nms:
                    nms[n2] = Name(n2)
                rp = RawProcess("neq", (nms[n1], nms[n2], examine_process(child.getChild(5), nms)))
                return rp
            if child.getRuleIndex() == eq:
                n1,n2=child.getChild(1).getText(),child.getChild(3).getText()
                if n1 not in nms:
                    nms[n1] = Name(n1)
                if n2 not in nms:
                    nms[n2] = Name(n2)
                rp = RawProcess("eq", (nms[n1], nms[n2], examine_process(child.getChild(5), nms)))
                return rp
            if child.getRuleIndex() == zero:
                rp = RawProcess("zero")
                return rp
            if child.getRuleIndex() == defined:
                names = []
                for i in range(2, child.getChildCount(), 2):
                    n = child.getChild(i).getText()
                    if n not in nms:
                        nms[n] = Name(n)
                    names.append(nms[n])
                rp = RawProcess("var", (child.getChild(0).getText(), names))
                return rp
    if process.getChildCount() == 3:
        if process.getChild(1).getText().replace(" ", "") == "|":
            c1, c2 = process.getChild(0), process.getChild(2)
            rp = RawProcess("par", (examine_process(c1, nms), examine_process(c2, nms)))
            return rp
        elif process.getChild(1).getText().replace(" ", "") == "+":
            c1, c2 = process.getChild(0), process.getChild(2)
            rp = RawProcess("sum", (examine_process(c1, nms), examine_process(c2, nms)))
            return rp
        elif process.getChild(0).getText() == "(":
            rp = examine_process(process.getChild(1), nms)
            return rp
        else:
            raise Exception("AT EOF")
            # return RawProcess("zero")


if __name__ == '__main__':
    txt = """P0(a,b)=(a<b>.0)+(b<a>.0)
    P1(a) = a<b>.0
    """
    main(txt)
