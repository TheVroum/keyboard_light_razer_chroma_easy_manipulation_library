"""Copyright © 2023 Jean Oustry. Tous droits réservés.
"""
import time
from .api import razerServerChromaConnection

__all__ = [
    razerServerChromaConnection
]


def example_random_highlight():
    with razerServerChromaConnection() as connection:
        while True:
            connection.apply_rand_chroma_custom()
            time.sleep(0.3)


def main():
    try:
        example_random_highlight()
    except EnvironmentError as err: print(err, "Make sure the latest version of razer synapse is installed. https://www.razer.com/fr-fr/synapse-3")

if __name__ == "__main__":
    main()
