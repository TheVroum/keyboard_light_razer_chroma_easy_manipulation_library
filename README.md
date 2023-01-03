# What is this library ?

This library allows a python application or script to change the keys backlight colors of a razer chroma compatible keyboard.
A demo is also available.

# How to install ?

Install [https://www.razer.com/fr-fr/synapse-3](https://www.razer.com/fr-fr/synapse-3). <br/>
Create an environment and activate it if you want to (optionnal). <br/>
Execute ```pip install razer-chroma-keyboard```

# How to test ?

Execute ```python -m razer_chroma_keyboard```. You should see promptly (in less than 3 seconds) the result on your keyboard.

# How to use as a library ?

Import with ```import razer_chroma_keyboard```. For this example, also ```import time```.
Prepare your (R, G, B) color tuples matrix. So you know the dimensions, you can use this black matrix and modify it : ```m = [[(0, 0, 0) for _ in range(22)] for _ in range(6)]```.
Then you can use a with statement (to allow fine control of the connection) like this : <br/>
```
with razer_chroma_keyboard.razerServerChromaConnection() as connection :
    connection.apply_chroma_custom(m)
    while True: time.sleep(1)
```
The second line is because, when the with statement is left, the connection will be stopped, and the keyboard will back to it's previous state after a moment (if another software controls it).
Example of full code to turn the whole keyboard into a specific color :
```
import razer_chroma_keyboard
import time

def change_color(color: tuple[int, int, int] = (50, 50, 50)):
    m = [[color for _ in range(22)] for _ in range(6)]
    with razer_chroma_keyboard.razerServerChromaConnection() as connection :
        connection.apply_chroma_custom(m)
        while True: time.sleep(1)

change_color((255, 191, 0)) #  Amber yellow.
```