import unittest
import os
import pandas as pd
import uuid
from rdflib import Graph
from src.skos_service import make_skos

class TestMakeSkos(unittest.TestCase):

    def setUp(self):
        # Create a temporary CSV file for testing
        self.csv_path = "test_data.csv"
        self.output_file = "fichier_skos.xml"
        data = {
            "label": ["Concept 1", "Concept 2"],
            "definition": ["Definition 1", "Definition 2"]
        }
        df = pd.DataFrame(data)
        df.to_csv(self.csv_path, index=False)

    def tearDown(self):
        # Clean up by removing temporary files created during tests
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_make_skos_output_file_creation(self):
        """Test if the SKOS output file is created."""
        make_skos(
            csv_path=self.csv_path,
            skos_prefLabel_columns=["label"],
            skos_definition_columns=["definition"],
            namespace="http://example.org/test#",
            scheme_id=str(uuid.uuid4()),
            scheme_name="Test Scheme",
            scheme_definition="A test concept scheme",
            concept_main_name="Main Concept",
            concept_main_definition="Main concept definition"
        )
        self.assertTrue(os.path.exists(self.output_file))

    def test_make_skos_valid_rdf(self):
        """Test if the SKOS output file is a valid RDF file."""
        make_skos(
            csv_path=self.csv_path,
            skos_prefLabel_columns=["label"],
            skos_definition_columns=["definition"],
            namespace="http://example.org/test#",
            scheme_id=str(uuid.uuid4()),
            scheme_name="Test Scheme",
            scheme_definition="A test concept scheme",
            concept_main_name="Main Concept",
            concept_main_definition="Main concept definition"
        )
        # Load the generated RDF file and check for validity
        g = Graph()
        g.parse(self.output_file, format="xml")
        self.assertGreater(len(g), 0, "The RDF graph should have some triples.")

    def test_make_skos_concepts(self):
        """Test if SKOS concepts are correctly created in the RDF output."""
        make_skos(
            csv_path=self.csv_path,
            skos_prefLabel_columns=["label"],
            skos_definition_columns=["definition"],
            namespace="http://example.org/test#",
            scheme_id=str(uuid.uuid4()),
            scheme_name="Test Scheme",
            scheme_definition="A test concept scheme",
            concept_main_name="Main Concept",
            concept_main_definition="Main concept definition"
        )
        # Load the generated RDF file
        g = Graph()
        g.parse(self.output_file, format="xml")

        # Check if the main concept and narrower concepts are present
        main_concept_uri = None
        for s, p, o in g.triples((None, None, None)):
            if str(o) == "Main Concept":
                main_concept_uri = s
                break
        self.assertIsNotNone(main_concept_uri, "Main concept should be in RDF graph")

        # Check that the narrower concepts are linked to the main concept
        narrower_concepts = list(g.triples((main_concept_uri, None, None)))
        self.assertGreater(len(narrower_concepts), 0, "There should be narrower concepts linked to the main concept.")

    def test_make_skos_namespace(self):
        """Test if the SKOS concepts use the specified namespace."""
        namespace = "http://example.org/test#"
        make_skos(
            csv_path=self.csv_path,
            skos_prefLabel_columns=["label"],
            skos_definition_columns=["definition"],
            namespace=namespace,
            scheme_id="test_scheme",
            scheme_name="Test Scheme",
            scheme_definition="A test concept scheme",
            concept_main_name="Main Concept",
            concept_main_definition="Main concept definition"
        )
        # Load the generated RDF file
        g = Graph()
        g.parse(self.output_file, format="xml")

        # Check if the namespace is used in the URIs
        uris = [str(s) for s, _, _ in g]
        for uri in uris:
            if uri.startswith("http"):
                self.assertTrue(uri.startswith(namespace), "All URIs should use the specified namespace.")

if __name__ == "__main__":
    unittest.main()
