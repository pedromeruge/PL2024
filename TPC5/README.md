# TPC4: Máquina de vending
## 2024-02-24

## Autor:
- A100709
- Pedro Miguel Meruge Ferreira

## Resumo

Neste trabalho foi proposto um programa que simula a interação com uma máquina de vending. Exsitem disponíveis os comandos:
- `LISTAR`: devolve uma lista dos itens disponíveis na máquina, o seu ID e preço.
- `MOEDA`: inicia um estado de introdução de moedas. O utilizador pode depois escrever 1c,2c,5c,10c,50c,1e ou 2e para introduzir saldo na máquina. O estado é interrompido com o caractér `.`, indicando o saldo após introdução das moedas.
- `SELECIONAR`: acomponhado de seguida por um número, compra um item da máquina, se ele existir e o utilizador tiver saldo suficiente. O saldo é atualizado de acordo com o preço do item.
- `SAIR`: termina a interação com a máquina, devolvendo o troco em moedas

O [script](maquina.py) desenvolvido suporta-se no módulo **ply.lex** do python. Utiliza os estados léxicos **"selecionar"** e **"moeda"** para corretamente processar o input do utilizador. Utiliza também uma variável de estado **"balance"** para gerir o saldo do utilizador a cada momento.