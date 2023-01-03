"""Copyright © 2023 Jean Oustry. Tous droits réservés.
"""
import pynput, click
import time, threading, itertools
from .api import razerServerChromaConnection

__all__ = [
    razerServerChromaConnection
]



def example_mooving_highlight():
    class Point:
        def __init__(self):
            self._col = 0
            self._row = 0
        @property
        def col(self):
            return self._col
        @col.setter
        def col(self, value):
            self._col = min(21, max(0, value))
        @property
        def row(self):
            return self._row
        @row.setter
        def row(self, value):
            self._row = min(5, max(0, value))

    actualize = threading.Event()
    actualize.set()

    coord = Point()
    actions = {pynput.keyboard.Key.left: lambda: coord.__setattr__("col", coord.__getattribute__("col") - 1)
            , pynput.keyboard.Key.up: lambda: coord.__setattr__("row", coord.__getattribute__("row") - 1)
            , pynput.keyboard.Key.right: lambda: coord.__setattr__("col", coord.__getattribute__("col") + 1)
            , pynput.keyboard.Key.down: lambda: coord.__setattr__("row", coord.__getattribute__("row") + 1)}
    callback = lambda key: [actions[key]() if key in actions else None, actualize.set()]

    pynput.keyboard.Listener(on_press=callback).start()

    with razerServerChromaConnection() as connection:
        while True:
            actualize.wait()
            actualize.clear()
            connection.generate_key_highlight_chroma_custom(coord.col, coord.row)


def example_random_highlight():
    with razerServerChromaConnection() as connection:
        while True:
            connection.apply_rand_chroma_custom()
            time.sleep(0.3)


def example_new_api():
    c = [[(0, 0, 255) if _ >= 22/2 else (0, 255, 0) for _ in range(22)] for __ in range(6)]
    for i in itertools.product(range(22), range(6)):
        if i[0] == 0 or  i[0] == 21 or  i[1] == 0 or i[1] == 5:
            c[i[1]][i[0]] = (255, 0, 0)
    with razerServerChromaConnection() as connection:
        connection.apply_chroma_custom(c)
        while True:
            time.sleep(0.3)


@click.command()
# @click.option("--example", prompt="Which example ? (1, 2, or 3)", default=2, required=True, show_default=True)
@click.option("--example", default=2, required=True, show_default=True)
def main(example):
    try:
        [example_mooving_highlight, example_random_highlight, example_new_api][example - 1]()
    except EnvironmentError as err: print(err, "Make sure the latest version of razer synapse is installed. https://www.razer.com/fr-fr/synapse-3")

if __name__ == "__main__":
    main()
