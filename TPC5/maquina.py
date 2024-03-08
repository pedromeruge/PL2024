import ply.lex as lex
import sys

def print_balance_to_coins(balance: int):
    result_str = ""
    euros = balance // 100
    cents = balance % 100
    if (euros > 0):
        result_str += f"{euros}e"
    if (cents > 0):
        result_str += f"{cents}c"
    return result_str

def convert_balance_to_coins(balance: int):
    result_coins = []
    coins = [("2e",200),("1e",100),("50c",50),("20c",20),("10c",10),("5c",5),("2c",2),("1c",1)]
    coin_iter = 0
    while balance > 0:
        curr_coin_type  = coins[coin_iter]
        n_coin = balance // curr_coin_type[1]
        balance = balance % curr_coin_type[1]
        if (n_coin > 0):
            result_coins.extend([curr_coin_type[0]] * n_coin)

        coin_iter = coin_iter + 1
    return result_coins

lista_produtos = [
    ("agua",50),
    ("bolo",60),
    ("agros",70),
    ("skittles",80),
    ("salame",50),
    ("mista",120),
    ("sandes",250)
]

states = (
    ('selecionar','exclusive'),
    ('moeda','exclusive')
)

tokens = [
    "SKIP",
    "COMMA",
    "CENTS",
    "EUROS",
    "LISTAR",
    "MOEDA",
    "SELECIONAR",
    "DOT",
    "SAIR"
]

def t_LISTAR(t):
    r'LISTAR'
    for index in range(0,len(lista_produtos)):
        print(f"{index+1}: {lista_produtos[index]}")

def t_MOEDA(t):
    r'MOEDA'
    t.lexer.begin('moeda')

def t_SELECIONAR(t):
    r'SELECIONAR'
    t.lexer.begin('selecionar')

#Como interpretado do enunciado, só se pode selecionar um item em cada "SELECIONAR", logo manda para estado inicial depois
def t_selecionar_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    if (t.value <= len(lista_produtos)):
        preco_item = lista_produtos[t.value-1][1]
        if (t.lexer.balance >= preco_item):
            t.lexer.balance -= preco_item
            print(f"COMPROU ITEM '{lista_produtos[t.value-1][0]}' CUST0: {print_balance_to_coins(lista_produtos[t.value-1][1])}")
            print(f"SALDO {print_balance_to_coins(t.lexer.balance)}")
        else:
            print(f"DINHEIRO INSUFICIENTE /!\\")
            print(f"SALDO: {print_balance_to_coins(t.lexer.balance)} | ITEM '{lista_produtos[t.value-1][0]}' CUSTA: {print_balance_to_coins(lista_produtos[t.value-1][1])}")
    else:
        print("ITEM INVÁLIDO")

    t.lexer.begin('INITIAL')

#Terminar inserção de moedas no estado MOEDAS
def t_moeda_DOT(t):
    r'\.'
    print(f"SALDO {print_balance_to_coins(t.lexer.balance)}")
    t.lexer.begin('INITIAL')
    # return t

def t_ANY_SKIP(t):
    r'[ \t]'

t_moeda_COMMA = r','

def t_moeda_CENTS(t):
    r'(1c|5c|10c|20c|50c)'
    t.value = int(t.value[:-1])
    t.lexer.balance += t.value
    # return t

def t_moeda_EUROS(t):
    r'(1e|2e)'
    t.value = int(t.value[:-1]) * 100
    t.lexer.balance += t.value
    # return t

def t_SAIR(t):
    r'SAIR'
    total_bal = ','.join(convert_balance_to_coins(t.lexer.balance))
    if total_bal == "":
        total_bal = "SEM TROCO"

    print(f"TROCO: {total_bal}")

    t.lexer.begin('INITIAL')
    # return t


t_ANY_ignore_COMMENT = r'\#.*'
def t_moeda_ignore_COMMA(t):
    r','

def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
#state variables
lexer.balance = 0

for line in sys.stdin:
    lexer.input(line)
    for tok in lexer:
        print(tok)