![](https://i.imgur.com/ccaix2x.png)

# Summary:

- [What is PyElit ?](#what-is-pyelit-)
- [Features](#features)
- [How to Install ?](#how-to-install-)
- [Geoparsing](#geoparsing)
- [Topic Modeling](#topic-modeling)
- [How to contribute ?](#contribuir)

## What is PyElit ?

PyElit, Extraction of Locations and Issues of a Text, is an library open-source to performing Geoparsing and Topic Modeling developed in Python. It was developed to be used in a research project at [Laboratório de Sistemas da Informação - UFCG](https://sites.google.com/view/lsi-ufcg). However it was decided that it would be better to make it available to the community and thereby allowing other developers to contribute to the library, whether with new features, improvements, reporting bugs and etc.

You work with very texts ? Want to extract locations ? Want to know which urban problem is addressed in a text ?

PyElit has as one of the objectives to perform the Geoparsing, allowing gazetteer to be used to improve the searches, currently there is only the gazetteer in some regions of the state of Paraíba, mostly in the cities of: Campina Grande and João Pessoa.

It also aims to classify texts that involve certain types of urban problems. In the future, we can allow library users to provide texts so that we can then process and generate topics.

We know that the library is not able to solve all problems, but it was useful for the project that started its creation. So we allow library users to make changes to the source code to adapt to their problem and then get betteer results in their research, and with that the library can be useful for a greater number of developers.

And so users who manage to make improvements will be able to send PR for the improvement of the library.

## Features:

| Features       | Description                                      |
| -------------- | ------------------------------------------------ |
| Geoparsing     | It allows extracting locations from any text.    |
| Topic Modeling | It allows you to classify text for a given topic |

## How to Install ?

PyElit version 0.1.2 is published in [PyPI](https://pypi.org/). So to install just run:

```sh
$ pip install PyElit
```

## Geoparsing

Details of how the library Geoparsing works.

- [Introduction](geoparsing/introdution.md)
  - [Objective](geoparsing/introdution.md#objetivo)
- [How to use ?](geoparsing/introdution.md#como-usar-)
  - [Geoparsin with correct case](geoparsing/introdution.md#geoparsing-com-case-correto-sem-utilização-do-gazetteer)
  - [Geoparsin with incorrect case](geoparsing/introdution.md#geoparsing-com-case-incorreto-sem-utilização-do-gazetteer)
  - [Geoparsing with the gazetteer(provided by the library itself)](geoparsing/introdution.md#geoparsing-com-gazetteer)

## Topic Modeling

Details of how the library Topic Modeling works.

- [Introduction](topic_modeling/introdution.md#introdução)
  - [Objective](topic_modeling/introdution.md#objetivo)
- [How to use ?](topic_modeling/introdution.md#como-usar-)
  - [Classify a text](topic_modeling/introdution.md#topicmodeling-classificar-um-texto)
  - [Print topics](topic_modeling/introdution.md#topicmodeling-imprimir-tópicos)
  - [Print topics keywords](topic_modeling/introdution.md#topicmodeling-imprimir-palavras-chaves-e-seus-pesos-em-cada-tópico)
  - [Representativeness of the name of the topics](topic_modeling/introdution.md#topicmodeling-mudar-representatividade-do-nomes-dos-tópicos)
  - [Print topic by ID](topic_modeling/introdution.md#topicmodeling-imprimir-um-tópico-por-meio-do-id-dele)

## How to contribute ?:

If you want to contribute to the project, you can start by taking a look [here](CONTRIBUTING-pt_br.md).
