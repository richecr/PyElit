# Introdução

PyElit é uma biblioteca que permite realizar o geoparsing de um certo texto. Por enquanto não é possível treinar com um gazetteer passado, mas isso está com futuras funcionalidades da biblioteca.

## Objetivo

A biblioteca tem como um dos objetivos realizar o Geoparsing de textos, permitindo que seja utilizados gazetteer para melhorar as buscas, atualmente só tem o gazetteer de algumas regiões do estado da Paraíba, em grande parte nas cidades de: Campina Grande e João Pessoa.

E também tem como objetivo realizar a classificação de textos que envolvam certos tipos de problemas urbanos. Futuramente poderiamos permitir que o usuário da biblioteca forneça os textos para que então realizassemos o tratamento e a geração de tópicos.

# Como usar ?

A classe `Geoparsing` é bastante simples de usar, basta importar e iniciar um objeto como instância da classe.
O `geoparsing` é o principal método da classe, pois ele quem é responsável por realizar o geoparsing de textos.

Vamos ver alguns exemplos de como usar:

## Geoparsing com case correto **sem** utilização do gazetteer:

```python
geop = Geoparsing()
text = "Eu moro na rua João Sérgio de Almeida no bairro de bodocongó em Campina Grande."
a = geop.geoparsing(text=text, case_correct=True)
print(a)
```

Entidades reconhecidas nesse exemplo:

```python
["Rua João Sérgio de Almeida", "Bodócongo", "Campina Grande"]
```

## Geoparsing com case incorreto **sem** utilização do gazetteer:

```python
geop = Geoparsing()
text = "Eu moro na rua João Sérgio de Almeida no bairro de bodocongó em Campina Grande."
a = geop.geoparsing(text=text, case_correct=False)
print(a)
```

Entidades reconhecidas nesse exemplo:

```python
["Bodocongó"]
```

## Geoparsing com o gazetteer:

```python
geop = Geoparsing()
text = "Eu moro na rua João Sérgio de Almeida no bairro de bodocongó em Campina Grande.".lower()
a = geop.geoparsing(text=text, case_correct=True, gazetteer_cg=True)
print(a)
```

Entidades reconhecidas nesse exemplo:

```python
[["rua joao sergio de almeida", "campina grande", "bodocongo"]]
```
