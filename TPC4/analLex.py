import ply.lex as lex
import re

tokens = (
    'SELECT',
    'SKIP',
    'FIELD',
    'COMMA',
    'FROM',
    'WHERE',
    'COMPAREOP',
    'NUMBER',
    'SEMICOLON',
)

#Tokens constantes
t_SELECT = r'SELECT'
t_SKIP = r'[ \t]+'
t_FIELD = r'\w+'
t_COMMA =r','
t_FROM = r'FROM'
t_WHERE = r'WHERE'
t_COMPAREOP = r'(<=?|=|>=?)'
t_SEMICOLON = r';'

#Tokens com código
def t_NUMBER(t):
    r'[+-]?\d+(\.\d+)?'
    t.value = int(t.value)
    return t

#Track número de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Gerir erros
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

texto_teste = "SELECT id, nome, salario FROM empregados WHERE salário >= 820;"

lexer.input(texto_teste)

for tok in lexer:
    print(tok)