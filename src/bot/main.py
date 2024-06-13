from components.log._saving_logs import _del_archives

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
    _del_archives("2024-06-12")