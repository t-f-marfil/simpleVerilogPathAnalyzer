import sys
import re

from .svlex import lexer
from .svyacc import parser
from .svast import Source
from .svutils import indent

class NoCurrentModule(Exception):
    pass


class SourceAnalyzer:
    def __init__(self, src:Source) -> None:
        self.source = src 
        self.modulenames = src.moduleNames()

        print("loading the source file...")
        self.dependency = src.getNetDependency()

        self.currentmodulename:str = None 
        self.currentmodule = None
        self.currentdependency = None

        if len(self.modulenames) > 0:
            self.setCurrentModule(list(self.modulenames)[-1])

    def setCurrentModule(self, name:str):
        target = self.source.findModule(name)
        if target is None:
            print("No such module found.")
        else:
            self.currentmodule = target
            self.currentmodulename = name
            self.currentdependency = self.dependency[name]

    def findWire(self, wire:str):
        if self.currentmodule is None:
            raise NoCurrentModule("no current module set.")

        obj = self.currentdependency
        upperRegs = obj.findUpperRegister(wire)
        directParent = obj.findDirectDependency(wire)

        return upperRegs, directParent


# if __name__ == "__main__":
def main(arg):
    with open(arg) as f:
        data = f.read()

    print()
    src = parser.parse(data, lexer=lexer, tracking=True)
    inst = SourceAnalyzer(src)

    while True:
        print()
        s = input(f"{str(inst.currentmodulename)} > ")
        print()

        setmodule = re.compile(r"module [A-z0-9]+")

        if s == "quit":
            break 
        elif s == "modules":
            for name in inst.modulenames:
                print(indent(name))
        elif re.fullmatch(setmodule, s) is not None:
            modulename = s.split()[1]
            inst.setCurrentModule(modulename)
        elif s == "stats":
            # not very useful
            module = inst.currentmodule
            print(module)
        elif s == "flatten":
            lst = inst.currentdependency.flattenedAssigns
            for item in lst:
                print(indent(str(item)))
        else:
            try:
                up, direct = inst.findWire(s)
                print(indent(f"Direct dependency:\n  {str(None if direct == () or direct is None else ', '.join(direct))}\n"))
                print(indent(f"Upstream registers:\n  {str(None if up == [] or up is None else ', '.join(up))}"))
            except NoCurrentModule as e:
                print(e)