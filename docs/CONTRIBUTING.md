# Contributing

> You can contribute at will, you will always be welcome. But we have some rules to be followed so that everyone is well received by everyone and that everyone can contribute in a happy way :smiley:.

## Add/Update Features:

You looked at the application and thought of some features that should be added to the project ? :open_mouth:

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
- Finally, click on `Submit new issue`.

## Clone the repository

On the home page of the [repository](https://github.com/Rickecr/PyElit) there is a `Fork` button. When you click, just wait to complete the fork. Then it will create the repository in your account and now just clone in your machine, this:

```sh
git clone https://github.com/<name_user>/PyElit
```

When finished, you will have the repository on your computer and then just open in your preferred editor and make your changes.

Before creating your branch for your development:
```sh
git checkout -b <name_branch>
```

For the name of the branch use the number of the issue to facilitate, ex: `issue_17`.

And now can begin the development :smiley: .

When you have finished making your changes, you should commit your changes, but first:

```sh
git add .
```

The above command will prepare all modified files to be committed, going through all the changes that were made by you where you will decide if the change will be added(you must be inside the project folder to use the command).
Now just commit the changes:

```sh
git commit -m "<Your_message>"
```

Remember to use clear messages. If what you're solving already has an issue open, reference issue in the commit.
Ex: `git commit -m "#17 - Add contributing.md"`

And finally, you will submit the changes to the remote repository:

```sh
git push --set-upstream origin <name_branch>
```

This is only the first time that you will have to submit a new branch to the remote repository, next times, just:

```sh
git push
```

But that will only appear in your fork, the official repository will not have its changes now what ? :confused:

Calm down, now the `Pull Request` or `PR` comes to help

## Contribute to implementation:

After having forked and clone the project, choose your favorite text editor. Now it's time to code.

But calm there, first of all, you should **choose an issue** you want to work with. If the issue is about functionality that does not exist, you should create and say you're working on it, case it exists, you must say that you intend to work on the issue. And after doing that, now you are ready to **code**.

### Understanding the folders:

The project is in the folder `pyelit`.

It has the texts used to train the topic modeling.

- In the `dados` folder: It has the texts used to train the topic modeling.

- In the `docs` folder: It has the library's documentation files.

- In the `Geoparsing` folder: It has all the files about the features related to the geoparsing

  - In the `./gazetteer` folder: It has files of gazetteer used by the library.
  - In the `./utils` folder: It has files when has the functions that were/are used by the library. Ex: To process the data of the gazetteer.

- In the `Pre_processamento` folder: It has files used to data processing, functions that can be useful for geoparsing and topic modeling.

- In the `TopicModeling` folder: It has all the files about the features related to the topic modeling.

  - In the `modelo` folder: It has the Topic Modeling trained model.

### How to run the application:

We use the pipenv for better dependencies management.
So you need to install first of all:

- Install pipenv:

```bash
$ pip install pipenv
```

Now you should activate the virtualenv(here will be installed all the used libraries):

```bash
$ pipenv shell
```

Now you need to install the model pt-br of spacy:

```bash
$ python -m spacy download pt_core_news_sm
```

And you're done, you're ready to start development.

**NOTE:** Run the above command inside the project folder.

- You're now ready to implement your feature/fix.

### Run the tests:

```bash
$ pytest --disable-warnings
```

### Entering the pattern:

We have chosen to follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) standard. For this install the extension of [Python to VSCode](https://marketplace.visualstudio.com/items?itemName=ms-python.python). Another solution is to use the pycodestyle.

#### Pycodestyle:

It is already a dev-package in the project.

With the virtualenv activated, you can run the pycodestyle:

- To run the pycodestyle:

  ```bash
  pycodestyle .
  ```

##

## Performing a Pull Request - PR

On the page of your fork will appear a message in yellow requesting that you do open Pull Request to the original repository. By clicking will open a page for you to fill in the information about your PR.

- Reference the issue on what are you working using `#<issue_number>`.

- Describe your changes.

- Wait for the evaluation of your PR, and we may ask for some changes to be made.