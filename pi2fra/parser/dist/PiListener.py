# Generated from Pi.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .PiParser import PiParser
else:
    from PiParser import PiParser

# This class defines a complete listener for a parse tree produced by PiParser.
class PiListener(ParseTreeListener):

    # Enter a parse tree produced by PiParser#root.
    def enterRoot(self, ctx:PiParser.RootContext):
        pass

    # Exit a parse tree produced by PiParser#root.
    def exitRoot(self, ctx:PiParser.RootContext):
        pass


    # Enter a parse tree produced by PiParser#line.
    def enterLine(self, ctx:PiParser.LineContext):
        pass

    # Exit a parse tree produced by PiParser#line.
    def exitLine(self, ctx:PiParser.LineContext):
        pass


    # Enter a parse tree produced by PiParser#definition.
    def enterDefinition(self, ctx:PiParser.DefinitionContext):
        pass

    # Exit a parse tree produced by PiParser#definition.
    def exitDefinition(self, ctx:PiParser.DefinitionContext):
        pass


    # Enter a parse tree produced by PiParser#process.
    def enterProcess(self, ctx:PiParser.ProcessContext):
        pass

    # Exit a parse tree produced by PiParser#process.
    def exitProcess(self, ctx:PiParser.ProcessContext):
        pass


    # Enter a parse tree produced by PiParser#zero.
    def enterZero(self, ctx:PiParser.ZeroContext):
        pass

    # Exit a parse tree produced by PiParser#zero.
    def exitZero(self, ctx:PiParser.ZeroContext):
        pass


    # Enter a parse tree produced by PiParser#write.
    def enterWrite(self, ctx:PiParser.WriteContext):
        pass

    # Exit a parse tree produced by PiParser#write.
    def exitWrite(self, ctx:PiParser.WriteContext):
        pass


    # Enter a parse tree produced by PiParser#read.
    def enterRead(self, ctx:PiParser.ReadContext):
        pass

    # Exit a parse tree produced by PiParser#read.
    def exitRead(self, ctx:PiParser.ReadContext):
        pass


    # Enter a parse tree produced by PiParser#nu.
    def enterNu(self, ctx:PiParser.NuContext):
        pass

    # Exit a parse tree produced by PiParser#nu.
    def exitNu(self, ctx:PiParser.NuContext):
        pass


    # Enter a parse tree produced by PiParser#eq.
    def enterEq(self, ctx:PiParser.EqContext):
        pass

    # Exit a parse tree produced by PiParser#eq.
    def exitEq(self, ctx:PiParser.EqContext):
        pass


    # Enter a parse tree produced by PiParser#neq.
    def enterNeq(self, ctx:PiParser.NeqContext):
        pass

    # Exit a parse tree produced by PiParser#neq.
    def exitNeq(self, ctx:PiParser.NeqContext):
        pass


    # Enter a parse tree produced by PiParser#defined.
    def enterDefined(self, ctx:PiParser.DefinedContext):
        pass

    # Exit a parse tree produced by PiParser#defined.
    def exitDefined(self, ctx:PiParser.DefinedContext):
        pass



del PiParser