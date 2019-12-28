import argparse
import os
from typing import List, Dict

from config import Config
import sprite_dl


config = Config()


def token_pokemon_list(data: List) -> List:
    pkmn_list = []
    for i in data:
        pkmn = sprite_dl.PokemonData(
            i["pokemon"], i["nickname"], i["shiny"], i["description"]
        )
        pkmn_list.append(pkmn)

    return pkmn_list


def build(c: Config) -> None:
    # links = {}
    generate_pokemon_list(c)
    generate_home(c)
    generate_posts(c)


def add_link_to_dict() -> Dict:
    pass


def generate_pokemon_list(c: Config) -> None:
    data = sprite_dl.open_file(c)
    pkmn_list = token_pokemon_list(data)

    template = c.JINJA_ENV.get_template("pkmn_list.html")
    output = template.render(pokemons=pkmn_list)
    print(output)

    # Creates File and writes list of pokemon to it
    rendered_file = "pokemon_list.html"
    with open(f"{c.BUILD_DIR}/{rendered_file}", "w") as f:
        print("Writing to build folder...")
        f.write(output)


def generate_home(c: Config) -> None:
    """ Home page for the static site. Contains Active team and links """
    template = c.JINJA_ENV.get_template("home.html")
    output = template.render()
    print(output)

    # Creates File and writes list of pokemon to it
    rendered_file = "index.html"
    with open(f"{c.BUILD_DIR}/{rendered_file}", "w") as f:
        print("Writing to build folder...")
        f.write(output)


def generate_posts(c: Config) -> None:
    """ Parses markdown files and writes to file """
    post_folder = os.listdir(c.CONTENT_POST_DIR)
    for file in post_folder:
        # Reads md file
        with open(f"{c.CONTENT_POST_DIR}/{file}", "r") as f:
            content = f.read()
        content_template = c.JINJA_ENV.get_template("content.html")
        output = content_template.render(content=content)

        with open(f"{c.BUILD_DIR}/{file[:-3]}.html", "w") as f:
            print(f"Creating content for {file[:-3]}.html...")
            f.write(output)


# TODO: Needed to wipe all posts to not worry aobut overwritting
def delete_posts(c: Config) -> None:
    pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Commands")
    parser.add_argument("command", type=str, help="builds site")
    args = parser.parse_args()

    # TODO: Create a Command the creates post
    if args.command == "build":
        if os.path.isdir(config.BUILD_DIR):
            # print("Build directory exists")
            pass
        else:
            print("Build directory doesn't exist")
            os.mkdir(config.BUILD_DIR)
        sprite_dl.main(config)
        build(config)
    elif args.command == "sprites":
        sprite_dl.main(config)
    elif args.command == "delete":
        sprite_dl.delete_sprites(config)
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
