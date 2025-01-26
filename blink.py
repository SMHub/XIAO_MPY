from machine import Pin
import time

# Define the LED pin
led = Pin(7, Pin.OUT)  # Use the correct GPIO number instead of D10

# Blink the LED in a loop
while True:
    led.value(1)   # Turn the LED on
    time.sleep(1)  # Wait for a second
    led.value(0)   # Turn the LED off
    time.sleep(1)  # Wait for a second
