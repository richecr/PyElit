# Sumário:

- [O que é PyElit ?](#o-que-é-pyelit-)
- [Funcionalidades](#funcionalidades)
- [Geoparsing](#geoparsing)
- [TopicModeling](#topicmodeling)

## O que é PyElit ?
PyElit, Extraction of Locations and Issues of a Text, é uma biblioteca open-source gratuita para realização de Geoparsing e Modelagem de Tópicos desenvolvida em Python.

Você trabalha com muitos textos ? Quer extrair localizações ?
Quer saber qual o problema urbano trata o seu texto ?

O PyElit foi criado especialmente para isso. Com ele é possível extrair localizações e classificar textos que em tópicos de problemas urbanos. No inicio, a biblioteca seria usada para um projeto que necessita de saídas como essas extração de localidades e a classificação dos textos em problemas urbanos. Pesquisa realizada no [Laboratório de Sistemas da Informação - UFCG](https://sites.google.com/view/lsi-ufcg).

Entretanto, foi decidido que a biblioteca seria disponibilizada para a comunidade. Sabemos que a biblioteca não é capaz de resolver todos os problemas, mas foi útil para o projeto que iniciou sua criação. Portanto, permitimos que os usuários da biblioteca possam fazer alterações no código fonte, adaptando ao seu problema para então obter melhores resultados em suas pesquisas, assim contribuindo para um maior número de pessoas.

E assim os usuários que conseguirem fazer melhorias poderia enviar PRs para o aprimoramento da biblioteca.

## Funcionalidades:
|  Funcionalidade  |  Descrição  |
|  --------------  |  ---------  |
|  Geoparsing      |  Permite extrair localizações de um texto qualquer.  |
|  TopicModeling   |  Permite classificar um dado texto para um determinado tópico de problemas urbanos  |

## Geoparsing
Detalhes de como funciona e como usar o Geoparsing da biblioteca.

- [Introdução](geoparsing/introdution.md)
    - [Objetivo](geoparsing/introdution.md#objetivo)
- [Como usar ?](geoparsing/introdution.md#como-usar-)
    - [Geoparsing em texto com case correto](geoparsing/introdution.md#geoparsing-com-case-correto-sem-utilização-do-gazetteer)
    - [Geoparsing em texto com case incorreto](geoparsing/introdution.md#geoparsing-com-case-incorreto-sem-utilização-do-gazetteer)
    - [Geoparsing com o gazetteer(disponibilizado pela própria biblioteca)](geoparsing/introdution.md#geoparsing-com-gazetteer)

## TopicModeling
Detalhes de como funciona e como usar o TopicModeling da biblioteca

- [Introdução](topic_modeling/introdution.md)
    - [Objetivo](#)
    - [Entendendo o funcionamento da classe](#)
- [Como usar ?](topic_modeling/introdution.md#como-usar-)
    - [Classificar um texto](topic_modeling/introdution.md#topicmodeling-classificar-um-texto)
    - [Imrpimir tópicos](topic_modeling/introdution.md#topicmodeling-imprimir-tópicos)
    - [Imprimir palavras chaves dos tópicos](topic_modeling/introdution.md#topicmodeling-imprimir-palavras-chaves-e-seus-pesos-em-cada-tópico)
    - [Representatividade do nome dos tópicos](topic_modeling/introdution.md#topicmodeling-mudar-representatividade-do-nomes-dos-tópicos)
    - [Imprimir tópico pelo ID](topic_modeling/introdution.md#topicmodeling-imprimir-um-tópico-por-meio-do-id-dele)