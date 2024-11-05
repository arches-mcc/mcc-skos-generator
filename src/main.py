from skos_service import make_skos  
   
if __name__ == "__main__":
    """
    Point d'entrée principal du script. Cette condition vérifie si le script 
    est exécuté directement (et non importé comme un module). Si c'est le cas,
    elle appelle la fonction make_skos() pour générer un fichier SKOS en utilisant
    les configurations et données spécifiées.
    
    Fonctionnalité:
    - Appelle la fonction make_skos() pour créer un fichier SKOS en format RDF/XML.
    """
    make_skos()    
    