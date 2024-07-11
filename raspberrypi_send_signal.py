import RPi.GPIO as GPIO
import time
import serial

pins = [3, 11, 13, 15, 16]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

for pin in pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

ser = serial.Serial('/dev/ttyGS0', 115200, timeout=1)
time.sleep(2)

previous_states = [GPIO.input(pin) for pin in pins]

try:
    while True:
        current_states = [GPIO.input(pin) for pin in pins]
        print(f"Pin {pins[0]}: {current_states[0]}, Pin {pins[1]}: {current_states[1]}, Pin {pins[2]}: {current_states[2]}, Pin {pins[3]}: {current_states[3]}, Pin {pins[4]}: {current_states[4]}")

        if current_states != previous_states:
            previous_states = current_states

            if all(state == 1 for state in current_states) or current_states == [1, 1, 0, 1, 0] or current_states == [1, 1, 0, 0, 1]:
                ser.write(b'1\n')
                print('Data sent: 1')
                time.sleep(3)
                previous_states = [GPIO.input(pin) for pin in pins]

        time.sleep(0.3)
except KeyboardInterrupt:
    print("\nCleaning up!")
    GPIO.cleanup()
    ser.close()
