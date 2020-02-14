import os
import random
import json

from deb_parse import Parser


def parse_from(filepath):
    try:
        parse = Parser(filepath)
    except (ValueError, TypeError):
        return None

    recovery_id = str(random.randint(1000, 9999))

    datastore = os.path.join("deb_parse_web", "datastore", recovery_id)
    os.makedirs(os.path.dirname(datastore), exist_ok=True)

    parse.to_json_file(os.path.join(datastore, "pkgs_list.json"), names_only=True)
    parse.to_json_file(os.path.join(datastore, "pkgs_raw.json"), raw=True)
    parse.to_json_file(os.path.join(datastore, "pkgs_clean.json"))

    return recovery_id


def check_installed(recovery_id, pkg):
    pass
