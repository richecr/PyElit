# Contributing

> You can contribute at will, you will always be welcome. But we have some rules to be followed so that everyone is well received by everyone and that everyone can contribute in a happy way :smiley:.

## Add/Update Features:

Você olhou a aplicação e pensou em alguma funcionalidade que deveria ser adicionada no projeto ? :open_mouth:

**_So you have two steps to follow:_**

- [Open an issue detailing your idea](#creating-an-issue)
- [You implement the functionality yourself](#contribuir-com-implementação)

## Creating an issue

On the [project](https://github.com/Rickecr/PyElit) page, you can click on the `Issues` button and a`new issue` button will appear on the page, then just select and follow the following steps:

- Select the type of your issue: `Bug ou Feature`.
- Give your issue a good name
- Detail very well about the purpose of the issue.
- Images if possible.
- Select labels for your issue.
- Finaly, click on `Submit new issue`.

## Clone the repository

On the home page of the [repository](https://github.com/Rickecr/PyElit) there is a `Fork` button. When you click, just wait to complete the fork. And then it will create the repository in your account. And now just clone in your machine, this:

```sh
git clone https://github.com/<name_user>/PyElit
```

When finished, you will have the repository on your computer and then just open in your preferred editor and make your changes.

Before you should create your branch for your development:

```sh
git checkout -b <name_branch>
```

For the name of the branch use the number of the issue to facilitate, ex: `issue_17`.

And now can begin the development :smiley: .

When you have finished make your changes, you should commit your changes, but first:

```sh
git add .
```

The above command will prepare all modified files to be committed, going through all the changes that were made by you where you will decide if the change will be added(you must be inside the project folder to use the command).
Now just commit the changes:

```sh
git commit -m "<Your_message>"
```

Remember to use message clear. If what you're solving already has an issue open, reference issue in commit.
Ex: `git commit -m "#17 - Add contributing.md"`

And finally, you will submit the changes to the remote repository:

```sh
git push --set-upstream origin <name_branch>
```

This is only the first time that submit a new branch to the remote repository, next times, just:

```sh
git push
```

But that will only in your fork, the official repository will not have its changes now what ? :confused:

Calm down, now that the `Pull Request` ou `PR`

## Contribute to implementation:

After having forked and clone the project, chosen your favorite text editor. Now it's time to code.

But calm there, first of all, you should **choose an issue** you want to work with. If the issue is about functionality does not exist, you should create and say you're working on it, case it exists, you must say that you intend to work on the issue. And after done that, now yes are you ready to **code**.

### Entendendo as pastas:

O projeto se encontra na pasta `pyelit`, estamos aceitando dicas de nomes para biblioteca também :blush: .

- Na pasta `dados`: Possue os textos usados para treinar o topic modeling.

- Na pasta `docs`: Encontra-se os arquivos de documentação da biblioteca.

- Na pasta `Geoparsing`: Encontra-se todos os arquivos sobre as funcionalidades relacionadas com o geoparsing.

  - Na pasta `./gazetteer`: Encontra-se os arquivos do gazetteer usados pela biblioteca.
  - Na pasta `./utils`: Encontra-se os arquivos onde tem as funções que foram/são utilizadas pela biblioteca. Ex: Para processar os dados do gazetteer.

- Na pasta `Pre_processamento`: Encontra-se os arquivos usados para processamentos dos dados, funções que podem ser uteis para o geoparsing e topic modeling.

- Na pasta `TopicModeling`: Encontra-se todos os arquivos sobre as funcionalidades relacionadas com o topic modeling.

  - Na pasta `modelo`: Encontra-se o modelo treinado do Topic Modeling.

### Como executar a aplicação:

Usamos o pipenv para melhor facilidade de gerenciamento das dependências.
Então é preciso instalar antes de tudo:

- Instalar o pipenv:

```bash
$ pip install pipenv
```

Agora você deve ativar o virtualenv(aqui já será instalada todas as libs utilizadas):

```bash
$ pipenv shell
```

Agora você precisar instalar o modelo em pt-br do spacy:

```bash
$ python -m spacy download pt_core_news_sm
```

E pronto, você está pronto para iniciar o desenvolvimento.

**OBS:** Executar o comando acima dentro da pasta do projeto.

- Agora você esta pronto para implementar sua funcionalidade/correção.

### Entrando nos padrões:

Nós optamos por seguir o padrão da [PEP 8](https://www.python.org/dev/peps/pep-0008/). Para isso instale a extensão do [Python para o VSCode](https://marketplace.visualstudio.com/items?itemName=ms-python.python). Outra solução é usar o pycodestyle.

#### Pycodestyle:

Ele já é uma dev-package no projeto.

Com o virtualenv ativado, você pode executar o pycodestyle:

- Para executar o pycodestyle:

  ```bash
  pycodestyle .
  ```

## Realizando uma Pull Request - PR

Na página do seu fork irá aparecer uma mensagem em amarelo solicitando que você faça uma Pull Request para o repositório original. Ao clicar irá abrir uma página para você preencher as informações sobre sua PR.

- Referencie a issue em que você está trabalhando usando `#<numero_da_issue>`

- Descreva suas modificações

- Espere pela avaliação da sua PR, e pode ocorrer de pedimos algumas alterações a seres feitas
