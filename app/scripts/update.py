from importlib import import_module
from importlib.metadata import packages_distributions
from os import system, chdir
from sys import prefix


path_to_reg = "data\\sys\\req.txt"
path_to_reg_temp = "data\\sys\\req_temp.txt"
req = ""
env_name = "env"

print("""[$] UPDATE MANAGER VER 0.1.0
[$] Checking env python...
[$] Status: starting...""")

if "env" != prefix.split("\\")[-1]:

    print(f"""[!] Program couldn't found environment:\n
[$] Create env ?""")

    response = input("[?] answer [y/n] > ")

    if response != "y":
        print("[$] Stopping update manager...")
        exit(1)

    print("""[$] Creating env
[$] Status: starting...""")
    chdir("..")
    system(f"python -m venv {env_name}")

    print("""[$] Status: complete!
[!] Restarting...
[$] Stopping update manager...""")
    exit(3)


print("""[$] Status: complete!
[$] Scanning requirements
[$] Status: starting...""")


with open(path_to_reg, "r") as file:
    for lib_name_ver in file.read().split("\n"):
        c = 0
        l_n_v = lib_name_ver.split("==")
        try:
            p_d = packages_distributions()
            import_name = ""
            for lkey in p_d.keys():
                # print(p_d[lkey][0], lkey, l_n_v[0])
                if p_d[lkey][0] == l_n_v[0]:
                    import_name = lkey
                
            if not import_name:
                raise ImportError
            
            import_module(import_name)
        except ImportError:
            print(l_n_v[0])
            req += f"{lib_name_ver}\n"

print("[$] Status: complete!")
if not req:
    print("[$] All ok!")
    print("[$] Stopping update manager...")
    exit(0)


print(f"""[!] Program couldn't found these modules or modules was broken:\n
{req}
[$] Install needed modules ?""")

response = input("[?] answer [y/n] > ")

if response != "y":
    print("[$] Stopping update manager...")
    exit(1)

print("""[$] Installing requirements
[$] Status: starting...""")
with open(path_to_reg_temp, "w") as file:
    file.write(req)

system(f"pip install -r {path_to_reg_temp}")
print("""[$] Status: complete!
[!] Restarting...
[$] Stopping update manager...""")

exit(2)
