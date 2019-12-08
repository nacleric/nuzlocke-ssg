""" sprite_dl.py will handle downloads for the sprites asset folder """

from config import Config
import os
import requests
import json


config = Config()


# TODO: if asset not found replace with missingno
# have an option to use either bw or xy
pkmn_sprite_url = {
    "bw": "https://play.pokemonshowdown.com/sprites/gen5ani",
    "bw_shiny": "https://play.pokemonshowdown.com/sprites/gen5ani-shiny",
    "xy": "https://play.pokemonshowdown.com/sprites/ani",
    "xy_shiny": "https://play.pokemonshowdown.com/sprites/ani-shiny",
}

# maybe use this if everything else fails
# pokeapi_sprites = "https://pokeapi.co/api/v2/pokemon/ditto/"


class PokemonData:
    """ Struct that holds json data """

    def __init__(self, name: str, nickname: str, shiny: bool, description: str):
        self.name = name
        self.nickname = nickname
        self.shiny = shiny
        self.description = description


def download_sprite(p: PokemonData, c: Config) -> None:
    # doesn't support shinies yet
    dl_location = f"{c.SPRITE_DIR}/{p.name}.gif"
    request_url = f"{pkmn_sprite_url[c.SPRITE_TYPE]}/{p.name}.gif"

    r = requests.get(request_url)
    with open(dl_location, "wb") as f:
        f.write(r.content)

    # Retrieve HTTP meta-data
    print(f"status: {r.status_code}, content: {r.headers['content-type']}")


def main() -> None:
    with open("pokemon.json", "r") as file:
        data = json.load(file)

    file_list = os.listdir("./static/sprites")

    for i in data.items():
        pkmn = PokemonData(i[0], i[1]["nickname"], i[1]["shiny"], i[1]["description"])
        if i not in file_list:
            download_sprite(pkmn, config)


if __name__ == "__main__":
    main()
