from .svlex import lexer
from .svyacc import parser
# from .svast import Source
# from .svutils import indent

def parseSrc(data:str):
    src = parser.parse(data, lexer=lexer, tracking=True)
    return src