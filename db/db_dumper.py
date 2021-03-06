""" This module contains functions for serializing the data in the program to a database.
"""

import os

from tinydb import TinyDB

def dump_model(model, target = os.getcwd() + "/db/" +  "new_organ_db"):
    """Serialize a model as a JSON file in such a way that it can be reopened at any moment for later use."""
    # Create the db for dumping
    try:
        target_db = TinyDB(target + ".json")
    except OSError as err:
            # If we encounter an error we raise it to the GUI
            raise err
    target_db.purge_tables()
    global_const = target_db.table("GlobalConstants")
    print(model.get_global_constants())
    global_const.insert(model.get_global_constants())

    global_funcs = target_db.table("GlobalFunctions")
    global_funcs.insert(model.get_global_functions())

    global_params = target_db.table("GlobalParameters")
    global_params.insert(model.get_global_param_ranges())

    systemic_organs = target_db.table("SystemicOrgans")
    for organ in model.get_organs().values():
        # Write the organ as a dict for JSON representation
        organ_representation = {}
        organ_representation['name'] = organ.get_name()
        organ_representation['variables'] = organ.get_local_ranges()
        organ_representation['functions'] = organ.get_funcs()
        systemic_organs.insert(organ_representation)
