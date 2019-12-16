from jinja2 import Environment, select_autoescape, FileSystemLoader


class Config:
    # select bw for 2d and xy for 3d models
    SPRITE_TYPE = "bw"

    # Markup
    CONTENT_POKEMON_DIR = "./content/team"
    CONTENT_POST_DIR = "./content/posts"

    # directory to download sprites in
    SPRITE_DIR = "./static/sprites"
    TEMPLATE_DIR = "./static/templates"
    CSS_DIR = "./static/stylesheets"
    BUILD_DIR = "./build"
    JINJA_ENV = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["html", "xml"]),
    )
