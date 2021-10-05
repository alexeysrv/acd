import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(17, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(4, GPIO.IN)

def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def bin2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac, signal)
    return signal

def adc():
    while True:
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
        

            
    

try:
    
    adc()
      
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print("GPIO cleanup completed")