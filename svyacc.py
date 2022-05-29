# Yacc example
from numpy import isin
import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from .svlex import tokens, lexer
from .svast import *


precedence = (
    ("left", "+", "-"),
    ("left", "*"),
    ("left", "LSHIFT", "RSHIFT"),
    ("left", "GEQ", "NONBLOCK", "<", ">"),
    ("left", "EQ", "NEQ"),
    ("left", "&"),
    ("left", "^"),
    ("left", "|"),
    ("left", "CONDAND"),
    ("left", "?", ":")
)

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
    arithexpr : wireexpr
    """
    p[0] = p[1]
    return 

# def p_arithexpr(p):
#     """
#     arithexpr : NUMBER
#               | ID
#     """
#     p[0] = ArithExpr(ArithExprType.LITERAL, p[1])
#     return 

# def p_arithexpr(p):
#     """
#     arithexpr : onearith
#               | onearith arithop arithexpr
#     """
#     p[0] = p[1]
#     # ommiting info
#     return 


# def p_onearith(p):
#     """
#     onearith : NUMBER
#              | ID
#     """
#     p[0] = ArithExpr(ArithExprType.LITERAL, p[1])
#     return


# def p_arithop(p):
#     """
#     arithop : '+'
#             | '*'
#             | '-'
#             | '/'
#     """
#     p[0] = p[1]
#     return

def p_portdec(p):
    """
    portdec : '(' ports 
    """
    p[0] = p[2]
    return 


def p_ports(p):
    """
    ports : porttype  portplus
          | ')'
    """
    if len(p) == 3:
        uno, dos, tres = p[2]
        types, slices, ids = [p[1]] + uno, dos, tres
        inst = Port()
        for t, slice, idlist in zip(types, slices, ids):
            for i in idlist:
                po = OnePort(t, i) if slice is None else OnePort(t, i, slice[0], slice[1])
                inst.addPort(po)

        p[0] = inst

    else:
        p[0] = Port()

def p_portplus(p):
    """
    portplus : wireslice idsterminal portplus 
             | empty
    """
    if len(p) == 4:
        uno, dos, tres = p[3]
        newids, termtype = p[2]
        p[0] = [[termtype] + uno, [p[1]] + dos, [newids] + tres]
    else:
        # type, slice, ids
        p[0] = [[], [], []]


def p_idsterminal(p):
    """
    idsterminal : ID portterminal
                | ID ',' idsterminal
    """
    if len(p) == 3:
        p[0] = [[p[1]], p[2]]
    else:
        uno, dos = p[3]
        p[0] = [[p[1]] + uno, dos]


def p_portterminal(p):
    """
    portterminal : ')'
                 | ',' porttype
    """
    if len(p) == 2:
        p[0] = None 
    else:
        p[0] = p[2]


def p_wireslice(p):
    """
    wireslice : '[' arithexpr wiresliceop arithexpr ']'
              | empty
    """
    if len(p) == 6:
        p[0] = (p[2], p[4])
    else:
        assert len(p) == 2
        p[0] = None


def p_porttype(p):
    """
    porttype : inout
             | inout wiretype
    """
    if len(p) == 2:
        p[0] = PortType(portInoutInvTable[p[1]])
    else:
        p[0] = PortType(portInoutInvTable[p[1]], p[2])

    return


def p_inout(p):
    """
    inout : INPUT
          | OUTPUT
    """
    p[0] = p[1]


def p_modulecontent(p):
    """
    modulecontent : wiredec ';' modulecontent
                  | assign ';' modulecontent
                  | always modulecontent
                  | moduleinst ';' modulecontent
                  | lparamdec ';' modulecontent
                  | genvardec ';' modulecontent
                  | genfor modulecontent
                  | genifelse modulecontent
                  | empty
    """
    if isinstance(p[1], list):
        for i in p[1]:
            if isinstance(i, Wiredec):
                p[0] = p[3].addWiredec(i)
            else:
                assert isinstance(i, Assign)
                p[0] = p[3].addAssign(i)
    elif isinstance(p[1], Assign):
        p[0] = p[3].addAssign(p[1])
    elif isinstance(p[1], Always):
        p[0] = p[2].addAlways(p[1])
    elif p[1] is None and len(p) == 4:
        p[0] = p[3]
    else:
        assert len(p) == 2 or len(p) == 3
        p[0] = ModuleContent()


def p_genvardec(p):
    """
    genvardec : GENVAR genids 
    """

def p_genids(p):
    """
    genids : ID 
           | ID ',' genids
    """

def p_wiredec(p):
    """
    wiredec : wiretype '[' arithexpr wiresliceop arithexpr ']' idassigns
            | wiretype '[' arithexpr wiresliceop arithexpr ']' ID '[' arithexpr wiresliceop arithexpr ']'
            | wiretype idassigns
    """
    if len(p) == 8:
        lst = []
        for i in p[7]:
            name, rhsval = i 
            if rhsval is not None:
                lhs = Lhs(LhsType.ID, name)
                assignObj = Assign(lhs, rhsval)
                lst += [assignObj]
            lst += [Wiredec(name, p[1], p[3], p[5])]
        p[0] = lst
    elif len(p) == 13:
        p[0] = [Wiredec(p[7], p[1], p[9], p[11])]
    else:
        assert len(p) == 3
        lst = []
        for i in p[2]:
            name, rhsval = i 
            if rhsval is not None:
                lhs = Lhs(LhsType.ID, name)
                assignObj = Assign(lhs, rhsval)
                lst += [assignObj]
            lst += [Wiredec(name, p[1])]
        p[0] = lst


def p_ids(p):
    """
    idassigns : oneidassign 
              | oneidassign ',' idassigns
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[3] + [p[1]]


def p_idassign(p):
    """
    oneidassign : ID 
                | ID '=' wireexpr
    """
    if len(p) == 2:
        # assigned?, wireid
        p[0] = (p[1], None)
    else:
        p[0] = (p[1], p[3])


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
               | forblock alwayscont
               | ifblock elseblock alwayscont
               | empty
    """
    if len(p) > 2 and p[2] == ';':
        p[0] = p[3].addAssign(p[1])
    elif len(p) == 3:
        if p[1] is None:
            p[0] = p[1]
        else:
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


def p_genfor(p):
    """
    genfor : FOR forcond BEGIN genforcontent END 
           | FOR forcond BEGIN ':' ID genforcontent END
    """

def p_genforcontent(p):
    """
    genforcontent : modulecontent
    """

def p_genifelse(p):
    """
    genifelse : genif
              | genif genelse
    """

def p_genif(p):
    """
    genif : IF '(' wireexpr ')' BEGIN modulecontent END
    """

def p_genelse(p):
    """
    genelse : ELSE genif
            | ELSE BEGIN modulecontent END
    """

def p_forblock(p):
    """
    forblock : FOR forcond BEGIN alwayscont END
             | FOR forcond BEGIN ':' ID alwayscont END
    """

def p_forcond(p):
    """
    forcond : '(' dtype ID '=' NUMBER ';' ID compop wireexpr ';' forupdate ')'
            | '(' ID '=' NUMBER ';' ID compop wireexpr ';' forupdate ')'
    """

def p_forupdate(p):
    """
    forupdate : ID INCR
              | ID DECR
              | ID MINUSEQ ID
              | ID PLUSEQ ID
    """

def p_dtype(p):
    """
    dtype : INT
          | INTEGER
    """

def p_compop(p):
    """
    compop : '<'
           | '>'
           | GEQ
           | NONBLOCK
    """

def p_ifblock(p):
    """
    ifblock : IF '(' wireexpr ')' BEGIN alwayscont END
            | IF '(' wireexpr ')' oneassign ';'
    """
    if len(p) == 8:
        p[0] = AlwaysIfblock(p[3], p[6])
    else:
        assert len(p) == 7
        one = AlwaysContent().addAssign(p[5])
        p[0] = AlwaysIfblock(p[3], one)


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
        | ID '[' arithexpr wiresliceop arithexpr ']'
        | ID '[' wireexpr ']'
        | '{' lhsconcat '}'
        | genextract
    """
    if len(p) == 2:
        # genextract??
        p[0] = Lhs(LhsType.ID, p[1])
    elif len(p) == 7:
        p[0] = Lhs(LhsType.IDSLICE, [p[1], p[3], p[5]])
    elif len(p) == 5:
        p[0] = Lhs(LhsType.IDSLICE, [p[1], p[3], p[3]])
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
             | wireexpr '+' wireexpr
             | wireexpr '-' wireexpr
             | wireexpr '*' wireexpr
             | wireexpr '&' wireexpr
             | wireexpr '|' wireexpr
             | wireexpr GEQ wireexpr
             | wireexpr NONBLOCK wireexpr
             | wireexpr LSHIFT wireexpr
             | wireexpr RSHIFT wireexpr
             | wireexpr EQ wireexpr
             | wireexpr NEQ wireexpr
             | wireexpr CONDAND wireexpr
             | wireexpr '<' wireexpr
             | wireexpr '>' wireexpr
             | wireexpr '^' wireexpr
             | wireval '?' wireexpr ':' wireexpr
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = WireExpr(WireExprType.BINOP, [p[1], p[2], p[3]])
    elif len(p) == 6:
        p[0] = WireExpr(WireExprType.TEROP, [p[1], p[3], p[5]])
    # else:
    #     p[0] = p[1]

    return 

def p_wireval_0(p):
    """
    wireval : ALLHIGH
            | ALLLOW
            | LITWIRE
            | NUMBER
            | '{' wireconcat '}'
            | '(' wireexpr ')'
            | ID '[' wireexpr wiresliceop wireexpr ']'
            | ID '[' wireexpr ']'
            | unaop wireval
            | genextract
    """
    if len(p) == 2:
        # genextract???
        p[0] = WireExpr(WireExprType.LITERAL, p[1])
    elif len(p) == 4:
        p[0] = p[2]
    elif len(p) == 7:
        p[0] = WireExpr(WireExprType.IDSLICE, [p[1], p[3], p[5]])
    elif len(p) == 5:
        p[0] = WireExpr(WireExprType.IDSLICE, [p[1], p[3], p[3]])
    elif len(p) == 8:
        p[0] = p[7]
    else:
        assert len(p) == 3
        p[0] = WireExpr(WireExprType.UNAOP, [p[1], p[2]])

    return 

def p_genextract(p):
    """
    genextract : ID '[' wireexpr ']' '.' ID sliceornone
               | ID '[' wireexpr ']' '.' genextract
    """

def p_sliceornone(p):
    """
    sliceornone : empty
                | '[' wireexpr wiresliceop wireexpr ']'
                | '[' wireexpr ']'
    """

# def p_wirecore(p):
#     """
#     wirecore : ID
#              | ID '[' wireexpr wiresliceop wireexpr ']'
#              | ID '[' wireexpr ']'
#     """

def p_wiresliceop(p):
    """
    wiresliceop : ':'
                | MINUSCOLON
    """

# def p_wireval_0(p):
#     """
#     wireval : ALLHIGH
#             | ALLLOW
#             | LITWIRE
#             | NUMBER
#             | '{' wireconcat '}'
#             | '(' wireexpr ')'
#             | ID '[' arithexpr wiresliceop arithexpr ']'
#             | ID '[' wireexpr ']'
#             | unaop wireval
#     """
#     if len(p) == 2:
#         p[0] = WireExpr(WireExprType.LITERAL, p[1])
#     elif len(p) == 4:
#         p[0] = p[2]
#     elif len(p) == 7:
#         p[0] = WireExpr(WireExprType.IDSLICE, [p[1], p[3], p[5]])
#     elif len(p) == 5:
#         p[0] = WireExpr(WireExprType.IDSLICE, [p[1], p[3], p[3]])
#     else:
#         assert len(p) == 3
#         p[0] = WireExpr(WireExprType.UNAOP, [p[1], p[2]])

#     return 


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
        p[0] = WireExpr(WireExprType.WIRECONCAT, [p[1]])
    else:
        assert p[3].ttype == WireExprType.WIRECONCAT
        p[0] = p[1].mergeConcat(p[3])


# def p_wireop(p):
#     """
#     wireop : '+'
#            | '-'
#            | '*'
#            | '&'
#            | '|'
#            | '^'
#            | '<'
#            | '>'
#            | LSHIFT
#            | RSHIFT
#            | EQ
#            | GEQ
#            | NONBLOCK
#            | CONDAND
#            | NEQ
#     """
#     p[0] = p[1]
#     return 


def p_moduleinst(p):
    """
    moduleinst : ID '#' '(' paramassign ')' ID '(' modportassign ')'
               | ID ID '(' modportassign ')'
    """

def p_paramassign(p):
    """
    paramassign : oneparamassign 
                | oneparamassign ',' paramassign
                | WILDCONN
                | empty
    """

def p_oneparamassign(p):
    """
    oneparamassign : oneportassign
    """

def p_modportassign(p):
    """
    modportassign : oneportassign
                  | oneportassign ',' modportassign
                  | WILDCONN
                  | empty
    """

def p_oneportassign(p):
    """
    oneportassign : wireexpr
                  | '.' ID '(' wireexpr ')'
    """

def p_lparamdec(p):
    """
    lparamdec : LOCALPARAM lparams

    """

def p_lparams(p):
    """
    lparams : onelparam
            | onelparam ',' lparams
    """

def p_onelparam(p):
    """
    onelparam : ID '=' wireexpr
    """


def p_empty(p):
    """
    empty : 
    """
    return

# Error rule for syntax errors
def p_error(p):
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])

    print('Syntax error in input! Parser State:{} {} . {}'
          .format(parser.state,
                  stack_state_str,
                  p))
    print("Syntax error in input!")
    # print("now parsing ", p.value)
    raise Exception(f"""failed in parsing.
now parsing '{p.value}' at line {p.lineno}""")

# Build the parser
parser = yacc.yacc()



# # lexer.input(data)

# a = parser.parse(data, lexer=lexer)
# print(a)