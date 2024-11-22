from pathlib import Path
import unittest
import os
import pandas as pd
import uuid
from rdflib import Graph, SKOS
from mcc_skos_service.skos_service import make_skos

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
        self.output_path = "mcc-skos-generator"
        self.output_file_path = "fichier_skos"
        self.main_project_root = "/workspaces"
        self.full_output_file = Path(self.main_project_root, self.output_path, f"{self.output_file_path}.xml")
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
        if os.path.exists(self.full_output_file):
            os.remove(self.full_output_file)

    def test_skos_columns_as_list(self):
        """Vérifie le fonctionnement avec les colonnes passées comme listes."""
        self.full_output_file = make_skos(
            csv_path=self.csv_path,
            imbrique=False,
            csv_separateur=',',
            skos_prefLabel_columns=["label"],
            skos_definition_columns=["definition"],
            skos_notes_columns=["note"],
            namespace="http://example.org/test#",
            scheme_id="test_scheme",
            scheme_name="Schéma de Test",
            scheme_definition="Définition du schéma de test",
            concept_main_name="Concept Principal",
            concept_main_definition="Définition du concept principal",
            output_file_name=self.output_file_path,
        )
        self.assertTrue(os.path.exists(self.full_output_file))

    def test_skos_columns_as_comma_separated_string(self):
        """Vérifie le fonctionnement avec les colonnes passées comme chaîne de caractères."""
        self.full_output_file = make_skos(
            csv_path=self.csv_path,
            imbrique=False,
            csv_separateur=',',
            skos_prefLabel_columns="label, label2, label3",
            skos_definition_columns="definition,definition2,definition3",
            skos_notes_columns="note,note2,note3",
            namespace="http://example.org/test#",
            scheme_id="test_scheme",
            scheme_name="Schéma de Test",
            scheme_definition="Définition du schéma de test",
            concept_main_name="Concept Principal",
            concept_main_definition="Définition du concept principal",
            output_file_name=self.output_file_path,
        )
        self.assertTrue(os.path.exists(self.full_output_file))

    def test_make_skos_output_file_creation(self):
        """Teste si le fichier de sortie SKOS est bien créé."""
        self.full_output_file = make_skos(
            csv_path=self.csv_path,
            csv_separateur=',',
            imbrique=False,
            skos_prefLabel_columns=["label"],
            skos_definition_columns=["definition"],
            skos_notes_columns=["note"],
            namespace="http://example.org/test#",
            scheme_id=str(uuid.uuid4()),
            scheme_name="Schéma de Test",
            scheme_definition="Un schéma de concept de test",
            concept_main_name="Concept Principal",
            concept_main_definition="Définition du concept principal",
            output_file_name=self.output_file_path,
        )
        self.assertTrue(os.path.exists(self.full_output_file))

    def test_make_skos_valid_rdf(self):
        """Teste si le fichier de sortie SKOS est un fichier RDF valide."""
        self.full_output_file = make_skos(
            csv_path=self.csv_path,
            csv_separateur=',',
            imbrique=False,
            skos_prefLabel_columns=["label"],
            skos_definition_columns=["definition"],
            skos_notes_columns=["note"],
            namespace="http://example.org/test#",
            scheme_id=str(uuid.uuid4()),
            scheme_name="Schéma de Test",
            scheme_definition="Un schéma de concept de test",
            concept_main_name="Concept Principal",
            concept_main_definition="Définition du concept principal",
            output_file_name=self.output_file_path,
        )
        g = Graph()
        g.parse(self.full_output_file, format="xml")
        self.assertGreater(len(g), 0, "Le graphe RDF doit contenir des triplets.")

    def test_make_skos_concepts(self):
        """Teste si les concepts SKOS sont correctement créés dans le fichier RDF de sortie."""
        self.full_output_file = make_skos(
            csv_path=self.csv_path,
            imbrique=False,
            csv_separateur=',',
            skos_prefLabel_columns=["label"],
            skos_definition_columns=["definition"],
            skos_notes_columns=["note"],
            namespace="http://example.org/test#",
            scheme_id=str(uuid.uuid4()),
            scheme_name="Schéma de Test",
            scheme_definition="Un schéma de concept de test",
            concept_main_name="Concept Principal",
            concept_main_definition="Définition du concept principal",
            output_file_name=self.output_file_path,
        )
        g = Graph()
        g.parse(self.full_output_file, format="xml")

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
        self.full_output_file = make_skos(
            csv_path=self.csv_path,
            imbrique=False,
            csv_separateur=',',
            skos_prefLabel_columns=["label"],
            skos_definition_columns=["definition"],
            skos_notes_columns=["note"],
            namespace=namespace,
            scheme_id="test_scheme",
            scheme_name="Schéma de Test",
            scheme_definition="Définition du schéma de test",
            concept_main_name="Concept Principal",
            concept_main_definition="Définition du concept principal",
            output_file_name=self.output_file_path,
        )
        g = Graph()
        g.parse(self.full_output_file, format="xml")

        uris = [str(s) for s, _, _ in g]
        for uri in uris:
            if uri.startswith("http"):
                self.assertTrue(uri.startswith(namespace), "Toutes les URI doivent utiliser l’espace de noms spécifié.")

    def test_missing_main_concept_name_when_not_imbrique(self):
       """Teste si une exception est levée lorsque 'concept_main_name' est manquant avec imbrique=False."""
       with self.assertRaises(ValueError) as context:
           make_skos(
                csv_path=self.csv_path,
                imbrique=False,
                csv_separateur=',',
                skos_prefLabel_columns=["label"],
                skos_definition_columns=["definition"],
                namespace="http://example.org/test#",
                scheme_id="test_scheme",
                scheme_name="Schéma de Test",
                scheme_definition="Définition du schéma de test",
                output_file_name=self.output_file_path,
           )
       self.assertIn(
           "Lorsque 'imbrique=False', 'concept_main_name' est obligatoire.",
           str(context.exception),
       )
    
    def test_missing_main_concept_preflabel_columns_when_imbrique(self):
        """Teste si une exception est levée lorsque 'skos_main_concept_preflabel_columns' est manquant avec imbrique=True."""
        with self.assertRaises(ValueError) as context:
            make_skos(
                csv_path=self.csv_path,
                csv_separateur=',',
                skos_prefLabel_columns=["label"],
                skos_definition_columns=["definition"],
                namespace="http://example.org/test#",
                scheme_id="test_scheme",
                scheme_name="Schéma de Test",
                scheme_definition="Définition du schéma de test",
                imbrique=True,
                skos_main_concept_preflabel_columns=[""],
                skos_main_concept_description_columns=[""],
                skos_narrow_concept_preflabel_columns=[""],
                skos_narrow_concept_description_columns=[""],
                output_file_name=self.output_file_path,
            )
        self.assertIn(
            "Lorsque 'imbrique=True', 'skos_main_concept_preflabel_columns' est obligatoire",
            str(context.exception),
        )
    
    def test_valid_params_with_imbrique_true(self):
        """Teste si la fonction fonctionne correctement avec 'imbrique=True' et des paramètres valides."""
        self.full_output_file = make_skos(
            csv_path=self.csv_path,
            csv_separateur=',',
            skos_prefLabel_columns=["label"],
            skos_definition_columns=["definition"],
            namespace="http://example.org/test#",
            scheme_id="test_scheme",
            scheme_name="Schéma de Test",
            scheme_definition="Définition du schéma de test",
            imbrique=True,
            skos_main_concept_preflabel_columns=["label"],
            skos_main_concept_description_columns=["definition"],
            skos_narrow_concept_preflabel_columns=["label2"],
            skos_narrow_concept_description_columns=["definition2"],
            output_file_name=self.output_file_path,
        )
        self.assertTrue(os.path.exists(self.full_output_file))

    def test_valid_params_with_imbrique_false(self):
        """Teste si la fonction fonctionne correctement avec 'imbrique=False' et des paramètres valides."""
        self.full_output_file = make_skos(
            csv_path=self.csv_path,
            csv_separateur=',',
            skos_prefLabel_columns=["label"],
            skos_definition_columns=["definition"],
            namespace="http://example.org/test#",
            scheme_id="test_scheme",
            scheme_name="Schéma de Test",
            scheme_definition="Définition du schéma de test",
            imbrique=False,
            concept_main_name="Concept Principal",
            concept_main_definition="Définition du concept principal",
            output_file_name=self.output_file_path,
        )
        self.assertTrue(os.path.exists(self.full_output_file))

if __name__ == "__main__":
    unittest.main()
