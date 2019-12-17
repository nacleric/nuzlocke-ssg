import argparse
import os
from typing import List

from config import Config
import sprite_dl


config = Config()


def list_of_pokemon(data: List) -> List:
    pkmn_list = []
    for i in data:
        pkmn = sprite_dl.PokemonData(
            i["pokemon"], i["nickname"], i["shiny"], i["description"]
        )
        pkmn_list.append(pkmn)

    return pkmn_list


def build(c: Config) -> None:
    data = sprite_dl.open_file(c)
    pkmn_list = list_of_pokemon(data)

    template = c.JINJA_ENV.get_template("pkmn_list.html")
    output = template.render(pokemons=pkmn_list)
    print(output)

    # CREATES NEW FILE
    # basedir = os.path.dirname(c.BUILD_DIR)
    # with open('mons.html', 'w'):
    #     print("in this func")


def main() -> None:
    parser = argparse.ArgumentParser(description="Commands")
    parser.add_argument("command", type=str, help="builds site")
    args = parser.parse_args()

    if args.command == "build":
        if os.path.isdir(config.BUILD_DIR):
            print("build directory exists")
        else:
            print("build directory doesn't exist")
            os.mkdir(config.BUILD_DIR)
        sprite_dl.main(config)
        build(config)
    elif args.command == "sprites":
        sprite_dl.main(config)
    elif args.command == "help":
        print(
            "Commands: \n"
            "build      generates the site and downloads assets \n"
            "sprites    only downloads the sprites"
        )
    else:
        print("Wrong command. Enter 'help'")


if __name__ == "__main__":
    main()
