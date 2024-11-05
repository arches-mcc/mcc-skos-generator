import os
from dotenv import load_dotenv

class Settings:
    """
    Classe Settings : Cette classe charge les configurations de l'environnement 
    en utilisant les variables définies dans un fichier .env. Elle permet d'accéder 
    aux différents paramètres nécessaires pour la génération de fichiers SKOS.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialisation de la classe Settings. Cette méthode charge les variables 
        d'environnement du fichier .env à l'aide de la fonction load_dotenv() et 
        initialise les attributs de configuration.
        
        Attributs:
        - CSV_PATH : chemin vers le fichier CSV contenant les données.
        - NAMESPACE : namespace RDF à utiliser pour les URIs.
        - SCHEME_ID : identifiant unique pour le schéma de concept.
        - SCHEMA_NAME : nom du schéma de concept.
        - SCHEMA_DEFINITION : définition du schéma de concept.
        - CONCEPT_MAIN_NAME : nom principal du concept.
        - CONCEPT_MAIN_DEFINITION : définition principale du concept.
        - CONCEPT_NARROWER_NAME : nom d'un concept plus spécifique (narrower).
        - CONCEPT_NARROWER_DEFINITION : définition d'un concept plus spécifique (narrower).
        - SKOS_DEFINITION_COLUMNS : colonnes du fichier CSV contenant les définitions SKOS.
        - SKOS_PREFLABEL_COLUMNS : colonnes du fichier CSV contenant les labels préférentiels SKOS.
        """
        load_dotenv()
        self.CSV_PATH = os.environ.get('CSV_PATH')
        self.NAMESPACE = os.environ.get('NAMESPACE')
        self.SCHEME_ID = os.environ.get('SCHEME_ID')
        self.SCHEMA_NAME = os.environ.get('SCHEMA_NAME')
        self.SCHEMA_DEFINITION = os.environ.get('SCHEMA_DEFINITION')
        self.CONCEPT_MAIN_NAME = os.environ.get('CONCEPT_MAIN_NAME')
        self.CONCEPT_MAIN_DEFINITION = os.environ.get('CONCEPT_MAIN_DEFINITION')
        self.CONCEPT_NARROWER_NAME = os.environ.get('CONCEPT_NARROWER_NAME')
        self.CONCEPT_NARROWER_DEFINITION = os.environ.get('CONCEPT_NARROWER_DEFINITION')
        self.SKOS_DEFINITION_COLUMNS = os.environ.get('SKOS_DEFINITION_COLUMNS')
        self.SKOS_PREFLABEL_COLUMNS = os.environ.get('SKOS_PREFLABEL_COLUMNS')
        