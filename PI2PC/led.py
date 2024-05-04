import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

def main(status):
	if status == "on":
		GPIO.output(18, True)
	elif status == "off":
		GPIO.output(18, False)
