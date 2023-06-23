""" Functions to decode specificities of the object Project. """
from pprint import pprint

from rdflib import Graph, URIRef

from globals import URI_ONTOLOGY, URI_ONTOUML
from modules.errors import report_error_requirement_not_met
from modules.utils_graph import get_all_ids_for_type


def get_package_contents(dictionary_data: dict, package_id: str, list_contents: list = []) -> list[dict]:
    """ Receives the dictionary with all loaded JSON data and returns the value of the 'contents' field for a given
    Package (received as an id).

    :param dictionary_data: Dictionary to have its fields decoded.
    :type dictionary_data: dict
    :param package_id: ID of the Package to have its list of contents returned.
    :type package_id: str
    :return: List of contents for a given Package.
    :rtype: list[dict]
    """

    # End of recursion
    if dictionary_data["id"] == package_id:
        if "contents" in dictionary_data:
            list_contents = dictionary_data["contents"].copy()
        else:
            list_contents = []

    # Recursively treats sub-dictionaries
    else:

        if list_contents != []:
            return list_contents

        for key in dictionary_data.keys():

            # Treat case dictionary
            if type(dictionary_data[key]) is dict:
                list_contents = get_package_contents(dictionary_data[key], package_id)

            # Treat case list
            elif type(dictionary_data[key]) is list:
                for item in dictionary_data[key]:
                    list_contents = get_package_contents(item, package_id, list_contents)
                    if list_contents != []:
                        break

    return list_contents


def set_package_containsmodelelement_property(dictionary_data: dict, ontouml_graph: Graph) -> None:
    """ Set object property ontouml:containsModelElement between a Package and its containing ModelElements.

    :param dictionary_data: Dictionary to have its fields decoded.
    :type dictionary_data: dict
    :param ontouml_graph: Knowledge graph that complies with the OntoUML Vocabulary
    :type ontouml_graph: Graph
    """

    # Get ids of all objects of type Package
    list_package_ids = get_all_ids_for_type(ontouml_graph, "Package")

    print(f"\n{list_package_ids = }")

    # For each Package (known ids):
    for package_id in list_package_ids:

        print()
        print(f"{package_id = }")

        # Get the list inside the 'contents' key
        package_id_contents_list = get_package_contents(dictionary_data, package_id)

        print(f"{package_id_contents_list = }")

        # If list is empty, do nothing
        if not package_id_contents_list:
            continue

        # Create a list of all ids inside the returned list
        list_related_ids = []
        for content in package_id_contents_list:
            list_related_ids.append(content["id"])

        # Include found related elements in graph using ontouml:containsModelElement
        for related_id in list_related_ids:
            ontouml_graph.add((URIRef(URI_ONTOLOGY + package_id),
                               URIRef(URI_ONTOUML + "containsModelElement"),
                               URIRef(URI_ONTOLOGY + related_id)))


def create_package_properties(dictionary_data: dict, ontouml_graph: Graph) -> None:
    """ Main function for decoding an object of type Package.
    It only calls other specific functions for setting the object's specific properties.

    :param dictionary_data: Dictionary to have its fields decoded.
    :type dictionary_data: dict
    :param ontouml_graph: Knowledge graph that complies with the OntoUML Vocabulary
    :type ontouml_graph: Graph
    """

    pprint(dictionary_data)

    set_package_containsmodelelement_property(dictionary_data, ontouml_graph)
