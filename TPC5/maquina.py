import ply.lex as lex
import sys
import json 
from datetime import date

def print_balance_to_coins(balance: int):
    result_str = ""
    euros = int(balance / 100)
    cents = int(balance % 100)
    if (euros > 0):
        result_str += f"{euros}e"
    if (cents > 0):
        result_str += f"{cents}c"
    if (result_str == ""):
        result_str = "0c"
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

jsonFile = open(sys.argv[1],"r")

lista_produtos = json.load(jsonFile)
jsonFile.close()

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
    print(
    """
    cod      | nome      | quantidade    | preço
    -----------------------------------------------------"""
    )
    for index in range(0,len(lista_produtos)):
        print(
    f'    {lista_produtos[index]["cod"]}        {lista_produtos[index]["nome"]}        {lista_produtos[index]["quant"]}              {lista_produtos[index]["preco"]}'
    )

def t_MOEDA(t):
    r'MOEDA'
    t.lexer.begin('moeda')

def t_SELECIONAR(t):
    r'SELECIONAR'
    t.lexer.begin('selecionar')

#Como interpretado do enunciado, só se pode selecionar um item em cada "SELECIONAR", logo manda para estado inicial depois
def t_selecionar_NUMBER(t):
    r'[A-Z]\d+'
    item = next((prod for prod in lista_produtos if prod["cod"] == t.value), None)  # procurar prod por cód na lista
    if (item != None):
        preco_item = int(item["preco"] * 100)
        if (t.lexer.balance >= preco_item):
            if (item["quant"] > 0):
                t.lexer.balance -= preco_item

                next((d.update({"quant": d["quant"] - 1}) for d in lista_produtos if d["cod"] == t.value)) #reduzir quantidade de produto na lista

                print(f"Pode retirar o produto dispensado \"{item['nome']}\"")
                print(f"Saldo = {print_balance_to_coins(t.lexer.balance)}")
            else:
                print("Máquina já não possui mais desse artigo")
        else:
            print(f"Saldo insuficiente para satisfazer o seu pedido")
            print(f"Saldo = {print_balance_to_coins(t.lexer.balance)}; Pedido \"{item['nome']}\" = {print_balance_to_coins(preco_item)}")
    else:
        print("Máquina não possui esse artigo")

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
        total_bal = "Sem troco"
        print("Sem troco")
    else:
        print(f"Pode retirar o troco: {total_bal}.")

    print("Até à próxima")
    jsonFile = open(sys.argv[1],"w")
    jsonFile.write(json.dumps(lista_produtos, indent=4)) # escrever valores atualizados para mesmo json
    jsonFile.close()

    #end program
    exit(0)

t_ANY_ignore_COMMENT = r'\#.*'

def t_moeda_ignore_COMMA(t):
    r','

def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

print(f"{date.today()}, Stock carregado, Estado atualizado.")
print("Bom dia. Estou disponível para atender o seu pedido.")

# Build the lexer
lexer = lex.lex()
#state variables
lexer.balance = 0

for line in sys.stdin:
    lexer.input(line)
    for tok in lexer:
        print(tok)