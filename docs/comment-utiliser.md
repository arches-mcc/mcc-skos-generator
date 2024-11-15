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

    Vous pouvez également importer skos_service dans un autre script Python et utiliser la fonction `make_skos()`.

    ``` python
    from skos_service import make_skos

    # Configuration des paramètres pour le fichier SKOS
    make_skos(
        csv_path="/chemin/vers/votre_fichier.csv",
        namespace="http://mcc:8000/", 
        scheme_id="b3b6ffcf-1eda-4f80-8140-be52fc343ea2", # Laisser vide pour un nouveau Thésaurus
        scheme_name="Nom du Schéma",
        scheme_definition="Définition du Schéma",
        concept_main_name="Nom Principal du Concept",
        concept_main_definition="Définition Principale du Concept",
        concept_narrower_name="Nom du Concept Plus Spécifique",
        concept_narrower_definition="Définition du Concept Plus Spécifique",
        skos_prefLabel_columns=["colonne1", "colonne2"],
        skos_definition_columns=["colonne3", "colonne4"],
        skos_notes_columns=["colonne5", "colonne6"],
        output_file_name="fichier_skos.xml",
        output_file_path="/chemin/vers/sortie/"
    )

    ```

    Cela permet de personnaliser les paramètres et de créer un fichier **SKOS** en fonction de vos besoins.

### Paramètres

#### Obligatoires

`csv_path (str)`: Chemin complet vers le fichier CSV contenant les données à convertir en SKOS.

`namespace (str)`: URI de base pour l'espace de noms RDF utilisé dans les identifiants des concepts.

`scheme_id (str)`: Identifiant unique pour le schéma de concepts SKOS. Laisser vide pour un nouveau Thésaurus.

`scheme_name (str)`: Nom du schéma de concepts, utilisé pour représenter le skos:ConceptScheme.

`scheme_definition (str)`: Définition descriptive associée au schéma de concepts.

`concept_main_name (str)`: Nom du concept principal (root concept).

`concept_main_definition (str)`: Définition textuelle du concept principal, utilisée dans le skos:definition.

#### Optionnels

`concept_narrower_name (str)`: Nom du concept plus spécifique (narrower concept).

`concept_narrower_definition (str)`: Définition du concept plus spécifique.

`skos_prefLabel_columns (list)`: Liste des colonnes du CSV utilisées pour générer les labels préférentiels (`skos:prefLabel`).

- Exemple : ["arrcod", "arrnom", "arrville"].
  
`skos_definition_columns (list)`: Liste des colonnes du CSV pour créer les définitions (`skos:definition`).

- Exemple : ["arrville", "arrcode", "arradr1"].

`skos_notes_columns (list)`:Liste des colonnes pour ajouter des notes (`skos:note`) aux concepts.

- Exemple : ["arrdateproelec", "president", "directeur"].

`output_file_name (str)`: Nom du fichier XML généré.

`output_file_path (str)`: Chemin complet où le fichier XML sera sauvegardé. Par défaut, il est enregistré dans le répertoire courant.

## Pour tester

Pour exécuter les tests, il suffit de lancer la commande depuis le répertoire `mcc-skos-generator/` dans le terminal :

``` shell
PYTHONPATH=src python -m unittest discover tests/
```
