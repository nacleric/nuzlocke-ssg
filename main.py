from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, NamedTuple
import argparse
import json
import os

from config import Config
import sprite_dl


config = Config()


def build(config=config) -> None:
    if config.ONLY_BLOG is False:
        generate_pokemon_list()
    generate_index()
    generate_posts()
    generate_styles()
    generate_scripts()


def generate_pokemon_list(config=config) -> None:
    """ Populates pokemon_list.html """
    template = config.JINJA_ENV.get_template("pokemon_list.html")

    with open(f"{config.CONTENT_POKEMON_DIR}/pokemon.json", "r") as file:
        print("[LOG] Tokenizing pokemon_list.json")
        json_data = json.load(file)

        pokemon_list = []
        for i in json_data:
            if i["shiny"] == True:
                asset_location = f"{config.SHINY_SPRITE_DIR}/{i['pokemon']}.gif"
            else:
                asset_location = f"{config.SPRITE_DIR}/{i['pokemon']}.gif"
            pokemon = sprite_dl.PokemonData(
                i["pokemon"],
                i["nickname"],
                i["shiny"],
                i["description"],
                asset_location,
            )
            pokemon_list.append(pokemon)
            sprite_dl.download_sprite(pokemon)
        output = template.render(pokemons=pokemon_list)

    # Creates File and writes list of pokemon to it
    rendered_file = "pokemon_list.html"
    with open(f"{config.BUILD_DIR}/{rendered_file}", "w") as f:
        print("[LOG] Writing to build folder...")
        f.write(output)


def generate_index(config=config) -> None:
    """ Index page for the static site """
    template = config.JINJA_ENV.get_template("index.html")

    # Grabbing meta-data of active_team.json to insert into index template
    with open(f"{config.CONTENT_POKEMON_DIR}/active_team.json", "r") as f:
        print("[LOG] Tokenizing active_team.json")
        json_data = json.load(f)

        active_team = []
        for i in json_data:
            if i["shiny"] == True:
                asset_location = f"{config.SHINY_SPRITE_DIR}/{i['pokemon']}.gif"
            else:
                asset_location = f"{config.SPRITE_DIR}/{i['pokemon']}.gif"
            pokemon = sprite_dl.PokemonData(
                i["pokemon"],
                i["nickname"],
                i["shiny"],
                i["description"],
                asset_location,
            )
            active_team.append(pokemon)
            sprite_dl.download_sprite(pokemon)
        output = template.render(pokemons=active_team)

    # Creates File and writes list of pokemon to it
    rendered_file = "index.html"
    with open(f"{config.BUILD_DIR}/{rendered_file}", "w") as f:
        print("[LOG] Generated index.html...")
        f.write(output)


def generate_posts(config=config) -> None:
    """ Generates the posts.html file (contains list of blogposts and sorts them)
        Also parses markdown files in ./content and writes to file in ./build
    """

    delete_posts()  # Clears build folder

    HTML_FILE = "posts.html"

    class PostToken(NamedTuple):
        title: str
        date: str
        intro: str
        filename: str
        file_location: str

    # Renders the template that redirects to all the posts
    template = config.JINJA_ENV.get_template(HTML_FILE)

    post_token_list = []
    post_folder = os.listdir(config.CONTENT_POST_DIR)
    for file in post_folder:
        # Reads md file from content folder
        with open(f"{config.CONTENT_POST_DIR}/{file}", "r") as f:
            content = f.read()
            content_template = config.JINJA_ENV.get_template("content.html")
            output = content_template.render(content=content)

        # Copies to build directory
        B_post_location = f"{config.BUILD_DIR}/posts/{file}"
        with open(B_post_location, "w") as f:
            print(f"[LOG] Creating content for {file}...")
            f.write(output)

        soup = BeautifulSoup(content, "html.parser")
        soup_title = soup.find("div", class_="title").get_text()
        soup_date = soup.find("div", class_="date").get_text()
        soup_intro = soup.find("div", class_="intro").get_text()
        post_token = PostToken(
            title=soup_title,
            date=soup_date,
            intro=soup_intro,
            filename=file,
            file_location=f"/posts/{file}",
        )
        post_token_list.append(post_token)
        post_token_list.sort(key=lambda x: x.date, reverse=True)

    rendered_posts_html = template.render(posts=post_token_list)
    with open(f"{config.BUILD_DIR}/{HTML_FILE}", "w") as f:
        print(f"[LOG] Generated {HTML_FILE}...")
        f.write(rendered_posts_html)


# TODO: fix this; only works with 1 stylesheet
def generate_styles(config=config) -> None:
    """ Parses stylesheets in ./static and writes to ./build/stylesheets """
    stylesheets_folder = os.listdir(config.CSS_DIR)
    for file in stylesheets_folder:
        # Reads stylesheets from static folder
        with open(f"{config.CSS_DIR}/{file}", "r") as f:
            css_file = f.read()

        # Writes into Build folder
        with open(f"{config.BUILD_DIR}/static/stylesheets/{file}", "w") as f:
            print("[LOG] Copying stylesheets to build folder...")
            f.write(css_file)


def generate_scripts(config=config) -> None:
    """ Parses stylesheets in ./static and writes to ./build/scripts"""
    scripts_folder = os.listdir(config.SCRIPTS_DIR)
    for file in scripts_folder:
        # Reads scripts from static folder
        with open(f"{config.SCRIPTS_DIR}/{file}", "r") as f:
            script_file = f.read()

        # Writes into Build folder
        with open(f"{config.BUILD_DIR}/static/scripts/{file}", "w") as f:
            print("[LOG] Copying scripts to build folder…")
            f.write(script_file)


def new_post(config=config) -> None:
    datetime_obj = datetime.now()
    current_date = datetime_obj.strftime("%m-%d-%Y")
    with open(f"{config.CONTENT_POST_DIR}/{datetime_obj}.html", "w") as f:
        f.write(
            f"<!-- Don't channge the classes or delete these -->\n"
            f"<div class='title'>Insert title here</div>\n"
            f"<div class='date'>{current_date}</div>\n"
            f"<div class='intro'>Insert intro here</div>\n"
        )


def delete_posts(config=config) -> None:
    B_post_folder = os.listdir(f"{config.BUILD_DIR}/posts")
    for file in B_post_folder:
        file_path = os.path.join(f"{config.BUILD_DIR}/posts", file)
        os.remove(file_path)
        print(f"[LOG] Deleting {file} from ./build/posts folder")


def main() -> None:
    parser = argparse.ArgumentParser(description="Commands")
    parser.add_argument("command", type=str, help="builds site")
    args = parser.parse_args()

    if args.command == "build":
        if os.path.isdir(config.BUILD_DIR):
            print("Build directory exists")
        else:
            print("Build directory doesn't exist")
            os.mkdir(config.BUILD_DIR)
            os.mkdir(f"{config.BUILD_DIR}/posts")
            os.mkdir(f"{config.BUILD_DIR}/static")
            os.mkdir(f"{config.BUILD_DIR}/static/stylesheets")
            os.mkdir(f"{config.BUILD_DIR}/static/scripts")
            os.mkdir(f"{config.BUILD_DIR}/static/shiny_sprites")
            os.mkdir(f"{config.BUILD_DIR}/static/sprites")
        sprite_dl.main()
        build()
    elif args.command == "newpost":
        new_post()
    elif args.command == "dl_sprites":
        sprite_dl.main()
    elif args.command == "del_sprites":
        sprite_dl.delete_sprites()
    elif args.command == "help":
        print(
            "Commands: \n"
            "build      |   generates the site and downloads assets \n"
            "dl_sprites |   only downloads the sprites\n"
            "del_sprites|   deletes sprites\n"
            "newpost    |   generates a markdown file for content"
        )
    else:
        print("Wrong command. Enter 'help'")


if __name__ == "__main__":
    main()
