# Introduction

PyElit is a library that allows performing the geoparsing of a certain text. For now, it is not possible to train with a past gazetteer, but this is one of the future ideas for the library.

## Objective

One goal of the library is to perform text geoparsing, allowing gazetteer to be used for improved searches, currently, there is only the gazetteer in some regions of the state of Paraíba, widely in the cities of Campina Grande and João Pessoa.

# How to use ?

The `Geoparsing` class is quite simple to use, just import and instantiate an object of the class. The `geoparsing` is the main method of the class since it is responsible for performing the geoparsing of texts.

Let's see some examples of how to use:

## Geoparsing with the correct case **without** using the gazetteer:

```python
from pyelit import Geoparsing

geop = Geoparsing()
text = "Eu moro na Rua João Sérgio de Almeida no bairro de bodocongó em Campina Grande."
a = geop.geoparsing(text=text, case_correct=True)
print(a)
```

 Recognized entities in this example:

```python
["Rua João Sérgio de Almeida", "Bodócongo", "Campina Grande"]
```

## Geoparsing with incorrect case ** without ** use of the gazetteer:

```python
from pyelit import Geoparsing

geop = Geoparsing()
text = "Eu moro na Rua João Sérgio de Almeida no bairro de bodocongó em Campina Grande."
a = geop.geoparsing(text=text, case_correct=False)
print(a)
```

Entities recognized in this example:

```python
["Bodocongó"]
```

## Geoparsing with the gazetteer:

```python
from pyelit import Geoparsing

geop = Geoparsing()
text = "Eu moro na Rua João Sérgio de Almeida no bairro de bodocongó em Campina Grande.".lower()
a = geop.geoparsing(text=text, case_correct=True, gazetteer_cg=True)
print(a)
```

Recognized entities in this example

```python
[["rua joao sergio de almeida", "campina grande", "bodocongo"]]
```
