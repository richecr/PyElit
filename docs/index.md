# Sumário:

- [O que é PyElit ?](#o-que-é-pyelit-)
- [Funcionalidades](#funcionalidades)
- [Geoparsing](#geoparsing)
- [TopicModeling](#topicmodeling)

## O que é PyElit ?

PyElit, Extraction of Locations and Issues of a Text, é uma biblioteca open-source para realização de Geoparsing e Modelagem de Tópicos desenvolvida em Python. É uma biblioteca desenvolvida para ser utilizada em um projeto de pesquisa no [Laboratório de Sistemas da Informação - UFCG](https://sites.google.com/view/lsi-ufcg). Entretanto foi decidido que seria melhor disponibilizar para a comunidade, assim permitindo que outros desenvolvedores possam contribuir para melhorar a biblioteca, seja com novas funcionalidades, melhorias, reportando BUGs e etc.

Você trabalha com muitos textos ? Quer extrair localizações ? Quer saber qual problema urbano é tratado em um texto ?

PyElit tem como um dos objetivos realizar o Geoparsing de textos, permitindo que seja utilizado gazetteer para melhorar as buscas, atualmente só tem o gazetteer de algumas regiões do estado da Paraíba, em grande parte nas cidades de: Campina Grande e João Pessoa.

E também tem como objetivo realizar a classificação de textos que envolvam certos tipos de problemas urbanos. Futuramente poderiamos permitir que os usuários da biblioteca forneça os textos para que então realizassemos o tratamento e a geração de tópicos.

Sabemos que a biblioteca não é capaz de resolver todos os problemas, mas foi útil para o projeto que deu inicio a sua criação. Portanto permitimos que os usuários da biblioteca possam fazer alterações no código fonte, adaptando ao seu problema para então obter melhores resultados em suas pesquisas, assim a biblioteca poderá ser útil para um maior número de pessoas.

E assim os usuários que conseguirem fazer melhorias poderá enviar PRs para o aprimoramento da biblioteca.

## Funcionalidades:

| Funcionalidade | Descrição                                                    |
| -------------- | ------------------------------------------------------------ |
| Geoparsing     | Permite extrair localizações de um texto qualquer.           |
| Topic Modeling | Permite classificar um dado texto para um determinado tópico |

## Como instalar:

A versão 0.1.2 do PyElit está publicada no [PyPI](https://pypi.org/). Portanto para instalar basta executar:

```sh
$ pip install PyElit
```

## Geoparsing

Detalhes de como funciona o Geoparsing da biblioteca.

- [Introdução](geoparsing/introdution.md)
  - [Objetivo](geoparsing/introdution.md#objetivo)
- [Como usar ?](geoparsing/introdution.md#como-usar-)
  - [Geoparsing em texto com case correto](geoparsing/introdution.md#geoparsing-com-case-correto-sem-utilização-do-gazetteer)
  - [Geoparsing em texto com case incorreto](geoparsing/introdution.md#geoparsing-com-case-incorreto-sem-utilização-do-gazetteer)
  - [Geoparsing com o gazetteer(disponibilizado pela própria biblioteca)](geoparsing/introdution.md#geoparsing-com-gazetteer)

## Topic Modeling

Detalhes de como funciona o Topic Modeling da biblioteca

- [Introdução](topic_modeling/introdution.md#introdução)
  - [Objetivo](topic_modeling/introdution.md#objetivo)
- [Como usar ?](topic_modeling/introdution.md#como-usar-)
  - [Classificar um texto](topic_modeling/introdution.md#topicmodeling-classificar-um-texto)
  - [Imrpimir tópicos](topic_modeling/introdution.md#topicmodeling-imprimir-tópicos)
  - [Imprimir palavras chaves dos tópicos](topic_modeling/introdution.md#topicmodeling-imprimir-palavras-chaves-e-seus-pesos-em-cada-tópico)
  - [Representatividade do nome dos tópicos](topic_modeling/introdution.md#topicmodeling-mudar-representatividade-do-nomes-dos-tópicos)
  - [Imprimir tópico pelo ID](topic_modeling/introdution.md#topicmodeling-imprimir-um-tópico-por-meio-do-id-dele)
