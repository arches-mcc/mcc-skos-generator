import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, SKOS
import uuid
import math
import os
from .settings import Settings


def make_skos(
    csv_path=None,
    skos_prefLabel_columns=None,
    skos_definition_columns=None,
    namespace=None,
    scheme_id=None,
    scheme_name=None,
    scheme_definition=None,
    concept_main_name=None,
    concept_main_definition=None,
    concept_narrower_name=None,
    concept_narrower_definition=None,
):    
    """
    Fonction pour créer un fichier SKOS (Simple Knowledge Organization System) en format XML à partir d'un fichier CSV.

    Parameters:
    - csv_path : chemin vers le fichier CSV contenant les données.
    - skos_prefLabel_columns : colonnes à utiliser pour le label préférentiel (prefLabel) du concept.
    - skos_definition_columns : colonnes à utiliser pour la définition du concept.
    - namespace : namespace utilisé pour les URIs RDF.
    - scheme_id : identifiant unique pour le schéma de concept.
    - scheme_name : nom du schéma de concept.
    - scheme_definition : définition du schéma de concept.
    - concept_main_name : nom du concept principal.
    - concept_main_definition : définition du concept principal.
    - concept_narrower_name : nom du concept plus spécifique (narrower).
    - concept_narrower_definition : définition du concept plus spécifique.

    Raises:
    - Exception si le chemin du fichier CSV est invalide.
    """
    
    # Charger les paramètres du fichier settings
    settings = Settings()
    CSV_PATH = csv_path or settings.CSV_PATH
    NAMESPACE = namespace or settings.NAMESPACE
    SCHEME_ID = scheme_id or settings.SCHEME_ID
    SCHEMA_NAME = scheme_name or settings.SCHEMA_NAME
    SCHEMA_DEFINITION = scheme_definition or settings.SCHEMA_DEFINITION
    CONCEPT_MAIN_NAME = concept_main_name or settings.CONCEPT_MAIN_NAME
    CONCEPT_MAIN_DEFINITION = concept_main_definition or settings.CONCEPT_MAIN_DEFINITION
    CONCEPT_NARROWER_NAME = concept_narrower_name or settings.CONCEPT_NARROWER_NAME
    CONCEPT_NARROWER_DEFINITION = concept_narrower_definition or settings.CONCEPT_NARROWER_DEFINITION
    SKOS_PREFLABEL_COLUMNS = skos_prefLabel_columns or settings.SKOS_PREFLABEL_COLUMNS.split(',')
    SKOS_DEFINITION_COLUMNS = skos_definition_columns or settings.SKOS_DEFINITION_COLUMNS.split(',')
    
    # Vérifier si un concept plus spécifique existe
    has_narrower = CONCEPT_NARROWER_NAME and CONCEPT_NARROWER_DEFINITION
    
    # Charger les données du fichier CSV
    if not CSV_PATH:
        raise Exception(f"Invalid CSV file path: '{CSV_PATH}'" )
    df = pd.read_csv(CSV_PATH)

    # Créer le graphe RDF
    g = Graph()

    # Définir un namespace pour les concepts
    NS = Namespace(NAMESPACE)
    g.bind("skos", SKOS)

    concept_scheme_uri = URIRef(NS[SCHEME_ID]) if SCHEME_ID else URIRef(NS[uuid.uuid4()])

    # Définir le schéma de concept principal
    g.add((concept_scheme_uri, RDF.type, SKOS.ConceptScheme))
    g.add(
        (
            concept_scheme_uri,
            SKOS.prefLabel,
            Literal(SCHEMA_NAME, "fr"),
        )
    )
    g.add(
        (
            concept_scheme_uri,
            SKOS.definition,
            Literal(SCHEMA_DEFINITION, "fr"),
        )
    )

    # Créer et ajouter des propriétés au concept principal
    concept_uri = get_new_uri(NS)
    g.add((concept_uri, RDF.type, SKOS.Concept))
    g.add(
        (
            concept_uri,
            SKOS.prefLabel,
            Literal(CONCEPT_MAIN_NAME, lang="fr"),
        )
    )
    g.add(
        (
            concept_uri,
            SKOS.definition,
            Literal(CONCEPT_MAIN_DEFINITION, lang="fr"),
        )
    )
    g.add((concept_scheme_uri, SKOS.hasTopConcept, concept_uri))
    g.add((concept_uri, SKOS.inScheme, concept_scheme_uri))  
    
    # Créer un nouveau URI pour le concept plus spécifique
    if has_narrower:
        concept_narrower_uri = get_new_uri(NS)
        g.add((concept_narrower_uri, RDF.type, SKOS.Concept))
        g.add((concept_narrower_uri, SKOS.inScheme, concept_scheme_uri))
        g.add((concept_narrower_uri, SKOS.prefLabel, Literal(CONCEPT_NARROWER_NAME, lang="fr")))
        g.add((concept_narrower_uri, SKOS.definition, Literal(CONCEPT_NARROWER_DEFINITION, lang="fr")))
        g.add((concept_uri, SKOS.narrower, concept_narrower_uri))

    # Ajouter des concepts au graphe
    for _, row in df.iterrows():
        
        cleaned_list_definition = clear_data(SKOS_DEFINITION_COLUMNS, row)
        cleaned_list_prefLabel = clear_data(SKOS_PREFLABEL_COLUMNS, row)

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
        
        # Relier l'URI de l'item comme un concept plus spécifique
        if has_narrower:
            g.add((concept_narrower_uri, SKOS.narrower, concept_item_uri))
        else:
            g.add((concept_uri, SKOS.narrower, concept_item_uri))
        

    # Sauvegarder le graphe en format XML/RDF (SKOS)
    output_file = "fichier_skos.xml"
    g.serialize(destination=output_file, format="xml")

    print(f"Fichier SKOS XML généré : {output_file}")

def clear_data(list, row):
    """
    Nettoyer les données d'une ligne du DataFrame en supprimant les valeurs NaN et None.
    
    Parameters:
    - list : liste des colonnes à nettoyer.
    - row : ligne du DataFrame.
    
    Returns:
    - Liste des valeurs nettoyées.
    """
    row_data = row[list].tolist()
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
