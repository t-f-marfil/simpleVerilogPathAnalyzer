from svutils import *

class AssignDependency:
    def __init__(self, ttype:AssignType, lhsId:list, rhsId:list, dependent=None) -> None:
        self.ttype = ttype
        self.lhsId = lhsId
        self.rhsId = rhsId
        self.dependent = dependent
        
    def __str__(self) -> str:
        txt = f"({joinNone(self.lhsId)}) {assigntypeTable[self.ttype]} ({joinNone(self.rhsId)})"
        if self.dependent is not None:
            txt += f" dependent to {joinNone(self.dependent)}"
        return txt

    def addDependent(self, depends:list):
        if self.dependent is None:
            self.dependent = []
        self.dependent += depends 
        return self

    def includeDependent(self):
        if self.dependent is None:
            self.dependent = []

        self.rhsId += self.dependent
        self.dependent = None
        return self


class IfelseblockDependency:
    def __init__(self, condwire:list, ifcontent, elsecontent=None) -> None:
        # if/elsecontent of AlwaysContentDependency
        self.condwire = condwire
        self.ifcontent = ifcontent
        self.elsecontent = elsecontent if elsecontent is not None else AlwaysContentDependency([], [])

    def __str__(self) -> str:
        txt = "If content with " + f"({', '.join(self.condwire) if len(self.condwire) > 0 else 'None'})"
        txt += "\n" + indent("If clause:\n" + indent(str(self.ifcontent)))
        txt += "\n" + indent("Else clause:\n" + indent(str(self.elsecontent)))
        return txt

    def addCondition(self, conds:list):
        self.condwire += conds 
        return self

    def flatten(self):
        blocksinIf = self.ifcontent.ifelse
        blocksinElse = self.elsecontent.ifelse

        flattend = list(map(lambda x: x.flatten(), blocksinIf + blocksinElse))

        allassigns = self.ifcontent.assign + self.elsecontent.assign
        for i in flattend:
            allassigns += i

        return [i.addDependent(self.condwire) for i in allassigns]


class AlwaysContentDependency:
    def __init__(self, assign:list, ifelse:list) -> None:
        # AssignDependency list, IfelseblockDependency list
        self.assign = assign
        self.ifelse = ifelse

    def __str__(self) -> str:
        txt = "Assign contents:\n" + indent(strStrgen(self.assign)) + "\nIfelse contents:\n" + indent(strStrgen(self.ifelse))
        return txt

    def ifFlatten(self):
        ans = []
        for i in self.ifelse:
            ans += i.flatten()

        return ans

    def extractAssign(self):
        lst = self.assign + self.ifFlatten()
        return [i.includeDependent() for i in lst]


class ModuleContentDependency:
    def __init__(self, assigndep:list, alwaysdep:list) -> None:
        self.assigndep = assigndep
        self.alwaysdep = alwaysdep
        
    def extractAssign(self):
        lst = self.assigndep
        for j in [i.extractAssign() for i in self.alwaysdep]:
            lst += j 

        return lst