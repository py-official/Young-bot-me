# pip lib
import yaml


def load_yaml_file(file_path: str, encoding: str | None = None) -> dict:  # function for loading data from yaml files
    # opening the yaml file at the specified path and loading data from it

    if encoding is not None:
        with open(file_path, "r", encoding=encoding) as yaml_file:
            data = yaml.safe_load(yaml_file)

    elif encoding is None:
        with open(file_path, "r", encoding="utf-8") as yaml_file:
            data = yaml.safe_load(yaml_file)

    return data


# function to dump data into yaml file
def dump_yaml_file(file_path: str, data: dict) -> None:
    # opening a yaml file at the specified path and dumping data into it
    with open(file_path, "w") as yaml_file:
        yaml.dump(data, yaml_file, sort_keys=False, encoding="utf-8", allow_unicode=True)


"""
from json import dump, load

cfg = "data/json/json_conf.json"


class JsonManager():
    def __init__(self):
        self.name = ""
        self.loadCode = 0
        self.replics = {}
        self.buffer = {}
        self.load_cfg(cfg)
        self.pjson = self.buffer["pjson"]

    def __str__(self):
        return str(self.buffer)

    def load_cfg(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            self.name = path.split("/")[-1]
            try:
                self.buffer = load(f)
            except Exception as e:
                self.name = ""
                self.loadCode = 0
                print(e)
            else:
                self.loadCode = 1

    def write_cfg(self, path: str, dictionary: dict) -> None:
        with open(path, "w", encoding="utf-8") as f:
            try:
                dump(dictionary, f, indent=2)
            except Exception as e:
                print(e)

    def procedure_for_bots(self, bot_name: str) -> None:
        self.replics = self.buffer[bot_name]["replics"]

    def dload_cfg(self, short_name: str) -> None:
        self.load_cfg(path=self.pjson+short_name)

    def dwrite_cfg(self, dictionary: dict, short_name: str = None) -> None:
        self.write_cfg(path=self.pjson+(self.name if short_name is None else short_name), dictionary=dictionary)
"""
