from .svutils import *

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

        # not effective at all from the perspective of security,
        # but should be effective in preventing mistakes
        self.decodeCalled = False
        self.callingDecode = False

        self.port = None

        # self.flattenedAssigns, self.directDependency is generated here
        self.decodeDependency()
        self.upperRegData = {}
        
    def extractAssign(self):
        if not self.callingDecode:
            raise Exception("extractAssign in ModuleContentDependency is called unexpectedly.")
        lst = []
        lst += self.assigndep
        for j in [i.extractAssign() for i in self.alwaysdep]:
            lst += j 

        return lst

    def decodeDependency(self):
        """Causes irreversible effect on data.
        """
        if not self.decodeCalled:
            self.decodeCalled = True
            self.callingDecode = True
            
            directDependency = {}
            trueReg = set()

            deplist = self.extractAssign()
            self.flattenedAssigns = deplist

            for item in deplist:
                lhs, rhs, assigntype = item.lhsId, item.rhsId, item.ttype
                
                for tag in lhs:
                    if assigntype == AssignType.NONBLOCK:
                        trueReg.add(tag)

                    if tag in directDependency:
                        directDependency[tag] += rhs 
                        directDependency[tag] = list(set(directDependency[tag]))
                    else:
                        directDependency[tag] = rhs

            for key in directDependency.keys():
                directDependency[key] = tuple(set(directDependency[key]))
            
            self.directDependency = directDependency
            self.trueReg = trueReg 

            self.callingDecode = False

        else:
            raise Exception("decodeDependency is not supposed to be called twice.")

    def addPortInfo(self, port):
        # port of Port (in svast.py)
        self.port = port
        self.inports = port.getInports()
        self.inportNames = set([i.name for i in self.inports])

        self.findUpperRegisterAll()

    def findUpperRegister(self, tag):
        if self.port is None:
            raise Exception("self.port is not given.")

        val = self.upperRegData.get(tag, None)
        # print(self.directDependency, tag)
        if val is None:
            lst = []
            try:
                for parent in self.directDependency[tag]:
                    if (parent in self.trueReg) or (parent in self.inportNames):
                        lst += [parent]
                    else:
                        lst += self.findUpperRegister(parent)

                    dummylist = [1]
                    if len(self.directDependency.get(parent, dummylist)) == 0:
                        # assigned Constant value
                        lst += [parent]
            except KeyError as e:
                key = str(e).replace("'", "")
                
                if key in self.inportNames:
                    print(f"{key} is an input port.") 
                else:
                    print(f"no dependency found on \"{key}\".")

            lst = list(set(lst))
            self.upperRegData[tag] = lst 
            return lst 
        else:
            # print("cached.")
            return val

    def findUpperRegisterAll(self):
        try:
            for tag in self.directDependency:
                self.findUpperRegister(tag)
        except RecursionError as e:
            raise Exception(str(e) + "\ninfinite loop in wires.")

    def findDirectDependency(self, wire:str):
        return self.directDependency.get(wire, None)