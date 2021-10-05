import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(17, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(4, GPIO.IN)

def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def bin2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac, signal)
    return signal


def adc():
        value = 128
        for i in range(6, 0, -1):
            signal = bin2dac(value)
            time.sleep(0.0007)
            comparatorValue = GPIO.input(4)
            if comparatorValue == 0:
                value = value - 2**i
            elif comparatorValue == 1:
                value = value + 2**i   
        voltage = value / levels * maxVoltage
        signal = bin2dac(value)
        time.sleep(0.01)
        print("Digital value = {:^3}, analog votage = {:.2f}".format(value, voltage))
        if value <= 2:
            led = bin2dac(0)
        elif value > 2 and value <= 32:
            led = bin2dac(128)
        elif value > 33 and value <= 64:
            led = bin2dac(192)
        elif value > 64 and value <= 96:
            led = bin2dac(224)
        elif value > 96 and value <= 131:
            led = bin2dac(240)
        elif value > 131 and value <= 160:
            led = bin2dac(248)
        elif value > 160 and value <= 192:
            led = bin2dac(252)
        elif value > 192 and value <= 224:
            led = bin2dac(254)
        elif value > 224:
            led = bin2dac(255)
        return led    
                         
            
    

try:
    while True:
        led = adc()
        GPIO.output(leds, led)
      
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    GPIO.output(leds, GPIO.LOW)
    GPIO.cleanup(leds)
    print("GPIO cleanup completed")