# pip lib
from cryptography.fernet import Fernet


def _get_secret_key(path_to_file_secret_key: str):
    with open(path_to_file_secret_key, "rb") as secret_key_file:
        return secret_key_file.read()


# function for decrypting data from a file with database host names
def get_encrypted_data(path_to_file: str, path_to_file_secret_key: str):
    # obtaining the secret encryption key
    secret_key = _get_secret_key(path_to_file_secret_key)

    # getting the tool managing the fernet algorithm
    fernet = Fernet(secret_key)

    with open(path_to_file, "rb") as conf_file:
        original_conf_file_data = conf_file.read()

    # decryption of data from a file with host names
    decrypted = fernet.decrypt(original_conf_file_data)
    decrypted_data = decrypted.decode("utf-8").split("\r\n")

    host_name = ""
    decrypted_dict_data = {}

    # a loop that converts text into a dictionary
    for data in decrypted_data:
        for symbol in data:
            if ":" == symbol:
                decrypted_dict_data[host_name] = data.split(": ")[1]
                host_name = ""
                break

            host_name += symbol
            del list(data)[data.index(symbol)]

    return decrypted_dict_data
