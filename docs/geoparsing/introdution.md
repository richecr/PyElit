# Introduction

PyElit is a library that allows perform the geoparsing of a certain text. For now it is not possible to train with a past gazetteer, but this is like future ideas for the library.

## Objective

One of the objectives of the library is to perform text geoparsing, allowing gazetteer to be used to improve searches, currently there is only the gazetteer in some regions of the state of Paraíba, largely in the cities of: Campina Grande and João Pessoa.

# How to use ?

The `Geoparsing` class is quite simples of use, just import and instantiate an object of class. The `geoparsing` is main method of the class, since it is responsible for perform geopasring texts.

Let's see some examples of how use:

## Geoparsing with correct case **without** using the gazetteer:

```python
from pyelit import Geoparsing

geop = Geoparsing()
text = "Eu moro na Rua João Sérgio de Almeida no bairro de bodocongó em Campina Grande."
a = geop.geoparsing(text=text, case_correct=True)
print(a)
```

Entities recognized in this example:

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

Entities recognized in this example:

```python
[["rua joao sergio de almeida", "campina grande", "bodocongo"]]
```
