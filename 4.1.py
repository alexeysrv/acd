import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3

def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def bin2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac, signal)
    return signal

def adc():
    while True:
    
        for value in range(256):    
            signal = bin2dac(value)
            time.sleep(0.0007)
            voltage = value / levels * maxVoltage
            comparatorValue = GPIO.input(4)
            if comparatorValue == 0:
                print("Digital value = {:^3}, analog votage = {:.2f}".format(value, voltage))
                break

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(17, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(4, GPIO.IN)

try:
    
    adc()
      
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print("GPIO cleanup completed")