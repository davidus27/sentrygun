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


def receive(socket):
    """
    Sleduje tok informacii zo "serveru".
    Ovlada uhol motora na základe informácii ziskanych z toku.
    informacie su synchronizovane na X-ove a Y-ove suradnice.
    """
    pwm1 = motorPWM(50,pin1)
    pwm2 = motorPWM(50,pin2)
    while True:
        ok = struct.unpack("?",socket.recv(struct.calcsize('?')))
        x = struct.unpack("i",socket.recv(struct.calcsize('i')))
        y = struct.unpack("i",socket.recv(struct.calcsize('i')))
        if not ok:
                break
        uholMotora(pwm1,uhol = int(x[0]), gpioPin=a)
        uholMotora(pwm2,uhol = int(y[0]), gpioPin=b)
         

def vytvorKlienta():
    """
    Spustenie nahravania.
    Program bude cakat na lokalnej IP: 192.168.0.2:8000
    """
    klient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    klient.connect(('192.168.0.2', 8000))
    return klient   

def nastavSpojenie(klient):
    """
    Vytvori spojenie medzi klietom a serverom.
    """
    spojenie = klient.makefile('wb')
    thread.start_new_thread(receive,(klient, ))
    return spojenie


def kameraBootstrap():
    """
    Pociatocne nastavenia kamery
    """
    kamera = PiCamera()
    kamera.resolution = (320, 240)
    kamera.start_preview()
    sleep(2)
    return kamera


def pokracuj(spojenie,stream):
    """
    Vymaze staru fotku a pokracuje v streame dat
    """
    spojenie.write(struct.pack('<L', stream.tell()))
    spojenie.flush()
    stream.seek(0)
    spojenie.write(stream.read())
    stream.seek(0)
    stream.truncate()



def nahravanie(kamera,stream):
   """
   Vytvori pociatocny stream obrazu prenasany cez Ethernet.
   V streame kontroluje flow dat a posiela info o zmene obrazu pri zmene akceleratora.
   """
    stream = io.BytesIO()
    dhx,dhy,dhz = None,None,None
    for frame in kamera.capture_continuous(stream, 'jpeg'):
            data = bus.read_i2c_block_data(0x1D,0x00,6)
            osx = (data[1] & 0x03) * 256 + data [0]
            if osx > 511 :
                    osx -= 1024
            osy = (data[3] & 0x03) * 256 + data [2]
            if osy > 511 :
                    osy -= 1024
            osz = (data[5] & 0x03) * 256 + data [4]
            if osz > 511 :
                    osz -= 1024
            if dhx == None:
                    dhx = osx
            if dhy == None:
                    dhy = osy
            if dhz == None:
                    dhz = osz
            if dhx > osx+10 or dhx < osx-10 or dhy > osy+10 or dhy < osy-10 or dhz > osz+10 or dhz < osz-10:
                    spojenie.write(struct.pack('<L',long(1)))
            else:
                pokracuj(spojenie,stream)



def main():
    """
    Spustenie samotneho programu
    """
    akcelerometer()
    kamera = kameraBootstrap()
    spojenie = nastavSpojenie()
    kameraBootstrap(kamera)
    nahravanie(kamera,stream)
    
    spojenie.write(struct.pack('<L', 0))
    spojenie.close()
    klient.close()

if __name__ == "__main__":
   main() 

