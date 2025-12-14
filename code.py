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

print("Initializing GPIO 0")
button = digitalio.DigitalInOut(board.GP0)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

print("Initializing Keyboard")
keyboard = Keyboard(usb_hid.devices)

def ticks_ms():
    return int(monotonic_ns() / 1_000_000)

def ticks_diff(end, start):
    if end >= start:
        return end - start
    else:
        return start - end

def sleep_ms(ms):
    sleep(ms / 1000)

state = 0
start = 0
end = 0
total = 0
letter = ""
decoded = ""

print("Start keyboard loop with button initial state =", button.value )
while True:
    try:
        if state == 0 and start != 0 and end != 0 and letter != "":
            # Check if a letter should be inserted
            if ticks_diff( ticks_ms(), end ) >= MorseCode.CHAR:
                decoded = MorseCode.get_ascii(letter)
                print (decoded, end="")
                keyboard.send(*MorseCode.get_keycode(letter))
                letter = ""
        
        if state == 0 and start != 0 and end != 0:
            # Check if a space should be inserted
            if ticks_diff( ticks_ms(), end ) >= MorseCode.WORD:
                print (" ", end="")
                keyboard.send(KeyCode.SPACE)
                start = 0
                end = 0
        
        # if the button is depressed
        if button.value == False:
            if state == 0:
                start = ticks_ms()
                state = 1
            led.value = True
        
        # if the button is released
        if button.value == True:
            if state == 1:
                end = ticks_ms()
                state = 0
                total = ticks_diff( end, start )
                if total <= MorseCode.DIT:
                    letter += '.'
                    print ('.', end="")
                else:
                    letter += '-'
                    print ('-', end="")
            led.value = False
        
        sleep_ms(int(MorseCode.DIT/5))
        
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt detected.")
        break
    except Exception as e:
        print( "\nAn error occurred.", e )
        break
led.value = False
print("Finished.")
