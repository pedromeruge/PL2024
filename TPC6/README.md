# TPC6: GIC LL(1)
## 2024-03-16

## Autor:
- A100709
- Pedro Miguel Meruge Ferreira

## Resumo
Neste trabalho foi proposto o desenvolvimento de uma GIC (Gramática Independente de Contexto) para uma linguagem descrita num conjunto de frases exemplo fornecidas. A gramática devia ser do tipo LL(1), devendo ter atenção às prioridades dos operadores, calcular os lookaheads de todas as produções formuladas, e garantir que se verifica a condição LL(1). As frases eram:
- ?a
- b = a * 2 / (27-3)
- ! a + b
- c = a * b / (a / b)

## Resolução
Começei por desenvolver uma gramática sem atenção à ambiguidade, tendo depois criado mais símbolos não terminais, para garantir que os conjuntos de produções não tinham prefixos comuns. A gramática obtida é apresentada de seguida:

T = {`?`, `id`, `num`, `=`, `*`, `/`, `(`, `)`, `-`, `!`, `+`}

NT = {`S`,`Exp`,`ExpAux`,`Termo`,`TermoAux`,`DivTermo`,`Fator`}

```
P = {
    p1:  S → `?` Fator
    p2:    | `!` Exp
    p3:    | `id` `=` Exp

    p4:  Fator → `(` Exp `)`
    p5:        | num
    p6:        | id

    p7:  Exp → Termo ExpAux

    p8:  ExpAux → `+` Exp
    p9:         | `-` Exp
    p10:         | ε

    p11:  Termo → Fator TermoAux

    p12:  TermoAux → `*` Termo
    p13:          | `/` Fator
    p14:          | ε
}
```

## Validação 
Para testar a condição LL(1) começei por calcular os lookaheads das produções:

LA(p1) = {`?`}

LA(p2) = {`!`}

LA(p3) = {`id`}

LA(p4) = {`(`}

LA(p5) = {`num`}

LA(p6) = {`id`}

LA(p7) = FirstN(Termo) = FirstN(Fator) = {`(`, `num`, `id`}

LA(p8) = {`+`}

LA(p9) = {`-`}

LA(p10) = Follow(ExpAux) = Follow(Exp) = {`)`} U Follow(ExpAux) U Follow(S) = {`)`} U ∅ U {`$`} = {`)`, `$`}

LA(p11) = FirstN(Fator) = {`(`, `num`, `id`}

LA(p12) = {`*`}

LA(p13) = {`/`}

LA(p14) = Follow(TermoAux) = Follow(Termo) = FirstN(ExpAux) U Follow(TermoAux) = ({`+`, `-`} U Follow(ExpAux)) U Follow(Termo) = ({`+`, `-`} U Follow(Exp)) U ∅ = ({`+`, `-`} U {`)`, `$`}) U ∅ = {`+`, `-`, `)`, `$`}

Depois testei a condição LL(1) e verifiquei que, para cada conjunto de produções, a interseção dos lookaheads é o conjunto vazio, como pretendido:

- LA(p1) ∩ LA(p2) ∩ LA(p3) = {`?`} ∩ {`!`} ∩ {`id`} = ∅

- LA(p4) ∩ LA(p5) ∩ LA(p6) = {`(`} ∩ {`num`} ∩ {`id`} = ∅

- LA(p8) ∩ LA(p9) ∩ LA(p10) = {`+`} ∩ {`-`} ∩ {`)`, `$`} = ∅

- LA(p12) ∩ LA(p13) ∩ LA(p14) = {`*`} ∩ {`/`} ∩ {`+`, `-`, `)`, `$`} = ∅





