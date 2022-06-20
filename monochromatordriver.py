import serial
import time

class Monochromator:
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600, timeout = 1)
        self.stepcount = 0
        self.wavelength = 0
        self.status = "" # fwdlim, revlim, err, good

        self.settominwavelength() # set to minimum wavelength by default

    def updatestatus(self):
        # reads byte from serial and uses byte to update status
        incoming = int(self.ser.read())
        if incoming == None: self.status = "err"
        elif incoming == 1: self.status = "good"
        elif incoming == 2: self.status = "revlim"
        elif incoming == 3: self.status = "fwdlim"
        else: self.status = "err"

    def enable(self):
        self.ser.write(3)
        time.sleep(0.1)

    def disable(self):
        self.ser.write(4)
        time.sleep(0.1)

    def steponce(self, dir):
        if dir:
            self.ser.write(1)
            self.stepcount += 1
        else:
            self.ser.write(2)
            self.stepcount -= 1
        
        self.update_status()
        self.update_wavelength()
        time.sleep(0.1)

    def setstepcount(self, desired):
        while self.stepcount != desired:
            if self.stepcount < desired: self.steponce(True)
            else: self.steponce(False)
            if self.status != "good": break

    def settominwavelength(self):
        # decreases step count until self.status -> revlim
        while self.status == "good":
            self.steponce(False)

        if self.status == "revlim": return
        else: raise Exception("received error ", self.status, "when setting to minimum wavelength")

    def set_wavelength(self):
        return 0
        # TODO: update when we know step -> wavelength relationship

    def update_wavelength(self):
        # TODO: update when we know step -> wavelength relationship
        return 0