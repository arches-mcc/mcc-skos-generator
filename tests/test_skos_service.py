import unittest
import os
import pandas as pd
import uuid
from rdflib import Graph, SKOS
from src.skos_service import make_skos

class TestMakeSkos(unittest.TestCase):
    """
    Classe de test pour la fonction make_skos, qui génère un fichier SKOS à partir d'un fichier CSV.
    
    Méthodes :
        - setUp : Prépare les fichiers temporaires nécessaires pour les tests.
        - tearDown : Nettoie les fichiers temporaires créés pendant les tests.
        - test_skos_columns_as_list : Vérifie que les colonnes SKOS fonctionnent lorsque passées comme listes.
        - test_skos_columns_as_comma_separated_string : Vérifie le fonctionnement avec les colonnes passées comme chaîne de caractères.
        - test_make_skos_output_file_creation : Vérifie si le fichier de sortie SKOS est bien créé.
        - test_make_skos_valid_rdf : Vérifie si le fichier SKOS de sortie est un fichier RDF valide.
        - test_make_skos_concepts : Vérifie que les concepts SKOS sont correctement créés dans le fichier RDF.
        - test_make_skos_namespace : Vérifie que les concepts SKOS utilisent le namespace spécifié.
    """

    def setUp(self):
        """Prépare un fichier CSV temporaire pour les tests."""
        self.csv_path = "test_data.csv"
        self.output_file = "fichier_skos.xml"
        data = {
            "label": ["Concept 1", "Concept 2"],
            "label2": ["Concept 1", "Concept 2"],
            "label3": ["Concept 1", "Concept 2"],
            "definition": ["Definition 1", "Definition 2"],
            "definition2": ["Definition 1", "Definition 2"],
            "definition3": ["Definition 1", "Definition 2"],
            "note": ["Note 1", "Note 2"],
            "note2": ["Note 1", "Note 2"],
            "note3": ["Note 1", "Note 2"]
        }
        df = pd.DataFrame(data)
        df.to_csv(self.csv_path, index=False)

    def tearDown(self):
        """Supprime les fichiers temporaires créés pendant les tests."""
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_skos_columns_as_list(self):
        """Vérifie le fonctionnement avec les colonnes passées comme listes."""
        make_skos(
            csv_path=self.csv_path,
            skos_prefLabel_columns=["label"],
            skos_definition_columns=["definition"],
            skos_notes_columns=["note"],
            namespace="http://example.org/test#",
            scheme_id="test_scheme",
            scheme_name="Schéma de Test",
            scheme_definition="Définition du schéma de test",
            concept_main_name="Concept Principal",
            concept_main_definition="Définition du concept principal"
        )
        self.assertTrue(os.path.exists(self.output_file))

    def test_skos_columns_as_comma_separated_string(self):
        """Vérifie le fonctionnement avec les colonnes passées comme chaîne de caractères."""
        make_skos(
            csv_path=self.csv_path,
            skos_prefLabel_columns="label, label2, label3",
            skos_definition_columns="definition,definition2,definition3",
            skos_notes_columns="note,note2,note3",
            namespace="http://example.org/test#",
            scheme_id="test_scheme",
            scheme_name="Schéma de Test",
            scheme_definition="Définition du schéma de test",
            concept_main_name="Concept Principal",
            concept_main_definition="Définition du concept principal"
        )
        self.assertTrue(os.path.exists(self.output_file))

    def test_make_skos_output_file_creation(self):
        """Teste si le fichier de sortie SKOS est bien créé."""
        make_skos(
            csv_path=self.csv_path,
            skos_prefLabel_columns=["label"],
            skos_definition_columns=["definition"],
            skos_notes_columns=["note"],
            namespace="http://example.org/test#",
            scheme_id=str(uuid.uuid4()),
            scheme_name="Schéma de Test",
            scheme_definition="Un schéma de concept de test",
            concept_main_name="Concept Principal",
            concept_main_definition="Définition du concept principal"
        )
        self.assertTrue(os.path.exists(self.output_file))

    def test_make_skos_valid_rdf(self):
        """Teste si le fichier de sortie SKOS est un fichier RDF valide."""
        make_skos(
            csv_path=self.csv_path,
            skos_prefLabel_columns=["label"],
            skos_definition_columns=["definition"],
            skos_notes_columns=["note"],
            namespace="http://example.org/test#",
            scheme_id=str(uuid.uuid4()),
            scheme_name="Schéma de Test",
            scheme_definition="Un schéma de concept de test",
            concept_main_name="Concept Principal",
            concept_main_definition="Définition du concept principal"
        )
        g = Graph()
        g.parse(self.output_file, format="xml")
        self.assertGreater(len(g), 0, "Le graphe RDF doit contenir des triplets.")

    def test_make_skos_concepts(self):
        """Teste si les concepts SKOS sont correctement créés dans le fichier RDF de sortie."""
        make_skos(
            csv_path=self.csv_path,
            skos_prefLabel_columns=["label"],
            skos_definition_columns=["definition"],
            skos_notes_columns=["note"],
            namespace="http://example.org/test#",
            scheme_id=str(uuid.uuid4()),
            scheme_name="Schéma de Test",
            scheme_definition="Un schéma de concept de test",
            concept_main_name="Concept Principal",
            concept_main_definition="Définition du concept principal"
        )
        g = Graph()
        g.parse(self.output_file, format="xml")

        main_concept_uri = None
        for s, p, o in g.triples((None, None, None)):
            if str(o) == "Concept Principal":
                main_concept_uri = s
                break
        self.assertIsNotNone(main_concept_uri, "Le concept principal doit être présent dans le graphe RDF")

        narrower_concepts = list(g.triples((main_concept_uri, None, None)))
        self.assertGreater(len(narrower_concepts), 0, "Il doit y avoir des concepts plus spécifiques liés au concept principal.")

    def test_make_skos_namespace(self):
        """Teste si les concepts SKOS utilisent le namespace spécifié."""
        namespace = "http://example.org/test#"
        make_skos(
            csv_path=self.csv_path,
            skos_prefLabel_columns=["label"],
            skos_definition_columns=["definition"],
            skos_notes_columns=["note"],
            namespace=namespace,
            scheme_id="test_scheme",
            scheme_name="Schéma de Test",
            scheme_definition="Définition du schéma de test",
            concept_main_name="Concept Principal",
            concept_main_definition="Définition du concept principal"
        )
        g = Graph()
        g.parse(self.output_file, format="xml")

        uris = [str(s) for s, _, _ in g]
        for uri in uris:
            if uri.startswith("http"):
                self.assertTrue(uri.startswith(namespace), "Toutes les URI doivent utiliser l’espace de noms spécifié.")

if __name__ == "__main__":
    unittest.main()
