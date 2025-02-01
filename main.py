from machine import Pin, PWM
import time

# Motor Pins (Adjust to your wiring)
MOTOR_PIN_A = 2
MOTOR_PIN_B = 3

# Encoder Pin (Adjust to your wiring)
ENCODER_PIN = 4

# Motor Driver
motor_a = PWM(Pin(MOTOR_PIN_A))
motor_b = PWM(Pin(MOTOR_PIN_B))
motor_a.freq(1000)
motor_b.freq(1000)

# Encoder
encoder_count = 0
encoder_prev_state = 0

def encoder_interrupt(pin):
    global encoder_count, encoder_prev_state
    current_state = encoder_pin.value()
    if current_state != encoder_prev_state:
        encoder_count += 1
        encoder_prev_state = current_state

encoder_pin = Pin(ENCODER_PIN, Pin.IN, Pin.PULL_UP)
encoder_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=encoder_interrupt)

def set_motor_speed(speed):
    if speed > 0:
        motor_a.duty(int(abs(speed)))
        motor_b.duty(0)
    elif speed < 0:
        motor_a.duty(0)
        motor_b.duty(int(abs(speed)))
    else:
        motor_a.duty(0)
        motor_b.duty(0)

# Target RPM
TARGET_RPM = 200

# Function to calculate RPM based on encoder counts
def calculate_rpm():
    global encoder_count
    prev_count = encoder_count
    time.sleep_ms(100)  # Sample time (adjust if needed)
    current_count = encoder_count
    delta_counts = current_count - prev_count

    # Assuming 100 pulses per revolution (adjust if different)
    rpm = (delta_counts / 100) * (60 / 0.1)  # 0.1 is the sample time in seconds
    return rpm

# Function to find the correct duty cycle for the target RPM (crude approach)
def find_duty_cycle(target_rpm):
    # This is a very basic approach.  A proper PID controller is recommended for
    # accurate speed control.  This approach will likely require tuning.

    duty_cycle = 512  # Start with a middle value
    current_rpm = 0

    # Iterate and adjust duty_cycle until current_rpm is close to target_rpm
    for _ in range(20): #Try 20 times
        set_motor_speed(duty_cycle)
        time.sleep_ms(200) #Small delay to get a reading
        current_rpm = calculate_rpm()

        if abs(current_rpm - target_rpm) < 10: #Check if close enough
            break

        if current_rpm < target_rpm:
            duty_cycle += 50 #Increase duty cycle a bit
        else:
            duty_cycle -= 50 #Decrease duty cycle a bit

        duty_cycle = max(0, min(1023, duty_cycle))  # Keep within valid range

    return duty_cycle

# Run the motor for 2 minutes at the target RPM
run_time_seconds = 2 * 60  # 2 minutes
start_time = time.time()

duty_cycle_to_use = find_duty_cycle(TARGET_RPM)
print(f"Duty Cycle: {duty_cycle_to_use}")

set_motor_speed(duty_cycle_to_use) #Set the motor speed

while time.time() - start_time < run_time_seconds:
    current_rpm = calculate_rpm()
    print(f"Current RPM: {current_rpm}")
    time.sleep(1)  # Check and print RPM every second

set_motor_speed(0)  # Stop the motor
print("Motor stopped")
print(f"Total Encoder Count: {encoder_count}")
