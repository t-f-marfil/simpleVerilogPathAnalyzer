# Yacc example

from numpy import isin
import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from svlex import tokens, lexer
from svast import *


def p_source(p):
    """
    source : moduledec source 
           | empty
    """
    if len(p) == 3:
        p[0] = p[2].addModule(p[1])
    else:
        assert len(p) == 2
        p[0] = Source()

    return


def p_moduledec(p):
    """
    moduledec : MODULE ID paramdec portdec ';' modulecontent ENDMODULE
              | MODULE ID portdec ';' modulecontent ENDMODULE
    """
    if len(p) == 8:
        inst = Module(p[2], p[6], p[4], p[3])
        p[0] = inst
    else:
        assert len(p) == 7
        inst = Module(p[2], p[5], p[3])
        p[0] = inst 

    return


def p_paramdec(p):
    """
    paramdec : '#' '(' params ')'
    """
    p[0] = p[3]
    return 


def p_params(p):
    """
    params : oneparam paramplus 
           | empty
    """
    if len(p) == 3:
        inst = p[2].addParam(p[1])
        p[0] = inst 
    else:
        p[0] = Parameter()

    return


def p_paramplus(p):
    """
    paramplus : ',' oneparam paramplus 
              | empty
    """
    if len(p) == 4:
        inst = p[3].addParam(p[2])
        p[0] = inst
    else:
        p[0] = Parameter()

    return
        

def p_oneparam(p):
    """
    oneparam : PARAMETER ID '=' arithexpr
    """
    p[0] = OneParam(p[2], p[4])
    return 


def p_arithexpr(p):
    """
    arithexpr : NUMBER
    """
    p[0] = int(p[1])
    return 


def p_portdec(p):
    """
    portdec : '(' ports ')'
    """
    p[0] = p[2]
    return 


def p_ports(p):
    """
    ports : oneport portplus 
          | empty
    """
    if len(p) == 3:
        p[0] = p[2].addPort(p[1])
    else:
        p[0] = Port()

def p_portplus(p):
    """
    portplus : ',' oneport portplus 
             | empty
    """
    if len(p) == 4:
        p[0] = p[3].addPort(p[2])
    else:
        p[0] = Port()

def p_oneport(p):
    """
    oneport : inouttype ID
            | inouttype '[' arithexpr ':' arithexpr ']' ID
    """
    if len(p) == 3:
        p[0] = OnePort(p[1], p[2])
    else:
        p[0] = OnePort(p[1], p[7], msb=p[3], lsb=p[5])

    return
    

def p_inouttype(p):
    """
    inouttype : INPUT
              | OUTPUT
              | INPUT wiretype
              | OUTPUT wiretype
    """
    if len(p) == 2:
        p[0] = PortType(portInoutInvTable[p[1]])
    else:
        p[0] = PortType(portInoutInvTable[p[1]], p[2])

    return


def p_modulecontent(p):
    """
    modulecontent : wiredec ';' modulecontent
                  | assign ';' modulecontent
                  | always modulecontent
                  | empty
    """
    if isinstance(p[1], Wiredec):
        p[0] = p[3].addWiredec(p[1])
    elif isinstance(p[1], Assign):
        p[0] = p[3].addAssign(p[1])
    elif isinstance(p[1], Always):
        p[0] = p[2].addAlways(p[1])
    else:
        assert len(p) == 2
        p[0] = ModuleContent()


def p_wiredec(p):
    """
    wiredec : wiretype '[' arithexpr ':' arithexpr ']' ID
            | wiretype ID
    """
    if len(p) == 8:
        p[0] = Wiredec(p[7], p[1], p[3], p[5])
    else:
        assert len(p) == 3
        p[0] = Wiredec(p[2], p[1])

def p_wiretype(p):
    """
    wiretype : WIRE
             | REG
             | LOGIC
    """
    p[0] = p[1]
    return 


def p_assign(p):
    """
    assign : ASSIGN lhs '=' wireexpr
    """
    p[0] = Assign(p[2], p[4])
    return 


def p_always(p):
    """
    always : ALWAYS '@' sensitivity alwayscontblock
           | ALWAYSFF '@' sensitivity alwayscontblock
           | ALWAYSCOMB alwayscontblock
    """
    if p[1] == "always":
        p[0] = Always(AlwaysType.NONE, p[3], p[4])
    elif p[1] == "always_ff":
        p[0] = Always(AlwaysType.FF, p[3], p[4])
    else:
        assert p[1] == "always_comb"
        p[0] = Always(AlwaysType.COMB, None, p[2])


def p_sensitivity(p):
    """
    sensitivity : '(' edge ID ')'
    """
    p[0] = Sensitivity(p[2], p[3])


def p_edge(p):
    """
    edge : POSEDGE
         | NEGEDGE
    """
    d = dict(zip(["posedge", "negedge"], EdgeType))
    p[0] = d[p[1]]


def p_alwayscontblock(p):
    """
    alwayscontblock : BEGIN alwayscont END 
    """
    p[0] = p[2]


def p_alwayscont(p):
    """
    alwayscont : oneassign ';' alwayscont
               | ifblock alwayscont
               | ifblock elseblock alwayscont
               | empty
    """
    if len(p) > 2 and p[2] == ';':
        p[0] = p[3].addAssign(p[1])
    elif len(p) == 3:
        inst = AlwaysIfelseblock(p[1])
        p[0] = p[2].addIfelseblock(inst)
    elif len(p) == 4:
        inst = AlwaysIfelseblock(p[1], p[2])
        p[0] = p[3].addIfelseblock(inst)
    else:
        assert len(p) == 2
        p[0] = AlwaysContent()


def p_oneassign(p):
    """
    oneassign : lhs '=' wireexpr
              | lhs NONBLOCK wireexpr
    """
    if p[2] == '=':
        p[0] = AlwaysAssign(AssignType.BLOCK, p[1], p[3])
    else:
        assert p[2] == "<="
        p[0] = AlwaysAssign(AssignType.NONBLOCK, p[1], p[3])


def p_ifblock(p):
    """
    ifblock : IF '(' wireexpr ')' BEGIN alwayscont END
    """
    p[0] = AlwaysIfblock(p[3], p[6])


def p_elseblock(p):
    """
    elseblock : ELSE ifblock
              | ELSE ifblock elseblock
              | ELSE BEGIN alwayscont END
    """
    if len(p) == 3:
        inst = AlwaysContent()
        inst.addIfelseblock(AlwaysIfelseblock(p[2]))
        p[0] = AlwaysElseblock(inst)
    elif len(p) == 4:
        inst = AlwaysContent()
        inst.addIfelseblock(AlwaysIfelseblock(p[2], p[3]))
        p[0] = AlwaysElseblock(inst)
    else:
        p[0] = AlwaysElseblock(p[3])



def p_lhs(p):
    """
    lhs : ID
        | ID '[' arithexpr ':' arithexpr ']'
        | '{' lhsconcat '}'
    """
    if len(p) == 2:
        p[0] = Lhs(LhsType.ID, p[1])
    elif len(p) == 7:
        p[0] = Lhs(LhsType.IDSLICE, [p[1], p[3], p[5]])
    else:
        p[0] = p[2]
    
    return 


def p_lhsconat(p):
    """
    lhsconcat : lhs
              | lhs ',' lhsconcat
    """
    if len(p) == 2:
        p[0] = Lhs(LhsType.LHSCONCAT, [p[1]])
    else:
        p[0] = p[1].mergeConcat(p[3])

    return 


def p_wireexpr(p):
    """
    wireexpr : wireval
             | wireval wireop wireexpr
             | wireval '?' wireexpr ':' wireexpr
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = WireExpr(WireExprType.BINOP, [p[1], p[2], p[3]])
    elif len(p) == 6:
        p[0] = WireExpr(WireExprType.TEROP, [p[1], p[3], p[5]])

    return 


def p_wireval_0(p):
    """
    wireval : ALLHIGH
            | ALLLOW
            | LITWIRE
            | '{' wireconcat '}'
            | '(' wireexpr ')'
            | ID '[' arithexpr ':' arithexpr ']'
            | ID '[' arithexpr ']'
            | unaop wireval
    """
    if len(p) == 2:
        p[0] = WireExpr(WireExprType.LITERAL, p[1])
    elif len(p) == 4:
        p[0] = p[2]
    elif len(p) == 7:
        p[0] = WireExpr(WireExprType.IDSLICE, [p[1], p[3], p[5]])
    elif len(p) == 5:
        p[0] = WireExpr(WireExprType.IDSLICE, [p[1], p[3], p[3]])
    else:
        assert len(p) == 3
        p[0] = WireExpr(WireExprType.UNAOP, [p[1], p[2]])

    return 


def p_unaop(p):
    """
    unaop : '~'
          | '&'
          | '^'
          | '|'
    """
    p[0] = p[1]


def p_wireval_1(p):
    """
    wireval : ID
    """
    p[0] = WireExpr(WireExprType.ID, p[1])
    return 


def p_wireconcat(p):
    """
    wireconcat : wireexpr
               | wireexpr ',' wireconcat
    """
    if len(p) == 2:
        p[0] = WireExpr(2, [p[1]])
    else:
        assert p[3].ttype == 2
        p[0] = p[1].mergeConcat(p[3])


def p_wireop(p):
    """
    wireop : '+'
           | '-'
           | '*'
           | '&'
           | '|'
           | '^'
           | '<'
           | '>'
           | EQ
           | GEQ
           | LEQ
    """
    p[0] = p[1]
    return 


def p_empty(p):
    """
    empty : 
    """
    return

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")
    # print("now parsing ", p.value)
    raise Exception(f"""failed in parsing.
now parsing '{p.value}' at line {p.lineno}""")

# Build the parser
parser = yacc.yacc()



# # lexer.input(data)

# a = parser.parse(data, lexer=lexer)
# print(a)