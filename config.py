from jinja2 import Environment, select_autoescape, FileSystemLoader


class Config:
    # Select bw for 2d and xy for 3d models
    SPRITE_TYPE = "bw"

    # Markup
    CONTENT_POKEMON_DIR = "./content/team"
    CONTENT_POST_DIR = "./content/posts"

    # Directory to download sprites in
    SPRITE_DIR = "./static/sprites"
    SHINY_SPRITE_DIR = "./static/shiny_sprites"
    TEMPLATE_DIR = "./static/templates"
    CSS_DIR = "./static/stylesheets"
    SCRIPTS_DIR = "./static/scripts"

    # Jinja environment variable
    JINJA_ENV = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=False
    )
    
    # Build
    BUILD_DIR = "./build"
    B_SPRITE_DIR = f"{BUILD_DIR}/static/sprites"
    B_SHINY_SPRITE_DIR = f"{BUILD_DIR}/static/shiny_sprites"

