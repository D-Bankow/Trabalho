import re

# ============================================================
# 1. Analisador Léxico (usando um autômato implícito via regex)
# ============================================================

TOKENS = [
    ("NUM", r'\d+'),
    ("ID", r'[a-zA-Z_]\w*'),
    ("PLUS", r'\+'),
    ("MINUS", r'-'),
    ("TIMES", r'\*'),
    ("DIV", r'/'),
    ("ASSIGN", r'='),
    ("LPAREN", r'\('),
    ("RPAREN", r'\)'),
    ("SPACE", r'\s+'),
]

def lexer(code):
    """Retorna uma lista de tokens válidos reconhecidos pelo AFD."""
    tokens = []
    pos = 0
    while pos < len(code):
        match = None
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                text = match.group(0)
                if token_type != "SPACE":  # ignora espaços
                    tokens.append((token_type, text))
                pos = match.end(0)
                break
        if not match:
            raise SyntaxError(f"Símbolo inválido em: {code[pos:]}")
    return tokens

# ============================================================
# 2. Analisador Sintático (Parser) — Gramática simples
# ============================================================
# Gramática (livre de contexto):
# EXPR -> TERM ((PLUS|MINUS) TERM)*
# TERM -> FACTOR ((TIMES|DIV) FACTOR)*
# FACTOR -> NUM | ID | LPAREN EXPR RPAREN | ID ASSIGN EXPR

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ("EOF", "")

    def eat(self, token_type):
        tok = self.peek()
        if tok[0] == token_type:
            self.pos += 1
            return tok
        raise SyntaxError(f"Esperado {token_type}, encontrado {tok}")

    def parse(self):
        node = self.expr()
        if self.peek()[0] != "EOF":
            raise SyntaxError("Tokens restantes inesperados!")
        return node

    def expr(self):
        node = self.term()
        while self.peek()[0] in ("PLUS", "MINUS"):
            op = self.eat(self.peek()[0])
            node = ("BIN_OP", op[1], node, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.peek()[0] in ("TIMES", "DIV"):
            op = self.eat(self.peek()[0])
            node = ("BIN_OP", op[1], node, self.factor())
        return node

    def factor(self):
        tok = self.peek()
        if tok[0] == "NUM":
            self.eat("NUM")
            return ("NUM", tok[1])
        elif tok[0] == "ID":
            self.eat("ID")
            if self.peek()[0] == "ASSIGN":
                self.eat("ASSIGN")
                expr_node = self.expr()
                return ("ASSIGN", tok[1], expr_node)
            return ("ID", tok[1])
        elif tok[0] == "LPAREN":
            self.eat("LPAREN")
            node = self.expr()
            self.eat("RPAREN")
            return node
        else:
            raise SyntaxError(f"Token inesperado: {tok}")

# ============================================================
# 3. Avaliação (interpretação simples)
# ============================================================

def eval_ast(node, env=None):
    if env is None:
        env = {}
    tipo = node[0]

    if tipo == "NUM":
        return int(node[1])
    elif tipo == "ID":
        return env.get(node[1], 0)
    elif tipo == "ASSIGN":
        _, var, expr = node
        val = eval_ast(expr, env)
        env[var] = val
        return val
    elif tipo == "BIN_OP":
        _, op, left, right = node
        l = eval_ast(left, env)
        r = eval_ast(right, env)
        if op == "+": return l + r
        if op == "-": return l - r
        if op == "*": return l * r
        if op == "/": return l / r
    else:
        raise ValueError(f"Nó inválido: {node}")

# ============================================================
# 4. Execução de Exemplo
# ============================================================
if __name__ == "__main__":
    code = "x = 3 + 5 * (2 - 1)"
    print("Código fonte:", code)

    tokens = lexer(code)
    print("\nTokens gerados:")
    for t in tokens:
        print(t)

    parser = Parser(tokens)
    ast = parser.parse()

    print("\nÁrvore sintática (AST):")
    print(ast)

    env = {}
    result = eval_ast(ast, env)
    print("\nResultado da execução:", result)
    print("Ambiente final:", env)
