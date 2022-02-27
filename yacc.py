from svlex import lexer
from svyacc import parser

with open("fabs.sv") as f:
    data = f.read()

# a = parser.parse(data, lexer=lexer, debug=True)
a = parser.parse(data, lexer=lexer, tracking=True)
# print(a)

fabs = a.find("fabs")
# print(fabs)
dep = fabs.getNetDependency()


# print(dep.directDependency)
# print(dep.trueReg)
# print(dep.findUpperRegister("dummy3"))
# dep.findUpperRegisterAll()
while True:
    s = input("wire?: ")
    if s == "quit":
        break 
    else:
        print(dep.findUpperRegister(s))

# always = fabs.content.always[0].content
# net = always.getNetDependency()
# print(net)

# for i in net.extractAssign():
#     print(i)


# assigns = cont.assigns
# target = assigns[0].rhs
# a = target.getAllID()
# print(a)