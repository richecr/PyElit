# Introdução

PyElit também é uma biblioteca que permite classificar textos que tratem de problemas urbanos. Por enquanto não é possível treinar o modelo com seus próprios dados.

## Objetivo

O módulo tem como objetivo classificar um texto em um dos problemas urbanos treinados no modelo: saneamento básico, trânsito, obras e diversos. O modelo foi treinado com reportagens do quadro de televisão: Calendário JPB do telejornal JPB da TV Cabo Branco afiliada da Rede Globo.

Permite também a visualização de documentos de textos daquele tópico, permite que vejamos as palavras chaves de um determinado tópico.

# Como Usar ?

A classe `TopicModeling` é bastante simple de ser utilizada. Basta importar e instanciar um objeto da classe e então chamar o método principal: `rate_text`.

Vamos ver alguns exemplos de como usar:

## TopicModeling: Classificar um texto

```python
topicModeling = TopicModeling()
result = topicModeling.rate_text("o ginásio da Escola Maria Honoriana Santiago está com obras paradas desde do início do ano.")

print("Tópicos e probabilidades:", result)
print("Tópico:", topicModeling.get_topic(r[0][0]))
```

Saídas para esse exemplo:

```python
Tópicos e probabilidades: [(2, 0.80940521), (0, 0.064506963), (1, 0.063506372), (3, 0.062581457)]
Tópico: obras
```

## TopicModeling: Imprimir tópicos

```python
topicModeling = TopicModeling()
print(topicModeling.print_topics())
```

Saída para esse exemplo:

```python
{0: 'saneamento', 1: 'trânsito', 2: 'obras', 3: 'diversos'}
```

## TopicModeling: Imprimir palavras chaves e seus pesos em cada tópico

```python
topicModeling = TopicModeling()

print(topicModeling.print_keywords(quant_max_palavras=2))
```

Saída para esse exemplo:

```python
[(0, '0.016*"água" + 0.015*"esgoto"'), (1, '0.025*"velocidad" + 0.024*"faixa"'), (2, '0.012*"escola" + 0.011*"obra"'), (3, '0.034*"estrada" + 0.015*"féria"')]
```

## TopicModeling: Mudar representatividade do nomes dos tópicos

```python
topicModeling = TopicModeling()

topicModeling.represent_topics([0, 1, 2, 3], ['Saneamento', 'Trânsito','Obras', 'Diversos'])
print(topicModeling.print_topics())
```

Saída para esse exemplo:

```python
{0: 'Saneamento', 1: 'Trânsito', 2: 'Obras', 3: 'Diversos'}
```

## TopicModeling: Imprimir um tópico por meio do id dele

```python
topicModeling = TopicModeling()

print(topicModeling.get_topic(id_topic=1))
```

Saída para esse exemplo:

```python
Tópico com id = 1: trânsito
```
