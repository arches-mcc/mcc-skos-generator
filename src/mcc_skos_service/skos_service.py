import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, SKOS
import uuid
import math
from mcc_skos_service.settings import Settings
from pathlib import Path


def make_skos(
    imbrique = None,
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
    skos_main_concept_preflabel_columns=None,
    skos_main_concept_description_columns=None,
    concept_narrower_name=None,
    concept_narrower_definition=None,    
    skos_narrow_concept_preflabel_columns=None,
    skos_narrow_concept_description_columns=None,
    output_file_name = None,
    output_file_path = None,
):    
    """
    Génère un fichier SKOS (Simple Knowledge Organization System) à partir d'un fichier CSV, avec la possibilité d'inclure des concepts imbriqués.

    ### Paramètres :
    - **imbrique** (bool, optionnel) : Indique si les concepts doivent être imbriqués. Par défaut, `False`.
    - **main_project_root** (str, optionnel) : Répertoire racine du projet.
    - **csv_path** (str) : Chemin vers le fichier CSV contenant les données source.
    - **skos_prefLabel_columns** (list, optionnel) : Colonnes pour le label préférentiel (`skos:prefLabel`).
    - **skos_definition_columns** (list, optionnel) : Colonnes pour la définition (`skos:definition`).
    - **skos_notes_columns** (list, optionnel) : Colonnes pour les notes supplémentaires (`skos:note`).
    - **namespace** (str) : Espace de noms RDF pour les URIs.
    - **scheme_id** (str, optionnel) : Identifiant unique pour le schéma SKOS.
    - **scheme_name** (str) : Nom du schéma SKOS.
    - **scheme_definition** (str) : Définition du schéma SKOS.
    - **concept_main_name** (str, optionnel) : Nom du concept principal.
    - **concept_main_definition** (str, optionnel) : Définition du concept principal.
    - **skos_main_concept_preflabel_columns** (list, optionnel) : Colonnes pour les labels préférentiels des concepts principaux.
    - **skos_main_concept_description_columns** (list, optionnel) : Colonnes pour les descriptions des concepts principaux.
    - **concept_narrower_name** (str, optionnel) : Nom du concept plus spécifique.
    - **concept_narrower_definition** (str, optionnel) : Définition du concept plus spécifique.
    - **skos_narrow_concept_preflabel_columns** (list, optionnel) : Colonnes pour les labels des concepts imbriqués.
    - **skos_narrow_concept_description_columns** (list, optionnel) : Colonnes pour les descriptions des concepts imbriqués.
    - **output_file_name** (str, optionnel) : Nom du fichier SKOS généré.
    - **output_file_path** (str, optionnel) : Chemin où sauvegarder le fichier SKOS.

    ### Retour :
    - **str** : Chemin complet du fichier SKOS généré.

    ### Exceptions :
    - `FileNotFoundError` : Si le chemin CSV est invalide.
    - `ValueError` : Si certains paramètres obligatoires sont manquants.

    ### Exemple :
    ```python
    make_skos(
        csv_path="/path/to/file.csv",
        namespace="http://example.org/namespace",
        scheme_name="Exemple de schéma",
        scheme_definition="Définition du schéma",
        concept_main_name="Concept principal",
        concept_main_definition="Définition principale",
        output_file_name="thesaurus.xml",
        output_file_path="/path/to/output"
    )
    ```
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
        'imbrique': imbrique,
        'skos_main_concept_preflabel_columns': skos_main_concept_preflabel_columns,
        'skos_main_concept_description_columns': skos_main_concept_description_columns,
        'skos_narrow_concept_preflabel_columns': skos_narrow_concept_preflabel_columns,
        'skos_narrow_concept_description_columns': skos_narrow_concept_description_columns,
    }
    
    # Attribuer des valeurs par défaut depuis les paramètres si le paramètre est None
    params = load_params(settings, params)

    params['output_file_name'] = params['output_file_name'] or str(uuid.uuid4())
    params['output_file_path'] = params['output_file_path'] or '/'
    params['main_project_root'] = params['main_project_root'] or '/workspaces'
    params['imbrique'] = params['imbrique'] or False
    
    # Vérifier si un concept plus spécifique existe
    has_narrower = params['concept_narrower_name'] and params['concept_narrconcept_narrower_definitionower_name'] 
    
    # Charger les données du fichier CSV
    if not params['csv_path']:
        raise FileNotFoundError(f"Invalid CSV file path: '{params['csv_path']}'" )

    # Créer le graphe RDF
    g = Graph()

    # Définir un namespace pour les concepts
    NS = Namespace(params['namespace'])
    g.bind("skos", SKOS)

    concept_scheme_uri = URIRef(NS[ params['scheme_id']]) if params['scheme_id'] else get_new_uri(NS)

    # Définir le schéma (Thésaurus)
    definition_scheme(params['scheme_name'], params['scheme_definition'], g, concept_scheme_uri)
    
    if params['imbrique']:
        return make_skos_narrowed(params, g, NS, concept_scheme_uri)

    # Créer et ajouter des propriétés au concept principal
    concept_uri = create_concept(params['concept_main_name'],
                                      params['concept_main_definition'],
                                      '',
                                      g,
                                      NS,
                                      concept_scheme_uri,
                                      True)  
    
    # Créer un nouveau URI pour le concept plus spécifique
    if has_narrower:
        concept_narrower_uri = create_concept(params['concept_narrower_name'],
                                            params['concept_narrower_definition'],
                                            '',
                                            g,
                                            NS,
                                            concept_scheme_uri,
                                            False,
                                            concept_uri) 

    df = pd.read_csv(params['csv_path'])
    # times = 0
    # Ajouter des concepts au graphe
    for _, row in df.iterrows():
        # if times == 2:
        #     continue
        
        cleaned_list_definition = clear_data(params['skos_definition_columns'], row)
        cleaned_list_prefLabel = clear_data(params['skos_prefLabel_columns'], row)
        cleaned_list_notes = clear_data(params['skos_notes_columns'], row)

        # Créer un item spécifique dans le concept       
        create_concept(cleaned_list_prefLabel,
                       cleaned_list_definition,
                       cleaned_list_notes,
                       g,
                       NS,
                       concept_scheme_uri,
                       False,
                        concept_uri if not has_narrower else concept_narrower_uri)
               
        # times += 1
        
    final_path = Path(params['main_project_root'],params['output_file_path'], params['output_file_name'])
    
    if final_path.suffix != ".xml":
        final_path = Path(f"{final_path}.xml")
        
    # Sauvegarder le graphe en format XML/RDF (SKOS)
    g.serialize(destination=str(final_path), format="pretty-xml", encoding='utf-8')

    print(f"Fichier SKOS XML généré : {final_path}")
    return final_path

def make_skos_narrowed(params, g: Graph, NS: Namespace, concept_scheme_uri: URIRef):       
    """
    Génère un fichier SKOS avec des concepts principaux et leurs sous-concepts à partir d'un fichier CSV.

    ### Description :
    Cette fonction lit un fichier CSV, crée des concepts principaux (`main concepts`) et des sous-concepts 
    (`narrower concepts`) dans un graphe RDF en utilisant le vocabulaire SKOS. Chaque ligne du fichier CSV 
    peut contenir des données pour un concept principal et, éventuellement, un ou plusieurs sous-concepts 
    ou éléments associés.

    ### Paramètres :
    - **params** (dict) : Dictionnaire contenant les paramètres nécessaires à la génération du SKOS.
    - **g** (Graph) : Objet Graph pour gérer les données RDF.
    - **NS** (Namespace) : Namespace RDF pour générer des URIs uniques.
    - **concept_scheme_uri** (URIRef) : URI du schéma SKOS.

    ### Retour :
    - **Path** : Chemin complet du fichier SKOS généré.
    """
    #times = 0
    df = pd.read_csv(params['csv_path'], encoding='utf_8')
    main_concepts = {}
    for _, row in df.iterrows():
        # if times == 10:
        #     continue
        
        main_concept_list_prefLabel = clear_data(params['skos_main_concept_preflabel_columns'], row)
        main_concept_list_description = clear_data(params['skos_main_concept_description_columns'], row)
        narrow_concept_list_prefLabel = clear_data(params['skos_narrow_concept_preflabel_columns'], row)
        narrow_concept_list_description = clear_data(params['skos_narrow_concept_description_columns'], row)
        
        
        try:            
            main_concept_uri = main_concepts[main_concept_list_prefLabel]
        except KeyError:           
            main_concept_uri = create_concept(main_concept_list_prefLabel,
                                          main_concept_list_description,
                                          '',
                                          g,
                                          NS,
                                          concept_scheme_uri,
                                          True)
            main_concepts[main_concept_list_prefLabel] = main_concept_uri
                        
        has_narrower = bool(narrow_concept_list_prefLabel)
        if has_narrower:
            narrow_concept_uri = create_concept(narrow_concept_list_prefLabel,
                                            narrow_concept_list_description,
                                            '',
                                            g,
                                            NS,
                                            concept_scheme_uri,
                                            False,
                                            main_concept_uri)
            
            
        if params['skos_prefLabel_columns']:      
            item_cleaned_list_definition = clear_data(params['skos_definition_columns'], row)
            item_cleaned_list_prefLabel = clear_data(params['skos_prefLabel_columns'], row)
            item_cleaned_list_notes = clear_data(params['skos_notes_columns'], row)

            # Créer un item spécifique dans le concept       
            create_concept(item_cleaned_list_prefLabel,
                           item_cleaned_list_definition,
                           item_cleaned_list_notes,
                           g,
                           NS,
                           concept_scheme_uri,
                           False,
                            main_concept_uri if not has_narrower else narrow_concept_uri)
        
        
        # times+=1
    
    final_path = Path(params['main_project_root'],params['output_file_path'], params['output_file_name'])
    
    if final_path.suffix != ".xml":
        final_path = Path(f"{final_path}.xml")
        
    # Sauvegarder le graphe en format XML/RDF (SKOS)
    g.serialize(destination=str(final_path), format="xml", encoding='iso-8859-1')

    print(f"Fichier SKOS XML généré : {final_path}")
    return final_path
    

def load_params(settings, params):
    """
    Charge les paramètres par défaut à partir d'un objet `settings` si les valeurs des paramètres sont `None`.

    ### Paramètres :
    - **settings** : Objet contenant les paramètres par défaut.
    - **params** (dict) : Dictionnaire de paramètres utilisateur.

    ### Retour :
    - **dict** : Dictionnaire mis à jour avec les paramètres par défaut.
    """
    for key, value in params.items():
        if value is None:
            params[key] = getattr(settings, key.upper(), None)
    
    return params

def create_concept(
    name: str,
    definition: str,
    notes: str,
    g: Graph,
    NS: Namespace,
    concept_scheme_uri,
    is_top_concept=False,
    narrower_of=None
):
    """
    Crée un concept SKOS et ajoute ses relations au graphe RDF.

    ### Paramètres :
    - **name** (str) : Nom du concept.
    - **definition** (str) : Définition du concept.
    - **notes** (str, optionnel) : Notes associées au concept.
    - **g** (Graph) : Objet Graph pour le RDF.
    - **NS** (Namespace) : Namespace pour les URIs.
    - **concept_scheme_uri** : URI du schéma SKOS.
    - **is_top_concept** (bool, optionnel) : Définit si le concept est un top concept.
    - **narrower_of** (URIRef, optionnel) : URI d'un concept parent.

    ### Retour :
    - **URIRef** : URI du concept créé.
    """
    concept_new_uri = get_new_uri(NS)
    name_utf8 = Literal(name, lang="fr")
    definition_utf8 = Literal(definition, lang="fr")
    g.add((concept_new_uri, RDF.type, SKOS.Concept))
    g.add((concept_new_uri, SKOS.inScheme, concept_scheme_uri))
    g.add((concept_new_uri, SKOS.prefLabel, name_utf8))
    g.add((concept_new_uri, SKOS.definition, definition_utf8))
    
    if notes:
        notes_utf8 = Literal(notes, lang="fr")
        g.add((concept_new_uri, SKOS.note, notes_utf8))

    if is_top_concept:
        g.add((concept_scheme_uri, SKOS.hasTopConcept, concept_new_uri))
    if narrower_of:
        g.add((narrower_of, SKOS.narrower, concept_new_uri))

    return concept_new_uri

def definition_scheme(scheme_name, scheme_definition, g: Graph, concept_scheme_uri):
    """
    Définit un schéma SKOS dans le graphe RDF.

    ### Paramètres :
    - **scheme_name** (str) : Nom du schéma.
    - **scheme_definition** (str) : Définition du schéma.
    - **g** (Graph) : Graphe RDF.
    - **concept_scheme_uri** : URI du schéma.

    ### Retour :
    - **None** : Ajoute des triples au graphe RDF.
    """
    g.add((concept_scheme_uri, RDF.type, SKOS.ConceptScheme))
    g.add((concept_scheme_uri,SKOS.prefLabel,Literal(scheme_name, "fr")))
    g.add((concept_scheme_uri,SKOS.definition,Literal(scheme_definition, "fr")))

def clear_data(columns, row):
    """
    Nettoie une ligne du DataFrame en supprimant les valeurs `NaN` ou `None`.

    ### Paramètres :
    - **columns** (list ou str) : Colonnes à nettoyer.
    - **row** (pd.Series) : Ligne du DataFrame.

    ### Retour :
    - **str** : Valeurs concaténées et nettoyées sous forme de chaîne.
    """
    columns = normalize_str(columns)
    
    if columns == ['']:
        return ''
         
    row_data = row[columns].tolist()
    cleaned_list = [
            str(item)
            for item in row_data
            if item is not None and not (isinstance(item, float) and math.isnan(item))
        ]    
    return " - ".join(cleaned_list)

def normalize_str(columns):
    """
    Normalise une chaîne de caractères représentant des colonnes, en la transformant en une liste.

    ### Description :
    Cette fonction prend une chaîne de caractères où les colonnes sont séparées par des virgules,
    supprime les espaces inutiles, et retourne une liste des noms de colonnes. Si l'entrée est déjà
    une liste, elle est retournée telle quelle.

    ### Paramètres :
    - **columns** (str ou list) : Une chaîne de caractères contenant des colonnes séparées par des virgules
      ou une liste déjà normalisée.

    ### Retour :
    - **list** : Liste de noms de colonnes.
    """
    if isinstance(columns, str):
        columns = columns.replace(" ", "").split(",")
    return columns


def get_new_uri(NS):
    """
    Génère un nouvel URI unique dans le namespace.

    ### Paramètres :
    - **NS** (Namespace) : Namespace pour l'URI.

    ### Retour :
    - **URIRef** : URI unique généré.
    """
    return URIRef(NS[str(uuid.uuid4())])
