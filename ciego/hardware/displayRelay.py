import RPi.GPIO as GPIO
import system.system_gpio as system_gpio
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(system_gpio.RELAY, GPIO.OUT)
GPIO.output(system_gpio.RELAY, GPIO.HIGH)


def open():
     GPIO.output(system_gpio.RELAY, GPIO.LOW)
     time.sleep(0.5)


def close():
    GPIO.output(system_gpio.RELAY, GPIO.HIGH)
    time.sleep(0.5)