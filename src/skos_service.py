import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, SKOS
import uuid
import math


def make_skos():
    # Charger les données du fichier CSV
    csv_file = "/workspaces/mcc-skos-script/fichiers/MUN.csv"
    df = pd.read_csv(csv_file)

    # Créer le graphe RDF
    g = Graph()

    # Définir un namespace pour les concepts
    NS = Namespace("http://mcc:8000/")
    g.bind("skos", SKOS)

    concept_scheme_uri = URIRef("http://mcc:8000/b3b6ffcf-1eda-4f80-8140-be52fc343ea2")
    concept_uri = get_new_uri(NS)

    # Definir o esquema de conceito e o conceito principal
    g.add((concept_scheme_uri, RDF.type, SKOS.ConceptScheme))
    g.add(
        (
            concept_scheme_uri,
            SKOS.prefLabel,
            Literal("Liste autorité immobilier GIPI", "fr"),
        )
    )
    g.add((concept_uri, RDF.type, SKOS.Concept))

    # Adicionar propriedades ao conceito principal
    g.add(
        (
            concept_uri,
            SKOS.prefLabel,
            Literal("Liste des municipalités", lang="fr"),
        )
    )
    g.add(
        (
            concept_uri,
            SKOS.definition,
            Literal("Renseignements sur les municipalités du Québec.", lang="fr"),
        )
    )
    g.add((concept_scheme_uri, SKOS.hasTopConcept, concept_uri))
    g.add((concept_uri, SKOS.inScheme, concept_scheme_uri))

    skos_definition_columns = [
        "munnom",
        "mdes",
        "regadm",
        "divrec",
        "mrc",
        "admregionale",
        "mgentile",
        "msuperf",
        "mpopul",
    ]

    # Cria um novo URI para o conceito narrower e define-o como skos:Concept
    concept_narrower_uri = get_new_uri(NS)
    g.add((concept_narrower_uri, RDF.type, SKOS.Concept))
    g.add((concept_narrower_uri, SKOS.inScheme, concept_scheme_uri))
    g.add((concept_narrower_uri, SKOS.prefLabel, Literal("Municipalités", lang="fr")))
    g.add((concept_uri, SKOS.narrower, concept_narrower_uri))

    # Ajouter des concepts au graphe
    for _, row in df.iterrows():

        row_data = row[skos_definition_columns].tolist()
        cleaned_list = [
            str(item)
            for item in row_data
            if item is not None and not (isinstance(item, float) and math.isnan(item))
        ]

        # Cria um URI para o item específico dentro do conceito narrower
        concept_item_uri = get_new_uri(NS)
        g.add((concept_item_uri, RDF.type, SKOS.Concept))
        g.add((concept_item_uri, SKOS.inScheme, concept_scheme_uri))
        g.add(
            (
                concept_item_uri,
                SKOS.prefLabel,
                Literal(f"{row['mcode']} - {row['munnom']}", lang="fr"),
            )
        )
        g.add(
            (
                concept_item_uri,
                SKOS.definition,
                Literal(" - ".join(cleaned_list), lang="fr"),
            )
        )

        # Relaciona o concept_item_uri como narrower de concept_narrower_uri
        g.add((concept_narrower_uri, SKOS.narrower, concept_item_uri))

    # Sauvegarder le graphe en format XML/RDF (SKOS)
    output_file = "fichier_skos.xml"
    g.serialize(destination=output_file, format="xml")

    print(f"Fichier SKOS XML généré : {output_file}")


def get_new_uri(NS):
    return URIRef(NS[str(uuid.uuid4())])
