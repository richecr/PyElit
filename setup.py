from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'PyElit',
    version = '0.1.0',
    author = 'Rich Elton',
    author_email = 'richelton14@gmail.com',
    description = 'Extração de localizações e de problemas urbanos de textos',
    long_description = long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/Rickecr/PyElit",
    project_urls = {
        'Código fonte': 'https://github.com/Rickecr/PyElit',
    },
    keywords = 'geoparsing topic modeling',
    license = 'MIT'
)