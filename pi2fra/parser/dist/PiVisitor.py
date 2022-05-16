# Generated from Pi.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .PiParser import PiParser
else:
    from PiParser import PiParser

# This class defines a complete generic visitor for a parse tree produced by PiParser.

class PiVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PiParser#root.
    def visitRoot(self, ctx:PiParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PiParser#line.
    def visitLine(self, ctx:PiParser.LineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PiParser#definition.
    def visitDefinition(self, ctx:PiParser.DefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PiParser#process.
    def visitProcess(self, ctx:PiParser.ProcessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PiParser#zero.
    def visitZero(self, ctx:PiParser.ZeroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PiParser#write.
    def visitWrite(self, ctx:PiParser.WriteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PiParser#read.
    def visitRead(self, ctx:PiParser.ReadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PiParser#nu.
    def visitNu(self, ctx:PiParser.NuContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PiParser#eq.
    def visitEq(self, ctx:PiParser.EqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PiParser#neq.
    def visitNeq(self, ctx:PiParser.NeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PiParser#defined.
    def visitDefined(self, ctx:PiParser.DefinedContext):
        return self.visitChildren(ctx)



del PiParser