"""Copyright © 2023 Jean Oustry. Tous droits réservés.
"""
import random, json, threading, time, itertools, copy
import requests

HANDSHAKE_URL = "http://localhost:54235/razer/chromasdk"
REQUIREMENTS = ["core", "device", "version"]
MIN_VERSIONS = [3, 3, 3]
INITIALIZATION_INFOS = {
        "title": "Razer chroma keyboard backlight python library.",
        "description": "Library for interfacing python "\
        "with Razer Chroma SDK REST API to control the backlight of a keyboard from the brand supporting it.",
        "author": {
            "name": "J.O.",
            "contact": "https://pypi.org/search/?q=razer-chroma-keyboard"
        },
        "device_supported": ["keyboard",],
        "category": "application"
    }


class razerServerChromaConnection:
    """Keyboard lights manipulation connection. Create an instance of this object to manipulate the keyboard lights.
    """
    @staticmethod
    def checkServer() -> bool:
        """Return True if server is running, valid, with the right version. No need to check explicitly for platform.

        Returns:
            bool: The server is running with the right version.
        """
        try:
            res = json.loads(requests.get(HANDSHAKE_URL).content)
        except requests.HTTPError:
            return False
        # Vérication qu'il s'agit bien d'un serveur razer chroma, et que sa version contient ses attibuts.
        if (all([requirement in res for requirement in REQUIREMENTS])):
            # Vérification que la version est suffisamment proche
            if (all([int(res[requirement][:1]) >= mv for mv, requirement in zip(MIN_VERSIONS, REQUIREMENTS)])):
                return True
            else:
                return False
        else:
            return False

    def __init__(self, default_state: list[list[int]] = [[2**7 + 2**15 + 2**23 for _ in range(22)] for __ in range(6)]
        , initialization_infos: dict=INITIALIZATION_INFOS, sleep_multiplicator:float=1):
        """Create a Razer Chroma connection. Only one can be active at a time. Should be used with a context manager.

        Args:
            default_state (list[list[int]], optional): The default state of the lights. Defaults to [[2**7 + 2**15 + 2**23 for _ in range(22)] for __ in range(6)] which is grey.
            initialization_infos (dict, optional): The information displayed about the program using razer chroma rest api in razer synapse.
            sleep_multiplicator (float, optional): By how much will be multiplied the paused time of 0.5s for the two pauses.

        Raises:
            EnvironmentError: Raised if the Razer Chroma REST server not running or not valid.
        """
        if not type(self).checkServer(): raise EnvironmentError("Razer Chroma REST server not running or not valid.")
        time.sleep(0.5*sleep_multiplicator)
        self.uri = json.loads(requests.post(
            HANDSHAKE_URL, json=initialization_infos).content)["uri"]
        self.keep_alive_thread = threading.Thread(
            target=self._keep_alive)
        self.keep_alive_thread.start()
        self.stop_keep_alive_thread = threading.Event()
        self.default_state = default_state
        self.state = self.default_state.copy()
        self.reset_to_default_state()
        time.sleep(0.5*sleep_multiplicator)

    def _keep_alive(self):
        while True:
            time.sleep(10)
            if self.stop_keep_alive_thread.is_set(): return
            requests.put(f"{self.uri}/heartbeat")

    def _direct_put_keyboard_effect(self, effect): requests.put(self.uri + "/keyboard", json=effect)

    def _apply_chroma_custom(self, chroma_custom_matrix): self._direct_put_keyboard_effect({"effect": "CHROMA_CUSTOM", "param": chroma_custom_matrix})

    def apply_chroma_custom(self, colors_matrix: list[list[tuple[int, int, int]]]):
        """Apply a (R, G, B) colors matrix to the keyboard.

        Args:
            colors_matrix (list[list[tuple[int, int, int]]]): Color matrix made of 22 X 6 (R, G, B) tuples.
        """
        colors_matrix = copy.deepcopy(colors_matrix)
        for i in itertools.product(range(22), range(6)):
            t = colors_matrix[i[1]][i[0]]
            if any(map(lambda c: c >= 2**8, t)): raise ValueError("Each value of each tuple, representing one colour, should be between 0 and 255 included.")
            colors_matrix[i[1]][i[0]] = t[0] + t[1] * (2**8) + t[2] * (2**16)
        self._apply_chroma_custom(colors_matrix) 

    def apply_rand_chroma_custom(self): self._apply_chroma_custom([[int(random.random() * (2**24)) for _ in range(22)] for __ in range(6)])
    """Assign a different random color to the light each key of the keyboard.
    """

    def reset_to_default_state(self): self._apply_chroma_custom(self.default_state)
    """Resests the keyboard lights to the default state provided during the razerServerChromaConnection creation.
    """

    @staticmethod
    def _generate_half_luminosity_chroma_custom():
        return [[2**7 + 2**15 + 2**23 for _ in range(22)] for __ in range(6)]

    def generate_key_highlight_chroma_custom(self, column: int, row: int):
        """Sets the light of the key with the provided coordinates to red. Set all the other lights to grey.
        """
        if column >= 22 or row >= 6: raise ValueError("Coordinates out of bounds. Column should be between 0 and 21 included, and row between 0 and 5 included.")
        l = razerServerChromaConnection._generate_half_luminosity_chroma_custom()
        l[row][column] = 2**8 - 1
        self._apply_chroma_custom(l)

    def __del__(self):
        self.stop_keep_alive_thread.set()

    def __exit__(self, *_):
        self.__del__()

    def __enter__(self): return self

