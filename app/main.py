from components.database.requests import RequestsToDatabase
from components.config import (
    DATABASE_STANDARD_TYPE,
    DATABASE_STANDARD_HOST_NAME,
)
from sqlalchemy import Column, Integer

"""
name_bot = ""


def set_name_bot(name: str):
    global name_bot
    name_bot = name


func_dict_map = {
    "name": set_name_bot
}


start_args = argv
for arg_id in range(1, len(start_args), 2):
    if start_args[arg_id][:1] != "-":

        continue

    format_arg = start_args[arg_id][1:]
    arg_value = start_args[arg_id+1]
    func_dict_map[format_arg](arg_value)


if not name_bot:
    print("[X] Internal Error: name is not set")
    exit()

bman = BotManager()
bman.init_bot(name_bot=name_bot)
"""

if __name__ == "__main__":
    database = RequestsToDatabase(type_database="mysql", host_name="ns35.link-host.net")

    columns = [
        Column("test", Integer)
    ]
    database.create_table("PendingUsers", columns)

    database.users_get_id("PendingUsers")
