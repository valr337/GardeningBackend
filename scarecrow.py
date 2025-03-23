from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
import time

# Servo Setup (GPIO18 = Pin 12)
factory = PiGPIOFactory()
servo = Servo(18, pin_factory=factory, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

# Ultrasonic Sensor Pins
TRIG = 23  # GPIO23 (Pin 16)
ECHO = 24  # GPIO24 (Pin 18)

# Setup GPIO mode and pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Function to measure distance
def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    timeout_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start - timeout_start > 0.02:
            return None

    timeout_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end - timeout_start > 0.02:
            return None

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

# Function to flap servo
def flap_servo():
    print("Bird detected! Flapping servo.")
    for _ in range(3):
        servo.min()
        time.sleep(0.3)
        servo.max()
        time.sleep(0.3)
    servo.mid()

# Main loop
print("Bird Detection System is running...")

try:
    while True:
        distance = measure_distance()
        if distance is not None:
            print("Distance:", distance, "cm")
            if distance < 10:
                flap_servo()
        else:
            print("No echo or timeout")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("System stopped.")
    GPIO.cleanup()
