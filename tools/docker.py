import yaml
from os import environ

c = yaml.load(open("../config.yml", "r"), Loader=yaml.Loader)


def main():
    yaml.dump(c["docker"], open("../build/docker-compose.yml", "w"), yaml.Dumper)


if __name__ == "__main__":
    main()
