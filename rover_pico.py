from machine import Pin, PWM
from time import sleep

# Motor A pins
ain1 = Pin(2, Pin.OUT)
ain2 = Pin(3, Pin.OUT)
pwma = PWM(Pin(4))
pwma.freq(1000)

# Motor B pins
bin1 = Pin(5, Pin.OUT)
bin2 = Pin(6, Pin.OUT)
pwmb = PWM(Pin(7))
pwmb.freq(1000)

# Standby pin
stby = Pin(8, Pin.OUT)
stby.high()   # Enable driver

def stop():
    ain1.low()
    ain2.low()
    bin1.low()
    bin2.low()
    pwma.duty_u16(0)
    pwmb.duty_u16(0)

def forward(speed=30000):
    ain1.high()
    ain2.low()
    bin1.high()
    bin2.low()
    pwma.duty_u16(speed)
    pwmb.duty_u16(speed)

def backward(speed=30000):
    ain1.low()
    ain2.high()
    bin1.low()
    bin2.high()
    pwma.duty_u16(speed)
    pwmb.duty_u16(speed)

def left(speed=30000):
    ain1.low()
    ain2.high()
    bin1.high()
    bin2.low()
    pwma.duty_u16(speed)
    pwmb.duty_u16(speed)

def right(speed=30000):
    ain1.high()
    ain2.low()
    bin1.low()
    bin2.high()
    pwma.duty_u16(speed)
    pwmb.duty_u16(speed)

# Demo sequence
while True:
    forward()
    sleep(2)
    backward()
    sleep(2)
    left()
    sleep(1)
    right()
    sleep(1)
    stop()
    sleep(2)
