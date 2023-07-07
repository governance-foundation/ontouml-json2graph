""" Main file for ontouml-json2graph. """

import time

from modules.arguments import publish_user_arguments, ARGUMENTS
from modules.decoder.decode_main import decode_json_to_graph
from modules.input_output import safe_load_json_file, write_graph_file
from modules.logger import initialize_logger
from modules.utils_general import get_date_time


def ontouml_json2graph(json_path: str, graph_format: str, language: str = "",
                       execution_mode: str = "production") -> str:
    """ Main function for ontouml-json2graph.

    :param json_path: Path to the JSON file to be decoded provided by the user.
    :type json_path: str
    :param graph_format: Format for saving the resulting knowledge graph.
    :type graph_format: str
    :param language: Language tag to be added to the ontology's concepts.
    :type language: str
    :param execution_mode: Information about execution mode. Valid values are 'production' (default) and 'test'.
    :type execution_mode: str
    :return: Saved output file path. Used for testing.
    :rtype: str
    """

    logger = initialize_logger(execution_mode)

    if execution_mode == "production":
        # Initial time information
        time_screen_format = "%d-%m-%Y %H:%M:%S"
        start_date_time = get_date_time(time_screen_format)
        st = time.perf_counter()

        logger.info(f"OntoUML JSON2Graph decoder started on {start_date_time}!\n")

    # Load JSON
    json_data = safe_load_json_file(json_path)

    # Decode JSON into Graph
    ontouml_graph = decode_json_to_graph(json_data, language)

    if execution_mode == "production":
        # Get software's execution conclusion time
        end_date_time = get_date_time(time_screen_format)
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)

        # The sleep function is for the correct printing. The performance is not affected as it only runs in production
        time.sleep(0.1)
        print()
        logger.info(f"Decoding concluded on {end_date_time}. Total execution time: {elapsed_time} seconds.")

    # Save graph as specified format
    output_file_path = write_graph_file(ontouml_graph, json_path, graph_format)
    logger.info(f"Output graph file successfully saved at {output_file_path}.")

    return output_file_path


if __name__ == '__main__':
    # Treat arguments

    publish_user_arguments()
    print(ARGUMENTS)
    exit(3)

    # Execute
    ontouml_json2graph(json_path, graph_format, language, "production")
