import board
import digitalio
import storage
import usb_cdc

print("Initializing GPIO 4 to check write protect")
write_pin = digitalio.DigitalInOut(board.GP4)
write_pin.direction = digitalio.Direction.INPUT
write_pin.pull = digitalio.Pull.UP

# If write pin is connected to ground on start-up, do not show the drive on USB
if not write_pin.value:
    print("Disabling USB drive (write protect enabled)")
    storage.disable_usb_drive()
    #usb_cdc.disable(console=True, data=False)