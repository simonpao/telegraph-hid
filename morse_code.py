from adafruit_hid.keycode import Keycode as KeyCode

class MorseCode:
    DIT = 250     # Dit: 1 unit
    DAH = DIT*3   # Dah: 3 units
    CHAR = DAH    # Inter-character space (the gap between the characters of a word): 3 units
    WORD = DIT*7  # Word space (the gap between two words): 7 units

    MORSE_CODE = {
        # Letters
        ".-":    "A", "-...":  "B", "-.-.":  "C", "-..":   "D",
        ".":     "E", "..-.":  "F", "--.":   "G", "....":  "H",
        "..":    "I", ".---":  "J", "-.-":   "K", ".-..":  "L",
        "--":    "M", "-.":    "N", "---":   "O", ".--.":  "P",
        "--.-":  "Q", ".-.":   "R", "...":   "S", "-":     "T",
        "..-":   "U", "...-":  "V", ".--":   "W", "-..-":  "X",
        "-.--":  "Y", "--..":  "Z",

        # Numbers
        "-----": "0", ".----": "1", "..---": "2", "...--": "3",
        "....-": "4", ".....": "5", "-....": "6", "--...": "7",
        "---..": "8", "----.": "9",

        # Common punctuation
        "......": ".",    # Including the incorrect period encoding for compatability
        ".-.-.-": ".", "--..--": ",", "..--..": "?", "-.-.--": "!",
        "-..-.": "/", ".--.-.": "@", "---...": ":",
        ".-..-.": "\"",

        # Prosigns (procedural signals)
        ".-...":  "...",   # Stand by / wait (Literally "AS")
        ".-.-.":  "\n",    # End of message (Literally "AR")
        "...-.-": "<SK>",  # End of contact (Literally "SK")
        "-...-":  "=",     # Separator (like paragraph break, literally "BT")
        "...-.":  "<ACK>", # Understood (Literally "VE")
    }

    ASCII_TO_KEYCODES = {
        # Letters
        "A": [KeyCode.SHIFT, KeyCode.A], "B": [KeyCode.SHIFT, KeyCode.B], "C": [KeyCode.SHIFT, KeyCode.C], "D": [KeyCode.SHIFT, KeyCode.D],
        "E": [KeyCode.SHIFT, KeyCode.E], "F": [KeyCode.SHIFT, KeyCode.F], "G": [KeyCode.SHIFT, KeyCode.G], "H": [KeyCode.SHIFT, KeyCode.H],
        "I": [KeyCode.SHIFT, KeyCode.I], "J": [KeyCode.SHIFT, KeyCode.J], "K": [KeyCode.SHIFT, KeyCode.K], "L": [KeyCode.SHIFT, KeyCode.L],
        "M": [KeyCode.SHIFT, KeyCode.M], "N": [KeyCode.SHIFT, KeyCode.N], "O": [KeyCode.SHIFT, KeyCode.O], "P": [KeyCode.SHIFT, KeyCode.P],
        "Q": [KeyCode.SHIFT, KeyCode.Q], "R": [KeyCode.SHIFT, KeyCode.R], "S": [KeyCode.SHIFT, KeyCode.S], "T": [KeyCode.SHIFT, KeyCode.T],
        "U": [KeyCode.SHIFT, KeyCode.U], "V": [KeyCode.SHIFT, KeyCode.V], "W": [KeyCode.SHIFT, KeyCode.W], "X": [KeyCode.SHIFT, KeyCode.X],
        "Y": [KeyCode.SHIFT, KeyCode.Y], "Z": [KeyCode.SHIFT, KeyCode.Z],

        # Numbers
        "0": [KeyCode.ZERO],  "1": [KeyCode.ONE],  "2": [KeyCode.TWO], "3": [KeyCode.THREE],
        "4": [KeyCode.FOUR],  "5": [KeyCode.FIVE], "6": [KeyCode.SIX], "7": [KeyCode.SEVEN],
        "8": [KeyCode.EIGHT], "9": [KeyCode.NINE],

        # Common punctuation
        ".": [KeyCode.PERIOD],                    ",":  [KeyCode.COMMA],                    "?": [KeyCode.SHIFT, KeyCode.FORWARD_SLASH], 
        "!": [KeyCode.SHIFT, KeyCode.ONE],        "-":  [KeyCode.MINUS],                    "/": [KeyCode.FORWARD_SLASH], 
        "@": [KeyCode.SHIFT, KeyCode.TWO],        ":":  [KeyCode.SHIFT, KeyCode.SEMICOLON], "+": [KeyCode.SHIFT, KeyCode.EQUALS], 
        "=": [KeyCode.EQUALS],                    "\"": [KeyCode.SHIFT, KeyCode.QUOTE],

        # Prosigns (procedural signals)
        "...": [KeyCode.PERIOD, KeyCode.PERIOD, KeyCode.PERIOD],
        "\n":  [KeyCode.ENTER],
        "<SK>": [KeyCode.SHIFT, KeyCode.COMMA, KeyCode.S, KeyCode.K, KeyCode.PERIOD],
        "<ACK>": [KeyCode.SHIFT, KeyCode.COMMA, KeyCode.A, KeyCode.C, KeyCode.K, KeyCode.PERIOD]
    }

    @staticmethod
    def get_ascii(morse_code):
        return MorseCode.MORSE_CODE.get(morse_code, "?")
    
    @staticmethod
    def get_keycode(morse_code):
        ascii_char = MorseCode.get_ascii(morse_code)
        return MorseCode.ASCII_TO_KEYCODES.get(ascii_char, [KeyCode.SHIFT, KeyCode.FORWARD_SLASH])