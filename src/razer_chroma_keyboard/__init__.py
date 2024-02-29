"""Copyright © 2023 Jean Oustry. Tous droits réservés."""
import time
from .api import razerServerChromaConnection

__all__ = [
    "razerServerChromaConnection"
]


def example_random_highlight():
    """Perform a simple chroma test on the keyboard, applying a random color on each key changing several times per second."""
    with razerServerChromaConnection() as connection:
        while True:
            connection.apply_rand_chroma_custom()
            time.sleep(0.3)


def main():
    """Perform a simple chroma test on the keyboard, applying a random color on each key changing several times per second."""
    try:
        example_random_highlight()
    except EnvironmentError as err: print(err, "Make sure the latest version of razer synapse is installed. https://www.razer.com/fr-fr/synapse-3")

if __name__ == "__main__":
    main()
