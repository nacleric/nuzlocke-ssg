import argparse
import os

from config import Config
import sprite_dl


config = Config()


def build(c: Config) -> None:
    template = c.JINJA_ENV.get_template('pkmn_list.html')
    output = template.render(name='Mary')
    print(output)

    # CREATES NEW FILE
    # basedir = os.path.dirname(c.BUILD_DIR)
    # with open('mons.html', 'w'):
    #     print("in this func")


def main() -> None:
    parser = argparse.ArgumentParser(description="Commands")
    parser.add_argument("build", type=str, help="builds site")
    args = parser.parse_args()

    if args.build != "build":
        print("not the command")
    else:
        if os.path.isdir(config.BUILD_DIR):
            print("build directory exists")
        else:
            print("build directory doesn't exist")
            os.mkdir(config.BUILD_DIR)
        build(config)


if __name__ == "__main__":
    main()