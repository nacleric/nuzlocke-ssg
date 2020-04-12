from jinja2 import Environment, select_autoescape, FileSystemLoader


class Config:
    # Select bw for 2d and xy for 3d models
    SPRITE_TYPE = "xy"

    # Markup
    CONTENT_POKEMON_DIR = "./content/team"
    CONTENT_POST_DIR = "./content/posts"

    # Directory to download sprites in
    SPRITE_DIR = "./static/sprites"
    SHINY_SPRITE_DIR = "./static/shiny_sprites"
    TEMPLATE_DIR = "./static/templates"
    CSS_DIR = "./static/stylesheets"

    # Jinja environment variable
    JINJA_ENV = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        #autoescape=select_autoescape(["html", "xml"]),
        autoescape=False
    )
    
    # Build
    BUILD_DIR = "./build"
    B_SPRITE_DIR = f"{BUILD_DIR}/static/sprites"
    B_SHINY_SPRITE_DIR = f"{BUILD_DIR}/static/shiny_sprites"

