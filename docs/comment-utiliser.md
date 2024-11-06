# Documentation pour MCC SKOS GENERATOR

## Installation

Assurez-vous que vous êtes dans le répertoire racine de votre projet, puis exécutez :

```shell
pip install .
```

Cela installera le script `mcc_skos_generator` et ses dépendances.

## Utilisation

Vous pouvez utiliser l'application de deux façons : directement avec le fichier main.py ou en important le module comme une bibliothèque.

1. Exécution via main.py

    Pour exécuter le script directement, utilisez la commande :

    ```shell
    python src/main.py
    ```

    Cette commande exécute le script principal et appelle la fonction   `make_skos()` pour générer un fichier **SKOS**.

2. Utilisation comme un package Python

    Vous pouvez également importer skos_service dans un autre script Python et utiliser la fonction make_skos().

    ``` python
    from skos_service import make_skos

    # Configuration des paramètres pour le fichier SKOS
    make_skos(
        csv_path="chemin/vers/votre_fichier.csv",
        namespace="http://exemple.com/namespace#",
        scheme_id="exemple_scheme_id",
        scheme_name="Nom du Schéma",
        scheme_definition="Définition du Schéma",
        concept_main_name="Nom Principal du Concept",
        concept_main_definition="Définition Principale du Concept",
        concept_narrower_name="Nom du Concept Plus Spécifique",
        concept_narrower_definition="Définition du Concept Plus Spécifique"
    )

    ```

    Cela permet de personnaliser les paramètres et de créer un fichier **SKOS** en fonction de vos besoins.

## Paramètres de make_skos

Voici les principaux paramètres acceptés par la fonction `make_skos()` :

- `csv_path` : chemin vers le fichier CSV.
- `namespace` : namespace RDF pour les URIs.
- `scheme_id` : identifiant du schéma de concept.
- `scheme_name` : nom du schéma de concept.
- `scheme_definition` : définition du schéma de concept.
- `concept_main_name` : nom du concept principal.
- `concept_main_definition` : définition du concept principal.
- `concept_narrower_name` : nom du concept plus spécifique.
- `concept_narrower_definition` : définition du concept plus spécifique.

## Pour tester

Pour exécuter les tests, il suffit de lancer la commande depuis le répertoire `mcc-skos-generator/` dans le terminal :

``` shell
PYTHONPATH=src python -m unittest discover tests/
```
