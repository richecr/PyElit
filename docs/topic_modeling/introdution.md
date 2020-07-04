# Introduction

PyElit is also a library that allows classifying texts that deal with urban problems. For now, it is not possible to train the model with your own data.

## Objective

The module aims to classify a text in one of the urban problems trained in the model: basic sanitation, traffic, works, and miscellaneous. The model was trained with television news reports: JPB Calendar of the JPB newscast of TV Cabo Branco affiliated with TV Globo.

It also allows the visualization of text documents of that topic, and also allows us to see the keywords for a given topic.

# How to use ?

The `TopicModeling` class is quite simple to use. Just import and instantiate an object of the class and then call the main method: `rate_text`.

Let's see some examples of how to use:

## Topic Modeling: Classify a text

```python
from pyelit import TopicModeling

topicModeling = TopicModeling()
result = topicModeling.rate_text("o ginásio da Escola Maria Honoriana Santiago está com obras paradas desde do início do ano.")

print("Topics and probabilities:", result)
print("Topic:", topicModeling.get_topic(r[0][0]))
```

Outputs for this example:

```python
Topics and probabilities: [(2, 0.80940521), (0, 0.064506963), (1, 0.063506372), (3, 0.062581457)]
Topic: obras
```

## Topic Modeling: Print topics

```python
from pyelit import TopicModeling

topicModeling = TopicModeling()
print(topicModeling.print_topics())
```

Output for this example:

```python
{0: 'saneamento', 1: 'trânsito', 2: 'obras', 3: 'diversos'}
```

## Topic Modeling: Print keywords and their weights on each topic

```python
from pyelit import TopicModeling

topicModeling = TopicModeling()
print(topicModeling.print_keywords(quant_max_palavras=2))
```

Output for this example:

```python
[(0, '0.016*"água" + 0.015*"esgoto"'), (1, '0.025*"velocidad" + 0.024*"faixa"'), (2, '0.012*"escola" + 0.011*"obra"'), (3, '0.034*"estrada" + 0.015*"féria"')]
```

## Topic Modeling: Change representativeness of topic names

```python
from pyelit import TopicModeling

topicModeling = TopicModeling()

topicModeling.represent_topics([0, 1, 2, 3], ['Sanitation', 'Traffic','Construction', 'Several'])
print(topicModeling.print_topics())
```

Output for this example:

```python
{0: 'Sanitation', 1: 'Traffic', 2: 'Construction', 3: 'Several'}
```

## Topic Modeling: Imprimir um tópico por meio do id dele

```python
from pyelit import TopicModeling

topicModeling = TopicModeling()

print("Topic with id = 1: " + topicModeling.get_topic(id_topic=1))
```

Output for this example:

```python
Tópico com id = 1: Traffic
```