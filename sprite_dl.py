""" sprite_dl.py will handle downloads for the sprites asset folder """
import os
import requests
import json
from typing import Dict

from config import Config


config = Config()


# TODO: if asset not found replace with missingno
# have an option to use either bw or xy
pkmn_sprite_url = {
    "bw": "https://play.pokemonshowdown.com/sprites/gen5ani",
    "bw_shiny": "https://play.pokemonshowdown.com/sprites/gen5ani-shiny",
    "xy": "https://play.pokemonshowdown.com/sprites/ani",
    "xy_shiny": "https://play.pokemonshowdown.com/sprites/ani-shiny",
}


class PokemonData:
    """ Struct that holds json data """

    def __init__(self, name: str, nickname: str, shiny: bool, description: str):
        self.name = name
        self.nickname = nickname
        self.shiny = shiny
        self.description = description


# class MetaData:
#     def __init__(self, total_pkmn):
#         self.total_pkmn = total_pkmn

# def open_file() -> int:
#     with open(f"{c.CONTENT_POKEMON_DIR}/pokemon.json", "r") as file:
#         data = json.load(file)

#     total_pkmn = len(data.items())

#     return total_pkmn


def open_file(c: Config) -> Dict:
    with open(f"{c.CONTENT_POKEMON_DIR}/pokemon.json", "r") as file:
        data = json.load(file)

    return data


def download_sprite(p: PokemonData, c: Config) -> None:
    dl_location = f"{c.SPRITE_DIR}/{p.name}.gif"
    if p.shiny is False:
        request_url = f"{pkmn_sprite_url[c.SPRITE_TYPE]}/{p.name}.gif"
    else:
        shiny = c.SPRITE_TYPE + "_shiny"
        request_url = f"{pkmn_sprite_url[shiny]}/{p.name}.gif"

    r = requests.get(request_url)
    # Retrieve HTTP meta-data
    print(f"Status: {r.status_code}, Content: {r.headers['content-type']}")

    if r.status_code != 404:
        # Downloads the sprite if page is found
        with open(dl_location, "wb") as f:
            f.write(r.content)
    else:
        print(f"ERROR: {p.name.upper()} might be spelled incorrectly")


def main(c: Config) -> None:
    data = open_file(c)

    file_list = os.listdir(c.SPRITE_DIR)

    for i in data.items():
        pkmn = PokemonData(i[0], i[1]["nickname"], i[1]["shiny"], i[1]["description"],)
        if i not in file_list:
            download_sprite(pkmn, config)


if __name__ == "__main__":
    main(config)
