import svlex

# Test it out

with open("fabs.sv") as f:
    data = f.read()

# Give the lexer some input
svlex.lexer.input(data)

# Tokenize
while True:
    tok = svlex.lexer.token()
    if not tok:
        break      # No more input
    print(tok)