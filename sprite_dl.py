""" sprite_dl.py will handle downloads for the sprites asset folder """
import os
import requests
import json
from typing import List

from config import Config


config = Config()


# TODO: if asset not found replace with missingno
pkmn_sprite_url = {
    "bw": "https://play.pokemonshowdown.com/sprites/gen5ani",
    "bw_shiny": "https://play.pokemonshowdown.com/sprites/gen5ani-shiny",
    "xy": "https://play.pokemonshowdown.com/sprites/ani",
    "xy_shiny": "https://play.pokemonshowdown.com/sprites/ani-shiny",
}


class PokemonData:
    """ Struct that holds json data """

    def __init__(self, pokemon: str, nickname: str, shiny: bool, description: str):
        self.pokemon = pokemon
        self.nickname = nickname
        self.shiny = shiny
        self.description = description


def open_file(c: Config) -> List:
    with open(f"{c.CONTENT_POKEMON_DIR}/pokemon.json", "r") as file:
        data = json.load(file)

    return data


def download_sprite(p: PokemonData, c: Config) -> None:
    """ Downloads sprites and inserts them into the proper folder """

    # Checks for shiny's and inserts the correct url
    if p.shiny is False:
        dl_location = f"{c.SPRITE_DIR}/{p.pokemon}.gif"
        notshiny = c.SPRITE_TYPE
        request_url = f"{pkmn_sprite_url[notshiny]}/{p.pokemon}.gif"
    else:
        dl_location = f"{c.SHINY_SPRITE_DIR}/{p.pokemon}.gif"
        shiny = c.SPRITE_TYPE + "_shiny"
        request_url = f"{pkmn_sprite_url[shiny]}/{p.pokemon}.gif"

    r = requests.get(request_url)

    # Retrieve HTTP meta-data
    print(
        f"-{p.pokemon}  Status: {r.status_code}, Content: {r.headers['content-type']}"
    )

    # Downloads the sprite if page is found
    if r.status_code != 404:
        with open(dl_location, "wb") as f:
            f.write(r.content)
    else:
        print(f"ERROR: {p.pokemon.upper()} might be spelled incorrectly")


def delete_sprites(c: Config) -> None:
    """ Clears sprite folders """
    shiny_folder = os.listdir(c.SHINY_SPRITE_DIR)
    sprite_folder = os.listdir(c.SPRITE_DIR)

    for file in shiny_folder:
        file_path = os.path.join(c.SHINY_SPRITE_DIR, file)
        os.remove(file_path)
        print(f"DELETING shiny {file}")
    for file in sprite_folder:
        file_path = os.path.join(c.SPRITE_DIR, file)
        os.remove(file_path)
        print(f"DELETING {file}")


def main(c: Config) -> None:
    data = open_file(c)

    delete_sprites(c)
    for i in data:
        pkmn = PokemonData(i["pokemon"], i["nickname"], i["shiny"], i["description"])
        download_sprite(pkmn, config)


if __name__ == "__main__":
    main(config)
