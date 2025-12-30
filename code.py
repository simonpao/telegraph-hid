import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode as KeyCode
from time import monotonic_ns, sleep
from morse_code import MorseCode

print("Initializing LED")
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

print("Initializing Light")
light = digitalio.DigitalInOut(board.GP3)
light.direction = digitalio.Direction.OUTPUT

print("Initializing GPIO 0")
button = digitalio.DigitalInOut(board.GP0)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

print("Initializing GPIO 1")
button2 = digitalio.DigitalInOut(board.GP1)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP

print("Initializing GPIO 2")
button3 = digitalio.DigitalInOut(board.GP2)
button3.direction = digitalio.Direction.INPUT
button3.pull = digitalio.Pull.UP

print("Initializing Keyboard")
keyboard = Keyboard(usb_hid.devices)

state = 0
start = 0
end = 0
total = 0
letter = ""
decoded = ""
mode = MorseCode.UPPER

def ticks_ms():
    return int(monotonic_ns() / 1_000_000)

def ticks_diff(end, start):
    if end >= start:
        return end - start
    else:
        return start - end

def sleep_ms(ms):
    sleep(ms / 1000)

def morse_to_ascii(case, gpio_button):
    global state, start, end, total, letter, led, light, keyboard, decoded

    if state == 0 and start != 0 and end != 0 and letter != "":
        # Check if a letter should be inserted
        if ticks_diff( ticks_ms(), end ) >= MorseCode.CHAR:
            if case == MorseCode.MORSE:
                print(" ", end="")
                keyboard.send(KeyCode.SPACE)
            else:
                decoded = MorseCode.get_ascii(letter, case)
                print (decoded, end="")
                keyboard.send(*MorseCode.get_keycode(letter, case))
            letter = ""

    if state == 0 and start != 0 and end != 0:
        # Check if a space should be inserted
        if ticks_diff( ticks_ms(), end ) >= MorseCode.WORD:
            if case == MorseCode.MORSE:
                print ("/ ", end="")
                keyboard.send(*[KeyCode.FORWARD_SLASH, KeyCode.SPACE])
            else:
                print (" ", end="")
                keyboard.send(KeyCode.SPACE)
            start = 0
            end = 0
    
    # if the button is depressed
    if gpio_button.value == False:
        if state == 0:
            start = ticks_ms()
            state = 1
            led.value = True
            light.value = True
    
    # if the button is released
    if gpio_button.value == True:
        if state == 1:
            end = ticks_ms()
            state = 0
            total = ticks_diff( end, start )
            if total <= MorseCode.DIT:
                print ('.', end="")
                if case == MorseCode.MORSE:
                    keyboard.send(KeyCode.PERIOD)
                letter += '.'
            else:
                print ('-', end="")
                if case == MorseCode.MORSE:
                    keyboard.send(KeyCode.MINUS)
                letter += '-'
            led.value = False
            light.value = False

print("Start keyboard loop with button initial state =", button.value, button2.value, button3.value )
while True:
    try:
        #print("keyboard loop with button state =", button.value, button2.value, button3.value )
        if button.value == False:
            mode = MorseCode.UPPER
        elif button2.value == False:
            mode = MorseCode.LOWER
        elif button3.value == False:
            mode = MorseCode.MORSE
        
        if mode == MorseCode.UPPER:
            morse_to_ascii(MorseCode.UPPER, button)
        if mode == MorseCode.LOWER:
            morse_to_ascii(MorseCode.LOWER, button2)
        if mode == MorseCode.MORSE:
            morse_to_ascii(MorseCode.MORSE, button3)
        
        sleep_ms(int(MorseCode.DIT/5))
        
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt detected.")
        break
    except Exception as e:
        print( "\nAn error occurred.", e )
        break
led.value = False
print("Finished.")
