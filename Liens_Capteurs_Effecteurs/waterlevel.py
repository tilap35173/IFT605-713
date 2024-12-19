import time
#import RPi.GPIO as GPIO
import RPiSim.GPIO as gpio #pour similation 
import paho.mqtt.client as mqtt
import traceback

# GPIO Pins
GPIO=gpio.GPIO
TRIG_PIN = 23
ECHO_PIN = 24

# MQTT Broker Configuration
MQTT_BROKER = "4232e4b4c8374524bcdcd1d81b1c34e5.s1.eu.hivemq.cloud"  # Replace with your MQTT broker address
MQTT_USERNAME= "isma1781"
MQTT_PASW="0209Ift713"
MQTT_PORT = 8883
MQTT_TOPIC = "home/waterlevel"

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def measure_distance():
    """
    Measure the distance using the ultrasonic sensor.
    Returns the distance in centimeters.
    """
    GPIO.output(TRIG_PIN, False)
    time.sleep(2)

    # Trigger the ultrasonic burst
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # Measure the time for the echo
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2  # Speed of sound = 343 m/s
    return round(distance, 2)

# MQTT Connection Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def publish_water_level(client):
    while True:
        try:
            distance = measure_distance()
            print(f"Water Level: {distance} cm")
            
            # Publish to MQTT topic
            client.publish(MQTT_TOPIC, str(distance))
            time.sleep(5)  # Publish every 5 seconds
        except KeyboardInterrupt:
            print("Stopping...")
            GPIO.cleanup()
            break

def main():
    # Initialize MQTT client
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASW)
    client.on_connect = on_connect

    try:
        client.connect(MQTT_BROKER,MQTT_PORT,100)
        client.tls_set()
        client.loop_start()  # Start the MQTT loop
        publish_water_level(client)
    except Exception as e:
        print(f"Error: {e}")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
