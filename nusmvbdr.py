class ExpressionBuilder:
    __expression = ""

    def __init__(self, arg1, arg2=None):
        if isinstance(arg1, str):
            self.__expression = arg1
        else:
            if arg2 is not None and arg1 <= arg2:
                self.__expression = str(arg1)+".."+str(arg2)
            else:
                self.__expression = str(arg1)

    def build(self):
        if len(self.__expression) == 0:
            raise Exception("Can't build empty expression")
        return self.__expression

    def withparen(self):
        return ExpressionBuilder("(" + self.build() + ")")

    def withnewline(self):
        return ExpressionBuilder(self.build() + "\n")

    def withnext(self):
        return ExpressionBuilder("next("+self.build()+")")

    def within(self, other):
        return ExpressionBuilder(self.build() + " in " + other.build())

    def withor(self, other):
        return ExpressionBuilder(self.build() + " | " + other.build())

    def withand(self, other):
        return ExpressionBuilder(self.build() + " & " + other.build())

    def witheq(self, other):
        return ExpressionBuilder(self.build() + " = " + other.build())

    def withlt(self, other):
        return ExpressionBuilder(self.build() + " < " + other.build())

    def withle(self, other):
        return ExpressionBuilder(self.build() + " <= " + other.build())

    def withgt(self, other):
        return ExpressionBuilder(self.build() + " > " + other.build())

    def withge(self, other):
        return ExpressionBuilder(self.build() + " >= " + other.build())

    def withadd(self, other):
        return ExpressionBuilder(self.build() + " + " + other.build())

    def withsub(self, other):
        return ExpressionBuilder(self.build() + " - " + other.build())

    def withmul(self, other):
        return ExpressionBuilder(self.build() + " * " + other.build())


class BaseDefinitionBuilder:
    def __init__(self, name, content=None):
        if not isinstance(name, str) or len(name) == 0:
            raise Exception("Definition name can't be empty")
        self.__name = name
        self.__content = content

    def name(self):
        return self.__name

    def content(self):
        return self.__content


class ExpressionDefinitionBuilder(BaseDefinitionBuilder):
    def withexp(self, expstr):
        if not isinstance(expstr, str) or len(expstr) == 0:
            raise Exception("Expression string can't be empty")
        return ExpressionDefinitionBuilder(self.name(), expstr)

    def build(self):
        if not isinstance(self.content(), str):
            raise Exception("Expression string must be set before building")
        return self.name() + " := " + self.content()+";"


class CaseDefinitionBuilder(BaseDefinitionBuilder):
    def withcase(self, expstr, resstr):
        if not isinstance(expstr, str) or len(expstr) == 0:
            raise Exception("Expression string can't be empty")

        if not isinstance(resstr, str) or len(resstr) == 0:
            raise Exception("Value string can't be empty")

        if self.content() is None:
            content = {}
        else:
            content = self.content().copy()

        content[expstr] = resstr
        return CaseDefinitionBuilder(self.name(), content)

    def withexpappended(self, lhsexp, op):
        if self.content() is None:
            content = {}
        else:
            content = self.content().copy()

        newcontent = {}
        for expstr in content.keys():
            newcontent[op(lhsexp, ExpressionBuilder(expstr)).build()] = content[expstr]

        return CaseDefinitionBuilder(self.name(), newcontent)

    def combined(self, other):
        if not isinstance(other, CaseDefinitionBuilder):
            raise Exception("Invalid definition to combine")

        if other.name() != self.name():
            raise Exception("Can't combine definition with different names")

        if other.content() is None:
            othercontent = {}
        else:
            othercontent = other.content().copy()

        if self.content() is None:
            content = {}
        else:
            content = self.content().copy()

        content.update(othercontent)
        return CaseDefinitionBuilder(self.name(), content)


    def build(self):
        if len(self.content()) == 0:
            raise Exception("At list 1 case must be added before building")

        defstr = "case\n"
        for expression, result in self.content().items():
            defstr += "  " + expression + " : " + result + ";\n"
        defstr += "esac;"
        return self.name() + " :=\n" + defstr
