from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('./requirements.txt', 'r') as f:
    requirements = []
    for line in f:
        requirements.append(line.strip())


class PostDevelopCommand(develop):
    """Pos-installation for development mode."""

    def run(self):
        develop.run(self)


class PostInstallCommand(install):
    """Pos-installation for installation mode."""

    def run(self):
        check_call("python3 -m spacy download pt_core_news_sm".split())
        install.run(self)


setup(
    name='PyElit',
    version='0.1.1',
    author='Rich Elton',
    author_email='richelton14@gmail.com',
    description='Extraction of Locations and Issues of a Text',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    url="https://github.com/Rickecr/PyElit",
    project_urls={
        'Código fonte': 'https://github.com/Rickecr/PyElit',
    },
    keywords='geoparsing topic modeling geo locations text issues problems urbans',
    license='MIT',
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    }
)
