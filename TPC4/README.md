# TPC4: Analisador léxico
## 2024-03-05

## Autor:
- A100709
- Pedro Miguel Meruge Ferreira

## Resumo

Neste trabalho foi proposto um analisador léxico que processe a frase `SELECT id, name, salario FROM empregados WHERE salario >= 820;`, devolvendo uma lista dos tokens presentes nela.

O [script](analLex.py) desenvolvido suporta-se no módulo **ply.lex** do python. Foram identificados os tokens:
- `SELECT`: palavra "SELECT"
- `SKIP`: espaços e tabs
- `FIELD`: nome de variável de tabela
- `COMMA`: vírgula
- `FROM`: palavra "FROM"
- `WHERE`: palavra "WHERE"
- `COMPAREOP`: operadores de comparação, aka `<`,`=`,`>`,`<=`,`>=`
- `NUMBER`: float
- `SEMICOLON`: ponto e vírgula
- `NEWLINE`: \n para gerir número de linhas