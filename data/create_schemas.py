import json
import os
from pathlib import Path
import datamodel_code_generator

# This script excepts to be run from the project root
schemas_folder = os.path.join("lol_qq_parser", "schemas")

# First, we handle the matchDetail dump
# TODO Test it with all available JSONs and make sure they all give the same format
match_detail_folder = os.path.join("data", "matchDetail")

for file_name in os.listdir(match_detail_folder):

    with open(os.path.join(match_detail_folder, file_name)) as file:
        input_dict = json.load(file)

    datamodel_code_generator.generate(
        str(input_dict),
        input_file_type=datamodel_code_generator.InputFileType.Json,
        input_filename=file_name,
        output=Path(os.path.join(schemas_folder, "match_detail.py")),
    )
