import ply.lex as lex
from ply.lex import TOKEN



# List of token names.   This is always required
_tokens = [
   'NUMBER',
   "LITWIRE",
   "ID",
   "NONBLOCK",
   "GEQ",
   "ALLHIGH",
   "ALLLOW",
   "LSHIFT",
   "RSHIFT",
   "EQ",
#    "LEQ",
   "CONDAND",
   "WILDCONN",

   "INCR",
   "DECR",
   "PLUSEQ",
   "MINUSEQ",
   "NEQ",

   "MINUSCOLON",
]

# Regular expression rules for simple tokens
t_MINUSCOLON = "-:"

t_INCR = r"\+\+"
t_DECR = "--"
t_PLUSEQ = r"\+="
t_MINUSEQ = "-="
t_NEQ = "!="

t_CONDAND = "&&"
t_WILDCONN = "\.\*"

t_NONBLOCK = "<="
t_GEQ = ">="
t_ALLHIGH = "'1"
t_ALLLOW = "'0"
t_LSHIFT = "<<"
t_RSHIFT = ">>"
t_EQ = "=="
# t_LEQ = "<="

literals = r"+-(){}[]*/;:,=?<>@~#&|^.%"

def t_LITWIRE(t):
    r"[0-9]+'(b|h|d)[0-9]+"
    return t

def t_NUMBER(t):
    r'\d+'
    # t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_COMMENT(t):
    r"(//.*)|(/\*(.|\n)*?\*/)|\(\*.*\*\)"

reserved = {
    "module": "MODULE",
    "endmodule": "ENDMODULE",
    "input": "INPUT",
    "output": "OUTPUT",
    "assign": "ASSIGN",
    "always": "ALWAYS",
    "always_ff": "ALWAYSFF",
    "always_comb": "ALWAYSCOMB",
    "posedge": "POSEDGE",
    "negedge": "NEGEDGE",
    "localparam": "LOCALPARAM",
    "parameter": "PARAMETER",
    "begin": "BEGIN",
    "end": "END",
    "wire": "WIRE",
    "reg": "REG",
    "logic": "LOGIC",
    "genvar" : "GENVAR",
    "if": "IF",
    "else": "ELSE",
    "for" : "FOR",

    "int" : "INT",
    "integer" : "INTEGER"
}

tokens = _tokens + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    raise Exception("Failed in lexing.")

# Build the lexer
lexer = lex.lex()

if __name__ == "__main__":
    with open("fabs.sv") as f:
        data = f.read()
    lexer.input(data)
    for i in lexer:
        print(i)