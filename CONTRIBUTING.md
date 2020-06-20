# Contributing

> Pode contribuir a vontade, você será sempre bem-vindo(a). Mas temos algumas regras para serem seguidas para que todos sejam bem recebidos por todos e que todos possam contribuir de maneira feliz :smiley:.

## Adicionar/Atualizar funcionalidades

Você olhou a aplicação e pensou em alguma funcionalidade que deveria ser adicionada no projeto ? :open_mouth:

**_Então, você tem dois passos para seguir:_**

- [Abrir uma issue detalhando sua ideia](#criando-uma-issue)
- [Você mesmo implementar a funcionalidade](#contribuir-com-implementação)

## Criando uma issue

Na página do [projeto](https://github.com/Rickecr/PyElit), você pode clicar no botão `Issues` e na página irá aparecer um botão `new issue`, então é só selecionar e seguir os seguintes passos:

- Selecione o tipo da sua issue: `Bug ou Feature`.
- Dê um bom nome a sua issue.
- Detalhe bem sobre qual objetivo da issue.
- Imagens caso possível.
- Selecione labels para sua issue.
- Por fim, clique em `Submit new issue`.

## Clonar o repositório

Na página inicial do [repositório](https://github.com/Rickecr/PyElit) tem um botão `Fork`. Ao clicar é só esperar concluir o fork. E então ele irá criar o repositório na sua conta. E agora é só clonar em sua máquina, assim:

```sh
git clone https://github.com/<nome_de_usuario>/PyElit
```

Ao concluir, você terá o repositório em seu computador e então é só abrir em seu editor preferido e fazer suas modificações.

Antes você deve criar sua branch para seu desenvolvimento:

```sh
git checkout -b <nome_branch>
```

Para o nome da branch use o número da issue para facilitar, ex: `issue_17`.

E agora pode começar o desenvolvimento :smiley: .

Ao terminar suas modificações, você deve commitar suas alterações, mas primeiro:

```sh
git add .
```

O comando acima irá preparar todos os arquivos modificados para serem commitados, passando por todas as alterações que foram feitas por você onde decedirá se a alteração será adicionada (você deve estar dentro da pasta do projeto para usar o comando). Agora é só commitar as alterações:

```sh
git commit -m "<Sua_Mensagem>"
```

Lembre-se de usar mensagens claras. Se o que você está resolvendo já possui uma issue aberta, faça referência a issue no commit. Ex: `git commit -m "#17 - Add contributing.md"`

E por fim, você irá enviar as alterações para o repositório remoto:

```sh
git push --set-upstream origin <nome_branch>
```

Isso é apenas na primeira vez que vai enviar uma nova branch para o repositório remoto, nas próximas vezes, basta apenas:

```sh
git push
```

Mas isso só irá alterar no seu fork, o repositório oficial não vai ter suas alterações e agora ? :confused:

Calma, agora que entra a `Pull Request` ou `PR`

## Contribuir com implementação:

Depois de ter realizado o fork e o clone do projeto, escolhido seu editor de texto favorito. Então é hora de codar.

Mas calma ai, antes de qualquer coisa, você deve **escolher uma issue** que pretender trabalhar. Se a issue que trata sobre a funcionalidade não existir, você deve criar e dizer que esta trabalhando nela, caso ela exista você deve dizer lá(caso não já tenha alguém) que pretende trabalhar na issue. E após feito isso, agora sim você está pronto para **codar**.

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
