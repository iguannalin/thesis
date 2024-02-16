import board
import touchio
from adafruit_debouncer import Debouncer, Button

THRESHOLD = 1000
t = touchio.TouchIn(board.GP12)
t.threshold = t.raw_value + THRESHOLD
touchpad = Button(t, value_when_pressed=True)

while True:
    touchpad.update()
    if touchpad.rose:

        print("Touch On")
    if touchpad.fell:
        print("Touch Off")