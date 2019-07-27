"""
File: server.py
Author: dave
Email: davidisbest27@gmail.com
Github: https://github.com/davidus27
Description: Hlavny Python 3.x program pre Server.
    Pocitac pripojeny na Raspberry Pi so staticky nastavenou IP adresou pre spravnu komunikaciu.
    Program zachytava jednotlive obrazy z ktorych nasledne po Strojovom predspracovani obrazu ziska konturu pohybujuceho sa objektu v periferii kamery.
    
    Po spusteni a restartovani sa ulozi staticka snimka, oproti ktorej je kazda dalsia porovnavana pomocou thresholdovej funkcie. 

    Pri tvorbe vacsich jednotlivych rozdielov program vytvara vacsie jednotlive celky-kontury. 
    Kedze Raspberry Pi motory mozu sledovat len jeden objekt, vacsia kontura ziska hlavnu pozornost a 
    program vypocita priblizne stredove uhly objektu, ktore po niti presuva spatne Klientovi (Raspberry Pi).
    
    Po spusteni vytvori GUI ikony pre vyobrazenie pohladu kamery s najdenymi konturami. Pomocou Ikon sa da manipulovat s programom klavesami "q" na vypnutie a
    "r" na resetovanie statickej referencnej snimky.

"""
from time import sleep
from numpy import int0,uint8,ones,fromstring
from socket import socket
from _thread import start_new_thread
import cv2
import io
import struct
import os
