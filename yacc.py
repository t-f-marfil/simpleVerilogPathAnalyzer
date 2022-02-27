from svast import Wiredec
from svlex import lexer
from svyacc import parser

with open("fabs.sv") as f:
    data = f.read()

# a = parser.parse(data, lexer=lexer, debug=True)
a = parser.parse(data, lexer=lexer, tracking=True)
# print(a)

fabs = a.find("fabs")

always = fabs.content.always[0].content
net = always.getNetData()
print(net)

for i in net.extractAssign():
    print(i)


# assigns = cont.assigns
# target = assigns[0].rhs
# a = target.getAllID()
# print(a)