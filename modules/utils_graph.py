""" Util functions related to graphs. """

from rdflib import Graph, URIRef, RDF

from globals import URI_ONTOUML, URI_ONTOLOGY
from modules.errors import report_error_io_read
from modules.utils_general import LOGGER


def load_all_graph_safely(ontology_file: str) -> Graph:
    """ Safely load graph from file to working memory.

    :param ontology_file: Path to the ontology file to be loaded into the working memory.
    :type ontology_file: str
    :return: RDFLib graph loaded as object.
    :rtype: Graph
    """

    ontology_graph = Graph()

    try:
        ontology_graph.parse(ontology_file, encoding='utf-8')
    except OSError as error:
        file_description = f"input ontology file"
        report_error_io_read(ontology_file, file_description, error)

    LOGGER.debug(f"Ontology file {ontology_file} successfully loaded to working memory.")

    return ontology_graph


def get_all_ids_for_type(ontology_graph: Graph, element_type: str) -> list[str]:
    """ Queries the graph for all elements of the given element_type and returns a list of their ids.

    :param ontology_file: Loaded ontology graph.
    :type ontology_file: Graph
    :param element_type: Type of the element (originally a JSON object) to be queried to have their ids returned .
    :type element_type: list[str]
    """

    list_of_ids_of_type = []

    # Getting the ID of all OntoUML Elements that are of element_type
    for element in ontology_graph.subjects(RDF.type, URIRef(URI_ONTOUML + element_type)):
        element = element.fragment
        list_of_ids_of_type.append(element)

    return list_of_ids_of_type
