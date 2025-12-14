# telegraph-hid

Circuitpython code for a Raspberry Pi Pico to act as a Human Interface Device for a telegraph transmitter.

![Telegraph HID](img/telegraph-hid.png)

Pulses on GPIO 0 will be interpreted as Morse Code according to their duration.

Morse Code uses the following terminology:
- DIT (one unit of time)
  - This is 250 milliseconds in this implementation
- DAH (three units of time)
  - Being three DITs, this is 750 milliseconds in this implementation

A dot (.) in Morse Code lasts for one DIT

A dash (-) in Morse Code lasts for one DAH

A pause of one DAH indicates a break between letters

A pause of seven DITs indicates a break between words

![Telegraph HID](img/telegraph-on-scope.png)

![Telegraph HID](img/prototype.png)

![Telegraph HID](img/rewire.png)

![Telegraph HID](img/telegraph-via-usb.png)
