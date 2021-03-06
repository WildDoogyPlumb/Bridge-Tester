#!/usr/bin/python


import os
import pygame
import random
import time
import serial
from pygame.locals import *
from threading import Thread  # import

from technical import *


pi = 0  # 1 = running on pi, 0 = running in test mode
if os.path.exists("/dev/i2c-0"):  # Am I running on a pi?
    pi = 1
    import smbus

if pi == 1:
    print "[INFO] Detected I2C. Running normally"
else:
    print "[INFO] Did not detect I2C. Running in simulation mode"


def log(*args):
    print "[Main]",
    # print time.strftime("%c"),
    # print " ",
    for arg in args:
        print arg,
    print ""



class fakeIIC():
    def read_word_data(self, a, b):
        return int(random.random() * 65535)

    def write_byte_data(self, a, b, c):
        pass

    def write_word_data(self, a, b, c):
        pass


class IOThread(Thread):
    def __init__(self):  ## to pass a variable to the class add here
        Thread.__init__(self)
        self.pressure = 0
        self.distance = 0
        self.PTare = 0
        self.DTare = 0
        self.pgaSetting = 0x8060
        self.pressureAddress = 0x49  # Address of Pressure ADC
        self.distanceAddress = 0x48  # Address of Distance ADC (adddr hooked to vcc)
        self.ledAddresses = [0x60, 0x61, 0x62, 0x63, 0x64]  # Addresses of LED 7 segment display Drivers
        self.bus = fakeIIC()  # just init this in case something ties to use it.
        self.segmentLookup = [63, 6, 91, 79, 102, 109, 125, 7, 127, 111, 119, 124, 57, 94, 121, 113, 123]
        self.pressureArray = []
        self.lastPressure = 0
        self.lastDistance = 0
        self.Display = [0] * 5
        self.pga = 2
        self.fps = 0
        self.lasttime = time.time()
        if pi == 1:  # running on a Pi?
            self.bus = self.initI2C(self.pressureAddress, self.distanceAddress)

    def initI2C(self, pressureA, distanceA):
        bus = smbus.SMBus(1)  # Setup IIC
        bus.write_word_data(pressureA, 0x01, self.pgaSetting)  # Default setup for Pressure
        bus.write_word_data(distanceA, 0x01, self.pgaSetting)  # Default setup for Distance
        # LEDS don't need setup
        return bus

    @staticmethod
    def find_all_USBs():
        """
        This function finds all connected USB sensors
        :return: Returns a list of strings, EG: 'ttyUSB0'
        """
        return [dev for dev in os.listdir("/dev/") if dev.startswith("ttyUSB")]

    def connect_USBs(self):
        """
        Opens a serial stream to the sensors, and tries to determine which is which.
        Streams are stored to local variables
        """
        all_devs = self.find_all_USBs()  # Get all USB devices to scan
        # Make sure there are 2 connected
        if len(all_devs) == 0:
            log("[ERROR] There are no detected sensors")
            raise IOError
        elif len(all_devs) == 1:
            log("[ OK ] One sensor connected at '/dev/{}'.".format(all_devs[0]))
            raise IOError
        elif len(all_devs) > 2:
            log("[WARNING] More than one sensor detected. Will try to determine which sensors to use.\n\tSensors:{}".format(all_devs))

        # Check all devices to figure out which is force, and which is displacement.
        for dev in all_devs:
            baud = 115200
            self.force_serial = serial.Serial(port='/dev/' + dev, baudrate=baud)
            if not self.force_serial.isOpen():
                self.force_serial.open()
            self.force_serial.write("RATE 8\n\r")

    def pollpress(self):
        self.force_serial.write("P\n\r")
        self.force_serial.flush()
        time.sleep(.01)
        msg = ""
        while self.force_serial.inWaiting():
            msg += self.force_serial.read(1)
        reading_raw = msg[0:msg.find("P")]
        try:
            pressure = float(reading_raw)
        except ValueError:
            pressure = None

        pressure -= self.PTare

        if pressure is not None:
            self.pressureArray.append([pressure, self.lastDistance, time.time()])  # time.time is far away from reading, but should be ok
        return pressure

    def pollpress2(self):
        readingraw = convertReading(self.bus.read_word_data(self.pressureAddress, 0x00))
        # if readingraw > 1000:
        # if self.pga == 2:
        # self.pga = 1
        # self.bus.write_word_data(self.pressureAddress,0x01,self.pgaSetting) # Gain of 2
        # elif self.pga == 4:
        # self.pga = 2
        # self.bus.write_word_data(self.pressureAddress,0x01,self.pgaSetting+2) # Gain of 4
        # readingraw = convertReading(self.bus.read_word_data(self.pressureAddress,0x00))
        # if readingraw < 500:
        # if self.pga == 1:
        # self.pga = 2
        # self.bus.write_word_data(self.pressureAddress,0x01,self.pgaSetting+2) # Gain of 2
        # elif self.pga == 2:
        # self.pga = 4
        # self.bus.write_word_data(self.pressureAddress,0x01,self.pgaSetting+4) # Gain of 4
        # readingraw = convertReading(self.bus.read_word_data(self.pressureAddress,0x00))
        pressure = (readingraw) / (2.0 ** self.pga)
        pressure -= self.PTare
        # if pressure < 50000:
        self.pressureArray.append([pressure, self.lastDistance, time.time()])  # time.time is far away from reading, but should be ok
        return pressure
        # else:
        #        return 0.0

    def setled(self, cellAddress, numberToDisplay):
        self.bus.write_byte_data(cellAddress, 0x44, self.segmentLookup[numberToDisplay])

    def getdist(self):
        readingraw = convertReading(self.bus.read_word_data(self.distanceAddress, 0x00))
        distance = (readingraw - 1200) / 1200.0
        distance -= self.DTare
        return distance

    def run(self):  ## dont need it here
        self.error = 0
        self.polls = 0
        while self.error == 0:  ## Main thread program using passed variable
            self.lastPressure = self.pollpress()
            # self.lastDistance = self.getdist()
            self.lastDistance = time.time() - self.lasttime
            # print("Pressure",self.pressure)
            # time.sleep(.001)
            # self.LED = 0
            # if self.polls%100 == 0:
            #    self.fps = 100/(time.time()-self.lasttime)
            #    self.lasttime = time.time()
            # self.polls+=1
            # while (self.count < 5):
            #    self.pollpress()
            #    #self.setled(self.ledAddresses[self.LED],self.Display[self.LED])
            #    self.count += 1
            #    self.LED += 1
            #    #print("LED",self.LED)
            #    #print("distance",self.distance)
            #    time.sleep(.0057)


def Draw_Chart(surface, x, y, hsize, vsize, dataset, (DataStart, DataEnd), (DXMin, DXMax), (DYMin, DYMax), color, stroke, bordercolor, border, stringFormat,
               MLfont):
    global timev
    times = [timev]
    times.append(time.time())  #################
    DataLen = DataEnd - DataStart
    DataHeightX = DXMax - DXMin
    DataHeightY = DYMax - DYMin
    xscale = (hsize + 1) / DataLen
    xscale2 = (hsize) / DataHeightX
    yscale = -(vsize - 60) / DataHeightY
    maxVal = 0
    maxInd = 0
    times.append(time.time())  #################
    MLfont = pygame.font.Font("freesansbold.ttf", 30)
    times.append(time.time())  #################
    if border >= 1:
        pygame.draw.lines(surface, bordercolor, 0, ((x, y), (x, y + vsize), (x + hsize, y + vsize), (x + hsize, y), (x, y)), border)
    times.append(time.time())  #################
    lines = []
    for j in range(DataLen):
        i = dataset[j + DataStart]
        if i[1] > maxVal:
            maxVal = i[1]
            maxInd = j
        lines.append((x + ((i[0] - DXMin) * xscale2), y + vsize + ((i[1] - DYMin) * yscale)))
    times.append(time.time())  #################
    pygame.draw.lines(surface, color, 0, lines, stroke)
    times.append(time.time())  #################
    pygame.draw.circle(surface, (0, 0, 255, 128), (int(lines[-1][0]), int(lines[-1][1])), 10)
    times.append(time.time())  #################
    px, py = (x + ((dataset[maxInd][0] - DXMin) * xscale2), y + vsize + ((dataset[maxInd][1] - DYMin) * yscale))
    tag = [(px + 20, py), (px, py - 20), (px - 20, py), (px, py + 20), (px + 20, py)]
    times.append(time.time())  #################
    if px > hsize / 2:
        tx, ty = px - 220, py
        pygame.draw.lines(surface, (0, 255, 0), 0, ((px - 20, py), (tx + 150, ty)), 2)
    else:
        tx, ty = px + 220, py
        pygame.draw.lines(surface, (0, 255, 0), 0, ((px + 20, py), (tx - 150, ty)), 2)
    times.append(time.time())  #################
    tag2 = [(tx + 150, ty), (tx + 130, ty - 20), (tx - 130, ty - 20), (tx - 150, ty), (tx - 130, ty + 20), (tx + 130, ty + 20), (tx + 150, ty)]
    pygame.draw.lines(surface, (0, 255, 0), 0, tag, 2)
    pygame.draw.lines(surface, (0, 255, 0), 0, tag2, 2)
    pygame.draw.lines(surface, (0, 255, 0), 0, ((tx, ty - 20), (tx - 130, ty - 20)), 2)
    times.append(time.time())  #################
    surface.blit(MLfont.render(stringFormat.format(dataset[maxInd][1]), 1, (0, 255, 0)), (tx - 130, ty - 14))
    times.append(time.time())  #################
    try:
        surface.blit(font.render("Choords: " + str((float(lines[3][0]), float(lines[3][1]))), 1, (100, 255, 100)), (40, 400))
        surface.blit(font.render("Choords: " + str((float(dataset[3][0]), float(dataset[3][1]))), 1, (100, 255, 100)), (40, 420))
        surface.blit(font.render("Last: " + str((float(lines[-1][0]), float(lines[-1][1]))), 1, (100, 255, 100)), (40, 440))
        surface.blit(font.render("Last: " + str((float(dataset[-1][0]), float(dataset[-1][1]))), 1, (100, 255, 100)), (40, 460))
        surface.blit(font.render("Max: " + str((float(DXMax), float(DXMin), float(DYMax), float(DYMin))), 1, (100, 255, 100)), (40, 480))
    except:
        pass
    return times


def Main():
    ################ Pygame Init
    pygame.init()
    fpsclock = pygame.time.Clock()
    WindowSurface = pygame.display.set_mode((1918, 1078))  # ,pygame.FULLSCREEN)
    pygame.display.set_caption("Pygame Test")
    fps = 0

    ################# Pygame declarations
    # CustomImage = pygame.image.load("test.png")
    MouseSurface = pygame.Surface((32, 32), 0, 8).convert_alpha()
    MouseSurface.fill((0, 100, 0, 0))
    pygame.draw.line(MouseSurface, (0, 255, 0), (16, 0), (16, 32), 1)
    pygame.draw.line(MouseSurface, (0, 255, 0), (0, 16), (32, 16), 1)

    font = pygame.font.Font("freesansbold.ttf", 12)
    forceFont = pygame.font.Font("freesansbold.ttf", 200)
    MLfont = pygame.font.Font("freesansbold.ttf", 30)
    runProgram = 1
    mousex, mousey = 0, 0
    lines = []
    Load = [0, 50000]
    Dist = [0, 50000]
    tp = 0.0
    td = 0.0
    PGA = 0
    setting = tclass.pgaSetting + (tclass.pga * 2)
    print hex(setting)
    # tclass.bus.write_word_data(tclass.distanceAddress,0x01,0x0000)
    tclass.bus.write_word_data(tclass.pressureAddress, 0x01, setting)
    global timev
    times = []
    charttimes = []
    f = open("/home/ben/Bridge_Tester/Python/times.csv", "w")
    while runProgram:
        times.append(time.time())  #################
        WindowSurface.fill(pygame.Color(0, 0, 0))  # Screen Redraw
        times.append(time.time())  #################
        # Process events
        for event in pygame.event.get():
            if event.type == QUIT:
                runProgram = 0
                break
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    runProgram = 0
                    tclass.error = 1
                    break
                if event.key == K_UP:
                    tclass.pga = clamp(tclass.pga + 1, 2, 5)
                    setting = tclass.pgaSetting + (tclass.pga * 2)
                    print hex(setting)
                    # tclass.bus.write_word_data(tclass.distanceAddress,0x01,0x0000)
                    tclass.bus.write_word_data(tclass.pressureAddress, 0x01, setting)
                if event.key == K_DOWN:
                    tclass.pga = clamp(tclass.pga - 1, 2, 5)
                    setting = tclass.pgaSetting + (tclass.pga * 2)
                    print hex(setting)
                    # tclass.bus.write_word_data(tclass.distanceAddress,0x01,0x0000)
                    tclass.bus.write_word_data(tclass.pressureAddress, 0x01, setting)
                if event.key == K_RIGHT:
                    lines = []
                    Load = [0, 50000]
                    Dist = [0, 50000]
                    tclass.DTare = tclass.lastDistance + tclass.DTare
                    # tclass.PTare = tclass.lastPressure+tclass.PTare
                    tclass.PTare = 0
                    tp = 0.0
                    td = 0.0
                    time.sleep(.1)
                    while len(tclass.pressureArray) > 1:
                        tmpAr = tclass.pressureArray.pop()  # clear saved pressures
                if event.key == K_LEFT:
                    print td
        times.append(time.time())  #################
        while len(tclass.pressureArray) > 51:
            readings = 0
            pressures = 0
            maxPressure = 0
            distances = 0
            for i in range(50):
                tmpAr = tclass.pressureArray.pop(0)
                readings += 1
                pressures += tmpAr[0]
                distances += tmpAr[1]
                maxPressure = max(tmpAr[0], maxPressure)
            if readings > 0:
                # tp = pressures/readings #Averages
                tp = maxPressure  # Max
                td = distances / readings
                if tp > Load[0]:
                    Load[0] = tp
                if tp < Load[1]:
                    Load[1] = tp
                if td > Dist[0]:
                    Dist[0] = td
                if td < Dist[1]:
                    Dist[1] = td
                    # print Dist, Load
            lines.append([td, tp])
        times.append(time.time())  #################
        if len(lines) > 2:
            timev = time.time()
            charttimes = Draw_Chart(WindowSurface, 10, 220, 1380, 800, lines, (0, len(lines)), (Dist[1], clamp(Dist[0], Dist[1] + .2, 300000)),
                                    (Load[1], clamp(Load[0], Load[1] + 80, 300000)), (255, 0, 0), 1, (255, 255, 255), 3, "{0:.2f} LB", MLfont)
        times.append(time.time())  #################
        # Draw
        # WindowSurface.blit(MouseSurface,(mousex-16,mousey-16))
        WindowSurface.blit(forceFont.render("{0:.1f} LB".format(tp), 1, (100, 255, 100)), (10, 10))
        WindowSurface.blit(forceFont.render("{0:.3f}\"".format(td), 1, (100, 255, 100)), (1100, 10))
        # WindowSurface.blit(forceFont.render(str(hex(int(td*535)+1100))[:6]+"\"",1,(100,255,100)),(700,10))
        WindowSurface.blit(font.render("Max Load: " + str(60000 / (2 ** tclass.pga))[:5] + "", 1, (100, 255, 100)), (600, 10))
        # WindowSurface.blit(font.render("FPS: {0:.1f}".format(1/(time.time()-fps)),1,(100,255,100)),(600,30))
        times.append(time.time())  #################
        tgd = []
        for i in range(1, len(times)):
            tgd.append((i, times[i] - times[i - 1]))
        ctgd = []
        for i in range(1, len(charttimes)):
            ctgd.append((i, charttimes[i] - charttimes[i - 1]))
        times = []
        times.append(time.time())  #################
        # Draw_Chart(WindowSurface,1400,220,400,800,tgd,(0,len(tgd)),(1,len(tgd)),(0,.1),(0,255,0),1,(255,255,255),3,"{0:.6f}",MLfont)
        # Draw_Chart(WindowSurface,1400,220,400,800,ctgd,(0,len(ctgd)),(1,len(ctgd)),(0,.1),(0,0,255),1,(255,255,255),3,"{0:.6f}",MLfont)
        WindowSurface.blit(font.render("Lines: " + str(len(lines)), 1, (100, 255, 100)), (1600, 240))
        WindowSurface.blit(font.render("Polling Frequency: " + str(int(tclass.fps)), 1, (100, 255, 100)), (1600, 260))
        WindowSurface.blit(MLfont.render("Min: " + str(Load[1]), 1, (100, 255, 100)), (10, 240))
        WindowSurface.blit(MLfont.render("Pressure Tare: " + str(tclass.PTare), 1, (100, 255, 100)), (10, 270))
        times.append(time.time())  #################
        pygame.display.update()
        times.append(time.time())  #################
    f.close()
    pygame.quit()


timev = 0

tclass = IOThread()  ## create instance
tclass.start()  ## start class running

Main()
