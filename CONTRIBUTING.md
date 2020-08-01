# Contributing

> You can contribute at will, you will always be welcome. But we have some rules to be followed so that everyone is well received by everyone and that everyone can contribute in a happy way :smiley:.

## Add/Update Features:

You looked the application and thought of some feature that should be added to the project ? :open_mouth:

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

The project is in the folder `pyelit`.

It has the texts used to train the topic modeling.

- In the `dados` folder: It has the texts used to train the topic modeling.

- In the `docs` folder: It has the library's documentation files.

- In the `Geoparsing` folder: It has all the files about the features related with the geoparsing

  - In the `./gazetteer` folder: It has files of gazetteer used by the library.
  - In the `./utils` folder: It has files when has the functions that were/are used by the library. Ex: To process the data of gazetteer.

- In the `Pre_processamento` folder: It has files used to data processing, functions that can be useful for geoparsing and topic modeling.

- In the `TopicModeling` folder: It has all the files about the features related with the topic modeling.

  - In the `modelo` folder: It has the Topic Modeling trained model.

### How to run the application:

We use the poetry for better facility of management of the dependencies.
So you need to install first of all:

- Install pipenv:

```bash
$ pip install poetry
```

Now you should ativate the virtualenv(here will be installed all the used libraries):

```bash
$ poetry shell
```

Now you need install the model pt-br of spacy:

```bash
$ python -m spacy download pt_core_news_sm
```

And you're done, you're ready to start development.

**NOTE:** Run the above command inside the project folder.

- You're now ready to implement your feature/fix.

### Run the tests:

```bash
$ poetry run pytest --disable-warnings
```

### Entering the pattern:

We have chosen to follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) standard. For this install the extension of [Python to VSCode](https://marketplace.visualstudio.com/items?itemName=ms-python.python). Another solution is use the pycodestyle.

#### Pycodestyle:

It is already a dev-package in the project.

With the virtualenv ativated, you can run the pycodestyle:

- To run the pycodestyle:

  ```bash
  $ poetry run pycodestyle .
  ```

##

## Realizando uma Pull Request - PR

In page of the your fork will appear a message in yellow requesting that you do open Pull Request to the original repository. By clicking will open a page for you to fill in the information about your PR.

- Reference the issue on what are you working using `#<numero_da_issue>`.

- Describe your changes.

- Wait for the evaluation of your PR, and we may ask for some changes to be made.
