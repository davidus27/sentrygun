"""
File: client.py
Author: dave
Email: davidisbest27@gmail.com
Github: https://github.com/davidus27
Description: Hlavny Python 2.x program pre Raspberry Pi v podobe Klienta pre hlavnu komunikaciu s pocitacom v ulohe Servera. Program inicializuje cez Ethernet lokalne spojenie cez staticku IP adresu: 
            -Klient:192.168.0.2:8000
            -Server:192.168.0.1:8000
    Na zaklade informacii spracovanych zo samotneho Servera sa vratia x-ove a y-ove suradnice pre servomotory. Po nastaveni servomotorov sa mozu pohybovat do danych suradnic. 
    Aktivne sledovanie suradnic z akcelerometra posielaju informaciu o resetovani statickeho obrazu pre Server na lepsie spracovanie kontur prostredia.
"""

import io
import socket
import struct
from time import sleep
from picamera import PiCamera
import RPi.GPIO as gpio
import thread
import smbus


#GPIO PINOUT
#definovane konstanty pre Raspberry Pi ktore PINy budeme pouzivat
pin1 = 11
pin2 = 12

def akcelerometer():
    """
    Inicializovanie hodnot pre akcelerometer
    """
    bus = smbus.SMBus(1)
    bus.write_byte_data(0x1D,0x16,0x01)


def motorPWM(frekvencia=50, gpioPin=0):
    """
    Inicializacia servomotora pre jednotlivy gpio pin
    """
    gpio.setwarnings(False)
    gpio.setup(gpioPin,gpio.OUT)
    pwm = gpio.PWM(gpioPin,frekvencia)
    pwm.start(0)
    return pwm


def uholMotora(pwm,uhol,gpioPin =0):
    """
    posunie motor pripojeny na gpioPin na zaklade
    vstupneho uhla.
    Funkcia prepocita uhol na PWM signal a nastavi podla neho servomotor.
    """
    uloha = (uhol /18)+2
    gpio.output(gpioPin, True)
    pwm.ChangeDutyCycle(uloha)
    sleep(1)
    gpio.output(gpioPin,False)
    pwm.ChangeDutyCycle(0)

