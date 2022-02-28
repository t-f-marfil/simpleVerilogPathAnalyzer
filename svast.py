from enum import Enum, auto
import re

from svutils import *
from svnetdata import *


class ModuleDuplicateErr(Exception):
    pass 


class Source:
    def __init__(self):
        self.modules = {}

    def __str__(self):
        txt = f"{len(self.modules)} toplevel{'' if len(self.modules) <= 1 else 's'}:"
        
        for i in reversed(self.modules.values()):
            txt += "\n\n" + indent(str(i))
        return txt

    def addModule(self, module):
        if module.name in self.modules:
            raise ModuleDuplicateErr(f"module with name '{module.name}' is declared twice.")
        
        self.modules[module.name] = module

        return self

    def find(self, key):
        return self.modules.get(key, None)


class OneParam:
    def __init__(self, name:str, val) -> None:
        self.name = name
        self.val = val 

    def __str__(self) -> str:
        txt = f"{self.name} = {str(self.val)}"
        return txt

class ParameterDuplicateErr(Exception):
    pass

class Parameter:
    def __init__(self) -> None:
        self.params = {}

    def addParam(self, oneparam:OneParam):
        # self.params = [oneparam] + self.params
        if oneparam.name in self.params:
            raise ParameterDuplicateErr(f"{oneparam.name} is declared twice.")
        self.params[oneparam.name] = oneparam
        return self

    def __str__(self) -> str:
        txt = "Parameter:"

        txtcore= ""
        for i in reversed(self.params.values()):
            txtcore += "\n" + str(i)

        return txt + indent(txtcore)


class PortTypeErr(Exception):
    pass


class PortInout(Enum):
    IN = auto()
    OUT = auto()


portInoutTable = dict(zip(PortInout, ["input", "output"]))
portInoutInvTable = dict(zip(["input", "output"], PortInout))

class PortType:
    def __init__(self, inout:PortInout, wiretype="wire") -> None:
        self.inout = inout 
        self.wiretype = wiretype

        # below is supposed to be detected while parsing
        # ptypes = ["input", "output"]
        # if ptype not in ptypes:
        #     raise PortTypeErr(f"{ptype} is not allowed as a port type.")


    def __str__(self) -> str:
        return portInoutTable[self.inout] + f" {self.wiretype}"


class OnePort:
    def __init__(self, ptype:PortType, name:str, msb=0, lsb=0) -> None:
        self.ptype = ptype 
        self.name = name 
        self.msb = msb 
        self.lsb = lsb 

    def __str__(self) -> str:
        txt = f"{str(self.ptype)} [{str(self.msb)}:{str(self.lsb)}] {str(self.name)}"
        return txt


class PortDuplicateErr(Exception):
    pass


class Port:
    def __init__(self) -> None:
        self.ports = {}

    def addPort(self, oneport:OnePort):
        if oneport.name in self.ports:
            raise PortDuplicateErr(f"{oneport.name} is declared twice")

        self.ports[oneport.name] = oneport
            
        return self

    def __str__(self) -> str:
        txt = "Port:"

        txtcore = ""
        for i in self.ports.values():
            txtcore += "\n" + str(i)

        if len(self.ports) == 0:
            txtcore += "\nNone"

        return txt + indent(txtcore)

    def getInports(self):
        lst = []
        for i in self.ports.values():
            if i.ptype.inout == PortInout.IN:
                lst += [i]
        return lst

    # def inoutClassify(self):
    #     inport, outport = [], []
    #     for p in self.ports:
    #         if p.ptype.inout == PortInout.IN:
    #             inport += [p]
    #         else:
    #             outport += [p]
    #     self.inport, self.outport = inport, outport

    def find(self, key):
        return self.ports.get(key, None)


class Wiredec:
    def __init__(self, name:str, wiretype:str, msb=0, lsb=0) -> None:
        self.name = name
        self.wiretype = wiretype
        self.msb = msb
        self.lsb = lsb
        
    def __str__(self) -> str:
        return f"{str(self.wiretype)} [{str(self.msb)}:{str(self.lsb)}] {str(self.name)}"


class TtypeErr(Exception):
    pass


class WireExprType(Enum):
    ID = auto()
    WIRECONCAT = auto()
    BINOP = auto()
    TEROP = auto()
    IDSLICE = auto()
    LITERAL = auto()
    UNAOP = auto()


class WireExpr: 
    """Rhs.
    """
    def __init__(self, ttype, data) -> None:
        """
        ttype
        1: ID (str)
        2: wireconcat (list)
        3: wireval wireop wireexpr (list(3))
        4: wireval? wireexpr : wireexpr (list(3))
        5: ID[n:m] (list(3) of arithexpr)
        6: '1 /'0 / LITWIRE (str)
        7: unaop wireval (list(2))
        """
        self.ttype = ttype
        self.data = data

    def __str__(self) -> str:
        txt = ""
        if self.ttype == WireExprType.ID:
            txt = str(self.data)
        elif self.ttype == WireExprType.WIRECONCAT:
            txt = f"{{{', '.join([str(i) for i in self.data])}}}"
        elif self.ttype == WireExprType.BINOP:
            txt = f"({str(self.data[0])}) {str(self.data[1])} {str(self.data[2])}"
        elif self.ttype == WireExprType.TEROP:
            txt = f"({str(self.data[0])})? {str(self.data[1])}: {str(self.data[2])}"
        elif self.ttype == WireExprType.IDSLICE:
            txt = f"{str(self.data[0])}[{str(self.data[1])}:{str(self.data[2])}]"
        elif self.ttype == WireExprType.LITERAL:
            txt = str(self.data)
        elif self.ttype == WireExprType.UNAOP:
            txt = f"{str(self.data[0])}{str(self.data[1])}"
        else:
            raise TtypeErr(f"{str(self.ttype)} is not allowed as ttype.")
        
        return txt
        
    def mergeConcat(self, concat):
        inst = WireExpr(WireExprType.WIRECONCAT, [self] + concat.data)
        return inst

    def getAllIDCore(self, anslist):
        if self.ttype == WireExprType.ID:
            anslist += [self.data]
        elif self.ttype == WireExprType.WIRECONCAT:
            for node in self.data:
                node.getAllIDCore(anslist)
        elif self.ttype == WireExprType.BINOP:
            uno, _, dos = self.data
            uno.getAllIDCore(anslist)
            dos.getAllIDCore(anslist)
        elif self.ttype == WireExprType.TEROP:
            for node in self.data:
                node.getAllIDCore(anslist)
        elif self.ttype == WireExprType.IDSLICE:
            anslist += [self.data[0]]
            _, msb, lsb = self.data
            msb.getAllIDCore(anslist)
            lsb.getAllIDCore(anslist)
        elif self.ttype == WireExprType.UNAOP:
            self.data[1].getAllIDCore(anslist)

        return

    def getAllID(self):
        ans = []
        self.getAllIDCore(ans)

        return ans

class ArithExprType(Enum):
    LITERAL = auto()
    BINOP = auto()

class ArithExpr:
    def __init__(self, ttype, data) -> None:
        """
        ttype
        1. LITERAL (str, maybe litwire/number/id)
        2. expr op expr (list(3))
        """
        self.ttype = ttype
        self.data = data

    def __str__(self) -> str:
        txt = ""
        if self.ttype == ArithExprType.LITERAL:
            txt = str(self.data)
        elif self.ttype == ArithExprType.BINOP:
            txt = f"{str(self.data[0])} {str(self.data[1])} {str(self.data[2])}"
        else:
            assert False

        return txt
        
    def getAllIDCore(self, anslist):
        if self.ttype == ArithExprType.LITERAL:
            pat = re.compile(r"[0-9]+|[0-9]+'(h|d|b)[0-9]+")
            if re.fullmatch(pat, self.data) is None:
                anslist += [self.data]
        elif self.ttype == ArithExprType.BINOP:
            uno, _, dos = self.data
            uno.getAllIDCore(anslist)
            dos.getAllIDCore(anslist)
        else:
            assert False 

    def getAllID(self):
        lst = []
        self.getAllIDCore(lst)
        return lst


class LhsType(Enum):
    ID = auto()
    IDSLICE = auto()
    LHSCONCAT = auto()


class Lhs:
    def __init__(self, ttype:LhsType, data) -> None:
        """
        ttype:
        1: ID (str)
        2: ID[n:m] (list(3))
        3: lhsconcat (list)
        """
        self.ttype = ttype
        self.data = data
        
    def __str__(self) -> str:
        txt = ""
        if self.ttype == LhsType.ID:
            txt = str(self.data)
        elif self.ttype == LhsType.IDSLICE:
            txt = f"{str(self.data[0])}[{str(self.data[1])}:{str(self.data[2])}]"
        else:
            assert self.ttype == LhsType.LHSCONCAT
            txt = f"{{{', '.join([str(i) for i in self.data])}}}"

        return txt

    def mergeConcat(self, concat):
        inst = Lhs(LhsType.LHSCONCAT, [self] + concat.data)
        return inst

    def getAllIDCore(self, anslist):
        if self.ttype == LhsType.ID:
            anslist += [self.data]
        elif self.ttype == LhsType.IDSLICE:
            anslist += [self.data[0]]
        else:
            assert self.ttype == LhsType.LHSCONCAT
            for node in self.data:
                node.getAllIDCore(anslist)

    def getAllID(self):
        ans = []
        self.getAllIDCore(ans)

        return ans


# class AssignDependency:
#     def __init__(self, ttype:AssignType, lhsId:list, rhsId:list, dependent=None) -> None:
#         self.ttype = ttype
#         self.lhsId = lhsId
#         self.rhsId = rhsId
#         self.dependent = dependent
        
#     def __str__(self) -> str:
#         txt = f"({joinNone(self.lhsId)}) {assigntypeTable[self.ttype]} ({joinNone(self.rhsId)})"
#         if self.dependent is not None:
#             txt += f" dependent to {joinNone(self.dependent)}"
#         return txt

#     def addDependent(self, depends:list):
#         if self.dependent is None:
#             self.dependent = []
#         self.dependent += depends 
#         return self
        

class Assign:
    def __init__(self, lhs:Lhs, rhs:WireExpr) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        txt = f"{str(self.lhs)} = {str(self.rhs)}"
        return txt

    def getNetDependency(self):
        return AssignDependency(AssignType.BLOCK, self.lhs.getAllID(), self.rhs.getAllID())


class AlwaysType(Enum):
    NONE = auto()
    FF = auto()
    COMB = auto()


class EdgeType(Enum):
    POS = auto()
    NEG = auto()


class Sensitivity:
    edgetype = dict(zip(EdgeType, ["posedge", "negedge"]))

    def __init__(self, edge:EdgeType, name:str) -> None:
        self.edge = edge
        self.name = name

    def __str__(self) -> str:
        txt = f"{Sensitivity.edgetype[self.edge]} {self.name}"
        return txt


class AlwaysAssign:

    def __init__(self, ttype:AssignType, lhs:Lhs, rhs:WireExpr) -> None:
        self.assigntype = ttype
        self.lhs = lhs 
        self.rhs = rhs 

    def __str__(self) -> str:
        txt = f"{str(self.lhs)} {assigntypeTable[self.assigntype]} {str(self.rhs)}"
        return txt

    def getNetDependency(self):
        data = AssignDependency(self.assigntype, self.lhs.getAllID(), self.rhs.getAllID())
        return data


class AlwaysIfblock:
    def __init__(self, cond:WireExpr, cont) -> None:
        # cont of AlwaysContent
        self.condition = cond 
        self.content = cont 

    def __str__(self) -> str:
        txt = f"If ({str(self.condition)}):\n" + indent(str(self.content))
        return txt

    def getNetDependency(self):
        return (self.condition.getAllID(), self.content.getNetDependency())


class AlwaysElseblock:
    def __init__(self, cont) -> None:
        # cont of always content
        self.content = cont

    def __str__(self) -> str:
        txt = "Else:\n" + indent(str(self.content))
        return txt

    def getNetDependency(self):
        return self.content.getNetDependency()


# class IfelseblockDependency:
#     def __init__(self, condwire:list, ifcontent, elsecontent=None) -> None:
#         # if/elsecontent of AlwaysContentDependency
#         self.condwire = condwire
#         self.ifcontent = ifcontent
#         self.elsecontent = elsecontent

#     def __str__(self) -> str:
#         txt = "If content with " + f"({', '.join(self.condwire) if len(self.condwire) > 0 else 'None'})"
#         txt += "\n" + indent("If clause:\n" + indent(str(self.ifcontent)))
#         txt += "\n" + indent("Else clause:\n" + indent(str(self.elsecontent)))
#         return txt

#     def addCondition(self, conds:list):
#         self.condwire += conds 
#         return self

#     def flatten(self):
#         newblockdata = []


        

class AlwaysIfelseblock:
    def __init__(self, ifblock:AlwaysIfblock, elseblock:AlwaysElseblock=None) -> None:
        self.ifblock = ifblock
        self.elseblock = elseblock

    def __str__(self) -> str:
        txt = str(self.ifblock)
        if self.elseblock is not None:
            txt += "\n" + str(self.elseblock)

        return txt

    def getNetDependency(self):
        condWires, ifcontents = self.ifblock.getNetDependency()
        if self.elseblock is not None:
            elsecontents = self.elseblock.getNetDependency()
        else:
            elsecontents = None

        # ifcont, elsecont, both are instances of AlwaysContentDependency
        return IfelseblockDependency(condWires, ifcontents, elsecontents)


# class AlwaysContentDependency:
#     def __init__(self, assign:list, ifelse:list) -> None:
#         # assignData, IfelseblockDependency
#         self.assign = assign
#         self.ifelse = ifelse

#     def __str__(self) -> str:
#         txt = "Assign contents:\n" + indent(strStrgen(self.assign)) + "\nIfelse contents:\n" + indent(strStrgen(self.ifelse))
#         return txt
        

class AlwaysContent:
    def __init__(self) -> None:
        self.assigns = []
        self.ifelseblocks = []

    def __str__(self) -> str:
        txt = "Assignments:\n"
        txtcore = strStrgen(self.assigns)
        txt += indent(txtcore)

        txt += "\nif/else blocks:\n"
        txt += indent(strStrgen(self.ifelseblocks))

        return txt

    def addAssign(self, assign:AlwaysAssign):
        self.assigns += [assign]
        return self

    def addIfelseblock(self, ifelseblock:AlwaysIfelseblock):
        self.ifelseblocks += [ifelseblock]
        return self

    def getNetDependency(self):
        assignData = [i.getNetDependency() for i in self.assigns]
        ifelseData = [i.getNetDependency() for i in self.ifelseblocks]

        return AlwaysContentDependency(assignData, ifelseData)


class Always:
    alwaystype = dict(zip(AlwaysType, ["always", "always_ff", "always_comb"]))

    def __init__(self, ttype:AlwaysType, sens:Sensitivity, cont:AlwaysContent) -> None:
        self.ttype = ttype 
        self.sensitivity = sens 
        self.content = cont 

    def __str__(self) -> str:
        txt = ""
        txt += Always.alwaystype[self.ttype]

        if self.ttype != AlwaysType.COMB:
            txt += f" @({str(self.sensitivity)})"

        txt += ":\n" + indent(str(self.content))

        return txt

    def getNetDependency(self):
        return  self.content.getNetDependency()


class WiredecDuplicateErr(Exception):
    pass


class ModuleContent:
    def __init__(self) -> None:
        self.wiredecs = {}
        self.assigns = []
        self.always = []

    def __str__(self) -> str:
        txt = ""
        # wire declarations
        txt += f"Wire declaration{'s' if len(self.wiredecs) > 1 else ''}:"
        
        txtcore = ""
        for i in reversed(self.wiredecs.values()):
            txtcore += "\n" + str(i)

        if len(self.wiredecs) == 0:
            txtcore += "\nNone"

        txt += indent(txtcore)

        # assign statements
        txt += f"\nAssign statement{'s' if len(self.wiredecs) > 1 else ''}:"
        txtcore = ""
        for i in reversed(self.assigns):
            txtcore += "\n" + str(i)

        if len(self.assigns) == 0:
            txtcore += "\nNone"

        txt += indent(txtcore)

        # always statements
        txt += "\nAlways blocks:"
        txtcore = ""
        for i in reversed(self.always):
            txtcore += "\n" + str(i)

        if len(self.assigns) == 0:
            txtcore += "\nNone"

        txt += indent(txtcore)

        txt = "ModuleContent:\n" + indent(txt)

        return txt

    def addWiredec(self, wiredec:Wiredec):
        if wiredec.name in self.wiredecs:
            raise WiredecDuplicateErr(f"{wiredec.name} is declared twice.")

        self.wiredecs[wiredec.name] = wiredec

        return self 

    def addAssign(self, assign:Assign):
        self.assigns += [assign]
        return self

    def addAlways(self, always:Always):
        self.always += [always]
        return self

    def findWiredec(self, key):
        return self.wiredecs.get(key, None)

    def getNetDependency(self):
        assignlst = [i.getNetDependency() for i in self.assigns]
        alwayslst = [i.getNetDependency() for i in self.always]
        return ModuleContentDependency(assignlst, alwayslst)


class Module:
    def __init__(self, name:str, content:ModuleContent, port:Port, param:Parameter=None) -> None:
        self.name = name
        self.content = content
        self.port = port 
        self.param = param

    def __str__(self):
        txt = f"Module {self.name}:"

        txtcore = ""
        if self.param is not None:
            txtcore += "\n" + str(self.param)
        txtcore += "\n" + str(self.port)
        txtcore += "\n" + str(self.content)

        return txt + indent(txtcore)

    def findDec(self, key):
        """Find the declaration of the wire by key.
        """
        uno = self.port.find(key)
        dos = self.content.findWiredec(key)

        ret = None 
        if uno is not None:
            if dos is not None:
                raise WiredecDuplicateErr(f"{key} is declared both as a port and as a wire.")
            ret = uno 
        else:
            ret = dos 

        return ret

    def getNetDependency(self):
        obj = self.content.getNetDependency()
        obj.addPortInfo(self.port)
        return obj
        