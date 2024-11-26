from machine import Pin, UART
import time

UART_TX = 12
UART_RX = 13
DIR = 10
STEP = 21
EN = 20

# configure the pins
pin_dir = Pin(DIR, Pin.OUT)
pin_step = Pin(STEP, Pin.OUT)
pin_en = Pin(EN, Pin.OUT)
tmc = UART(0, baudrate=11520, tx=Pin(UART_TX), rx=Pin(UART_RX))

# try to establish uart connection with the TMC2209

tmc.init()

# try to talk to the TMC2209
tmc.write("hello")
time.sleep(0.1)
print(tmc.read())
