import json
import yaml

# print(1716843600.0 - 1716238800.0)
# 604800.0

with open("../../data/json/bots_properties.json", "r", encoding="utf-8") as json_config_file:
    json_config_data = json.load(json_config_file)

with open("../../data/json/bots_properties.yaml", "w") as yaml_config_file:
    yaml.safe_dump(json_config_data, yaml_config_file, sort_keys=False)
