from svlex import lexer
from svyacc import parser

with open("fabs.sv") as f:
    data = f.read()


# a = parser.parse(data, lexer=lexer, tracking=True, debug=True)
a = parser.parse(data, lexer=lexer, tracking=True)
print(a)

# for mod in a.modules.values():
#     print(mod.getNetDependency())

# print(dep.directDependency)
# print(dep.trueReg)
# print(dep.findUpperRegister("dummy3"))

dep = a.getNetDependency()
# dep.findUpperRegisterAll()

for i in dep[0].flattenedAssigns:
    print(i)
# print(a)
# print(dep.upperRegData)

# while True:
#     s = input("wire?: ")
#     if s == "quit":
#         break 
#     else:
#         print(dep.findUpperRegister(s))

# always = fabs.content.always[0].content
# net = always.getNetDependency()
# print(net)

# for i in net.extractAssign():
#     print(i)


# assigns = cont.assigns
# target = assigns[0].rhs
# a = target.getAllID()
# print(a)