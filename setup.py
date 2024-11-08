"""
Ce fichier de configuration est utilisé pour configurer la distribution
du package Python. Il contient des informations essentielles telles que le nom
du package, la version, les packages inclus et les dépendances requises.

Ce fichier utilise setuptools, une bibliothèque pour faciliter la création,
la distribution et l'installation de packages Python.

Pour plus d'informations sur l'utilisation de setuptools, consultez :
https://setuptools.pypa.io/en/latest/userguide/quickstart.html
"""

from setuptools import setup, find_packages

setup(
    name="mcc_skos_service",
    version="0.0.1",
    description="Package for generating SKOS files from CSV",
    author="Thalles Lima",
    author_email="thalles.lima@systematix-qc.com",
    packages=find_packages(),
    package_dir={"": "src"},  # maps the package root to 'src'
    py_modules=["skos_service"],  # includes only the skos_service module
    install_requires=[
        "pandas",
        "rdflib",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "make-skos=skos_service:make_skos",
        ],
    },
)
