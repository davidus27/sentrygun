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


def pripojenie():
    """Pripája sa na sieťový socket"""
    server_soket = socket()
    try:
        server_soket.bind(('0.0.0.0', 8000))
    except OSError as e:
        os.system("taskkill /F /IM Python.exe")
    else:
        server_soket.listen(0)
        return server_soket


class Projekt(object):
    def __init__(self):
        pass

    
    def prenos(self,spojenie,velkost_snimky =0):
        """ Ziskava z vlakna snimku """
        self.stream = BytesIO()
        self.stream.write(spojenie.read(velkost_snimky))
        self.stream.seek(0)
    

    def dekodovanie(self):
        """ Dekoduje stream obrazov na ndarray format z kniznice numpy"""
        data = fromstring(self.stream.getvalue(), dtype=uint8)
        self.snimka = cv2.imdecode(data, 1)


   def spracovanie_obrazu(self):
        """ Spracovava obraz a vracia kontury """
        kernel = ones((3,3),uint8)
        seda = cv2.cvtColor(self.snimka, cv2.COLOR_BGR2GRAY)
        seda = cv2.medianBlur(seda,5)
        seda = cv2.morphologyEx(seda,cv2.MORPH_CLOSE,kernel)
        if self.prva_snimka is None:
                self.prva_snimka = seda
        self.rozdielova_snimka = cv2.absdiff(self.prva_snimka,seda)
        ret,self.binarna_snimka = cv2.threshold(self.rozdielova_snimka,35,200,cv2.THRESH_BINARY)
        self.binarna_snimka = cv2.morphologyEx(self.binarna_snimka,cv2.MORPH_CLOSE,kernel)
        (__,self.kontury,__) = cv2.findContours(self.binarna_snimka,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

    def stredovy_bod(self, i):
        """ Zistuje stred objektu"""
        M = cv2.moments(i)
        self.stred = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        self.hodnotax = 55.32 + (self.betax*self.stred[0]) 
        self.hodnotay = 62.57 + (self.betay*self.stred[1])


    def posli(self,cl):
        """ Posiela hodnoty x a y spolu so synchronizačnou Boolean hodnotou"""
        cl.sendall(struct.pack("?",True))
        cl.sendall(struct.pack("i",int(self.hodnotax)))
        cl.sendall(struct.pack("i",int(self.hodnotay)))


    def vyobrazenie(self,i):
        """ Vytvára ohraničenie objektu a označenie stredového bodu"""	
        cv2.circle(self.snimka, self.stred, 5,(255,255,255), -2)
        cv2.putText(self.snimka, "uhol x:{0}".format(int(self.hodnotax)),(0,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),0)
        cv2.putText(self.snimka, "uhol y: {0}".format(int(self.hodnotay)),(0,45),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),0)

    def ikony(self):
        """ Spušťa ikony"""
        cv2.imshow("Kamera", self.snimka)
        cv2.imshow("Threshold ",self.rozdielova_snimka)
        cv2.imshow("Rozdiel",self.binarna_snimka)



def main():
    server_soket = pripojenie()

if __name__ == "__main__":
    main()
