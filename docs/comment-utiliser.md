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
        imbrique=True,
        csv_path="/path/to/file.csv",
        csv_separateur=";",
        namespace="http://example.org/namespace",
        scheme_name="Exemple de schéma",
        scheme_definition="Définition du schéma",
        skos_main_concept_preflabel_columns=["NomConcept"],
        skos_narrow_concept_preflabel_columns=["NomSousConcept"],
        output_file_name="thesaurus.xml",
        output_file_path="/path/to/output"
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

#### Optionnels

`imbrique (bool)`: Indique si les concepts doivent être imbriqués. Par défaut, False. Si True, des valeurs dynamiques pour les concepts principaux et imbriqués seront extraites du CSV.

`concept_main_name (str)`: Nom du concept principal (root concept). Non utilisé si `imbrique=True`.

`concept_main_definition (str)`: Définition textuelle du concept principal, utilisée dans le skos:definition. Non utilisé si `imbrique=True`.

`concept_narrower_name (str)`: Nom du concept plus spécifique (narrower concept). Non utilisé si `imbrique=True`.

`concept_narrower_definition (str)`: Définition du concept plus spécifique. Non utilisé si `imbrique=True`.

`skos_main_concept_description_columns (list)` : Colonnes pour les descriptions des concepts principaux. Utilisé si `imbrique=True`.

`skos_main_concept_preflabel_columns (list)`:  Colonnes pour les labels préférentiels des concepts principaux. Obligatoire si `imbrique=True`.

`skos_narrow_concept_preflabel_columns  (list)` : Colonnes pour les labels des concepts plus spécifique imbriqués. Utilisé si `imbrique=True`.

`skos_narrow_concept_description_columns  (list)` : Colonnes pour les descriptions des concepts plus spécifique imbriqués. Utilisé si `imbrique=True`.

`skos_prefLabel_columns (list)`: Liste des colonnes du CSV utilisées pour générer les labels préférentiels (`skos:prefLabel`). Obligatoire si `imbrique=False`.

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
