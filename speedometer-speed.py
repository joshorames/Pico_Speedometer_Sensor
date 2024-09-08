from machine import Pin, Timer
import time

tire_diameter = 0.0001460222 # 235mm to miles

# Define the GPIO pin for the sensor
SENSOR_PIN = 15

# Initialize the pin
sensor = Pin(SENSOR_PIN, Pin.IN, Pin.PULL_UP)

# Variables for counting pulses
pulse_count = 0
last_pulse_time = time.ticks_ms()

# Pulse counting function
def pulse_handler(pin):
    global pulse_count
    pulse_count += 1

# Setup an interrupt for the sensor pin
sensor.irq(trigger=Pin.IRQ_FALLING, handler=pulse_handler)

def calculate_mph(pulse_frequency, pulses_per_revolution, wheel_circumference_miles):
    # Calculate revolutions per second
    revolutions_per_second = pulse_frequency / pulses_per_revolution
    
    # Calculate revolutions per hour
    revolutions_per_hour = revolutions_per_second * 3600
    
    # Calculate speed in miles per hour
    speed_mph = revolutions_per_hour * wheel_circumference_miles
    
    return speed_mph

# Function to calculate and print speed
def calculate_speed():
    global pulse_count
    global last_pulse_time
    current_time = time.ticks_ms()
    elapsed_time = time.ticks_diff(current_time, last_pulse_time)
    
    if elapsed_time > 1000:  # Update speed every second
        speed = (pulse_count / (elapsed_time / 1000)) * 60  # Speed in pulses per minute
        pulses_per_second = speed/60
        speed_mph = calculate_mph(pulses_per_second, 16, tire_diameter)
        print(f"Speed: {speed_mph:.2f} MPH")
        pulse_count = 0
        last_pulse_time = current_time

# Timer to call calculate_speed every second
def timer_callback(timer):
    calculate_speed()

# Initialize the timer to call the callback function every 1000ms (1 second)
timer = Timer()
timer.init(period=1000, mode=Timer.PERIODIC, callback=timer_callback)

# Main loop
while True:
    time.sleep(0.1)  # Sleep to reduce CPU usage