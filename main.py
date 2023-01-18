"""
 * Escribe un programa que sea capaz de generar contraseñas de forma aleatoria.
 * Podrás configurar generar contraseñas con los siguientes parámetros:
 * - Longitud: Entre 8 y 16.
 * - Con o sin letras mayúsculas.
 * - Con o sin números.
 * - Con o sin símbolos.
 * (Pudiendo combinar todos estos parámetros entre ellos)
"""

import random
import configparser

# Read configuration from config file and initialize 2 dictionaries
def load_configuration():
    # Read configuration file with 'configparser' library
    config_file = configparser.RawConfigParser()
    config_file.read("config.ini")

    # Initialize dictionary with password generator config values
    config = {
        "pw_lenght": config_file.getint("GLOBAL", "pw_lenght"),
        "uppercase": config_file.getboolean("GLOBAL", "uppercase"),
        "numbers": config_file.getboolean("GLOBAL", "numbers"),
        "symbols": config_file.getboolean("GLOBAL", "symbols")
    }

    # Initialize dictionary containing different type of characters that will be used to generate passwords
    # Letters, numbers and symbols
    generators = {
        "lowercase_alphabet": config_file["GENERATORS"]["lowercase_alphabet"],
        "uppercase_alphabet": config_file["GENERATORS"]["uppercase_alphabet"],
        "numbers": config_file["GENERATORS"]["numbers"], 
        "symbols": config_file["GENERATORS"]["symbols"]
    }

    return config, generators

# Mixes lowercase and uppercase letters randomly
def get_mixed_list(lower_letters, upper_letters):
    lower_letters_length = len(lower_letters)

    mixed_list = list(lower_letters)
    for letter in upper_letters:
        pos = random.randint(0, lower_letters_length)
        mixed_list.insert(pos, letter)

    return mixed_list


# Get a list containing letters that will be used to generate the password
# They can be lowercase or both (lowercase and uppercase) 
def get_alphabet(uppercase, lowercase_alphabet, uppercase_alphabet):
    if uppercase:
        return get_mixed_list(lowercase_alphabet, uppercase_alphabet)
    return list(lowercase_alphabet)

# Get a random element from the given list
def get_next_char(lst):
    return random.choice(lst)

# Converts generators (strings) into lists. Those generators were initialized in 'load_configuration' function
# For example:
# "abcdefghijklmnopqrstuvwxyz" --> [a, b, c, d, e, ...]
def initialize_lists(config, generators):
    alphabet = get_alphabet(
        config["uppercase"], 
        generators["lowercase_alphabet"], 
        generators["uppercase_alphabet"]
    )
    numbers = None
    symbols = None
    # 'options' list can have 3 values maximum:
    #   'A' represents "Alphabet"
    #   'N' represents "Numbers"
    #   'S' represents "Symbols"
    # It says which generators lists will be used to generate the password
    options = ['A']
    if config["numbers"]:
        numbers = list(generators["numbers"])
        options.append('N')
    if config["symbols"]:
        symbols = list(generators["symbols"])
        options.append('S')

    return alphabet, numbers, symbols, options

def main():
    config, generators = load_configuration()
    alphabet, numbers, symbols, options = initialize_lists(config, generators)

    # Password generator
    gen_password = ""
    for _ in range(config["pw_lenght"]):
        # Choose ramdonly next character type 
        next_char_option = random.choice(options)
        
        # Appends next char to the password
        if next_char_option == 'A':
            gen_password += get_next_char(alphabet)
        elif next_char_option == 'N':
            gen_password += get_next_char(numbers)
        else:
            gen_password += get_next_char(symbols)

    print(f"Generated password is:\t{gen_password}")

if __name__ == "__main__":
    main()