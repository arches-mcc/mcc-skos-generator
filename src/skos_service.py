import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, SKOS
import uuid
import math
import os
from settings import Settings
from pathlib import Path


def make_skos(
    main_project_root=None,
    csv_path=None,
    skos_prefLabel_columns=None,
    skos_definition_columns=None,
    skos_notes_columns=None,
    namespace=None,
    scheme_id=None,
    scheme_name=None,
    scheme_definition=None,
    concept_main_name=None,
    concept_main_definition=None,
    concept_narrower_name=None,
    concept_narrower_definition=None,
    output_file_name = None,
    output_file_path = None,
):    
    """
    Fonction pour créer un fichier SKOS (Simple Knowledge Organization System) au format XML à partir d'un fichier CSV. 
    Cette fonction permet de structurer et d'organiser des concepts hiérarchiques sous forme de thésaurus.

    Parameters:
    - main_project_root (str, optional): Chemin racine du projet principal. Utilisé pour définir le contexte général du fichier de sortie.
    - csv_path (str, optional): Chemin complet vers le fichier CSV contenant les données à convertir en format SKOS.
    - skos_prefLabel_columns (list, optional): Liste des colonnes du CSV à utiliser pour générer le label préférentiel (`skos:prefLabel`) du concept principal.
    - skos_definition_columns (list, optional): Liste des colonnes du CSV à utiliser pour générer la définition (`skos:definition`) du concept principal.
    - skos_notes_columns (list, optional): Liste des colonnes du CSV pour générer des notes supplémentaires (`skos:note`) associées au concept.
    - namespace (str, optional): URI de base pour le namespace RDF utilisé dans les identifiants des concepts. Définit l'espace de noms pour les URIs RDF.
    - scheme_id (str, optional): Identifiant unique pour le schéma de concepts SKOS. Utilisé pour référencer le schéma dans le fichier.
    - scheme_name (str, optional): Nom du schéma de concepts, représenté par `skos:ConceptScheme`.
    - scheme_definition (str, optional): Définition descriptive pour le schéma de concepts.
    - concept_main_name (str, optional): Nom du concept principal (root concept) à inclure dans le fichier SKOS.
    - concept_main_definition (str, optional): Définition textuelle du concept principal, utilisée dans `skos:definition`.
    - concept_narrower_name (str, optional): Nom du concept plus spécifique (narrower concept) qui est associé hiérarchiquement au concept principal.
    - concept_narrower_definition (str, optional): Définition du concept plus spécifique.
    - output_file_name (str, optional): Nom du fichier XML de sortie, dans lequel sera enregistré le SKOS généré.
    - output_file_path (str, optional): Chemin complet vers le dossier où le fichier XML sera sauvegardé. Si non spécifié, il sera sauvegardé dans le répertoire de travail courant.

    Returns:
    - None: La fonction crée un fichier XML en format SKOS et le sauvegarde sans retourner de valeur.

    Raises:
    - ValueError: Si le `csv_path` est invalide ou non spécifié. Le chemin du fichier CSV doit être un fichier valide pour que la fonction puisse traiter les données.
    - FileNotFoundError: Si le fichier CSV spécifié n'est pas trouvé au `csv_path`.
    - Exception: Pour d'autres erreurs générales liées à l'écriture du fichier de sortie ou à la création de l'arborescence XML.

    Exemple d'utilisation:
    ```python
    make_skos(
        main_project_root="/path/to/project",
        csv_path="/path/to/data.csv",
        skos_prefLabel_columns=["Nom", "Titre"],
        skos_definition_columns=["Description"],
        namespace="http://example.org/thesaurus/",
        scheme_id="conceptScheme1",
        scheme_name="Exemple Thesaurus",
        scheme_definition="Un exemple de thésaurus pour démonstration",
        concept_main_name="Concept Principal",
        concept_main_definition="Définition du concept principal",
        concept_narrower_name="Sous-concept",
        concept_narrower_definition="Définition du sous-concept",
        output_file_name="thesaurus.xml",
        output_file_path="/path/to/output"
    )
    ```

    Cette fonction est utile pour générer des fichiers SKOS destinés à la structuration de connaissances, facilitant l'interopérabilité et la gestion de données sémantiques.
    """
        
    # Charger les paramètres du fichier settings
    settings = Settings()
    
    params = {
        'main_project_root': main_project_root,
        'csv_path': csv_path,
        'namespace': namespace,
        'scheme_id': scheme_id,
        'scheme_name': scheme_name,
        'scheme_definition': scheme_definition,
        'concept_main_name': concept_main_name,
        'concept_main_definition': concept_main_definition,
        'concept_narrower_name': concept_narrower_name,
        'concept_narrower_definition': concept_narrower_definition,
        'skos_prefLabel_columns': skos_prefLabel_columns,
        'skos_definition_columns': skos_definition_columns,
        'skos_notes_columns': skos_notes_columns,
        'output_file_name': output_file_name,
        'output_file_path': output_file_path,
    }
    
    # Attribuer des valeurs par défaut depuis les paramètres si le paramètre est None
    for key, value in params.items():
        if value is None:
            params[key] = getattr(settings, key.upper(), None)

    params['output_file_name'] = params['output_file_name'] or str(uuid.uuid4())
    params['output_file_path'] = params['output_file_path'] or '/'
    params['main_project_root'] = params['main_project_root'] or '/workspaces'
    
    # Vérifier si un concept plus spécifique existe
    has_narrower = concept_narrower_name and concept_narrower_definition
    
    # Charger les données du fichier CSV
    if not params['csv_path']:
        raise Exception(f"Invalid CSV file path: '{params['csv_path']}'" )

    df = pd.read_csv(params['csv_path'])

    # Créer le graphe RDF
    g = Graph()

    # Définir un namespace pour les concepts
    NS = Namespace(namespace)
    g.bind("skos", SKOS)

    concept_scheme_uri = URIRef(NS[scheme_id]) if scheme_id else URIRef(NS[uuid.uuid4()])

    # Définir le schéma de concept principal
    g.add((concept_scheme_uri, RDF.type, SKOS.ConceptScheme))
    g.add(
        (
            concept_scheme_uri,
            SKOS.prefLabel,
            Literal(scheme_name, "fr"),
        )
    )
    g.add(
        (
            concept_scheme_uri,
            SKOS.definition,
            Literal(scheme_definition, "fr"),
        )
    )

    # Créer et ajouter des propriétés au concept principal
    concept_uri = get_new_uri(NS)
    g.add((concept_uri, RDF.type, SKOS.Concept))
    g.add(
        (
            concept_uri,
            SKOS.prefLabel,
            Literal(concept_main_name, lang="fr"),
        )
    )
    g.add(
        (
            concept_uri,
            SKOS.definition,
            Literal(concept_main_definition, lang="fr"),
        )
    )
    g.add((concept_scheme_uri, SKOS.hasTopConcept, concept_uri))
    g.add((concept_uri, SKOS.inScheme, concept_scheme_uri))  
    
    # Créer un nouveau URI pour le concept plus spécifique
    if has_narrower:
        concept_narrower_uri = get_new_uri(NS)
        g.add((concept_narrower_uri, RDF.type, SKOS.Concept))
        g.add((concept_narrower_uri, SKOS.inScheme, concept_scheme_uri))
        g.add((concept_narrower_uri, SKOS.prefLabel, Literal(concept_narrower_name, lang="fr")))
        g.add((concept_narrower_uri, SKOS.definition, Literal(concept_narrower_definition, lang="fr")))
        g.add((concept_uri, SKOS.narrower, concept_narrower_uri))


    # times = 0
    # Ajouter des concepts au graphe
    for _, row in df.iterrows():
        # if times == 2:
        #     continue
        
        cleaned_list_definition = clear_data(params['skos_definition_columns'], row)
        cleaned_list_prefLabel = clear_data(params['skos_prefLabel_columns'], row)
        cleaned_list_notes = clear_data(params['skos_notes_columns'], row)

        # Créer un URI pour un item spécifique dans le concept plus spécifique
        concept_item_uri = get_new_uri(NS)
        g.add((concept_item_uri, RDF.type, SKOS.Concept))
        g.add((concept_item_uri, SKOS.inScheme, concept_scheme_uri))
        g.add(
            (
                concept_item_uri,
                SKOS.prefLabel,
                Literal(" - ".join(cleaned_list_prefLabel), lang="fr"),
            )
        )
        g.add(
            (
                concept_item_uri,
                SKOS.definition,
                Literal(" - ".join(cleaned_list_definition), lang="fr"),
            )
        )
        
        if params['skos_notes_columns'] and cleaned_list_notes:
            g.add(
                (
                    concept_item_uri,
                    SKOS.note,
                    Literal(" - ".join(cleaned_list_notes), lang="fr"),
                )
            )
        # times += 1
        # Relier l'URI de l'item comme un concept plus spécifique
        if has_narrower:
            g.add((concept_narrower_uri, SKOS.narrower, concept_item_uri))
        else:
            g.add((concept_uri, SKOS.narrower, concept_item_uri))
        
    final_path = Path(params['main_project_root'],params['output_file_path'], params['output_file_name'])
    
    if final_path.suffix != ".xml":
        final_path = Path(f"{final_path}.xml")
        
    # Sauvegarder le graphe en format XML/RDF (SKOS)
    g.serialize(destination=final_path, format="xml")

    print(f"Fichier SKOS XML généré : {final_path}")
    return final_path

def clear_data(columns, row):
    """
    Nettoyer les données d'une ligne du DataFrame en supprimant les valeurs NaN et None.
    
    Parameters:
    - columns : liste des colonnes à nettoyer.
    - row : ligne du DataFrame.
    
    Returns:
    - Liste des valeurs nettoyées.
    """
    if isinstance(columns, str):
        columns = columns.replace(" ", "").split(",")
         
    row_data = row[columns].tolist()
    cleaned_list = [
            str(item)
            for item in row_data
            if item is not None and not (isinstance(item, float) and math.isnan(item))
        ]    
    return cleaned_list


def get_new_uri(NS):
    """
    Génère un nouvel URI unique.
    
    Parameters:
    - NS : namespace pour l'URI.
    
    Returns:
    - Un URI unique.
    """
    return URIRef(NS[str(uuid.uuid4())])
