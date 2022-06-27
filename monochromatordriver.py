import serial
import time

class Monochromator:
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600, timeout = 2)
        self.stepcount = 0
        self.wavelength = 0
        self.status = "" # fwdlim, revlim, err, good

        print(self.ser.readline())

        #self.settominwavelength() # set to minimum wavelength by default

    def update_status(self):
        # reads byte from serial and uses byte to update status
        incoming = self.ser.read().decode('ascii')
        if incoming == None: self.status = "err"
        elif incoming == "1": self.status = "good"
        elif incoming == "2": self.status = "revlim"
        elif incoming == "3": self.status = "fwdlim"
        else: self.status = "err"

    def enable(self):
        self.ser.write('3'.encode('ascii'))
        self.update_status()
        time.sleep(0.1)

    def disable(self):
        self.ser.write('4'.encode('ascii'))
        self.update_status()
        time.sleep(0.1)

    def steponce(self, dir):
        if dir:
            self.ser.write('1'.encode('ascii'))
            self.stepcount += 1
        else:
            self.ser.write('2'.encode('ascii'))
            self.stepcount -= 1
        
        self.update_status()
        self.update_wavelength()
        time.sleep(0.025)

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

    def set_wavelength(self, wavelength):
        return 0
        while wavelength != self.wavelength:
            if wavelength > self.wavelength: self.steponce(True)
            else: self.steponce(False)
            self.update_wavelength()

            if self.status != "good": raise Exception("received error ", self.status, "when setting to wavelength", wavelength)

    def update_wavelength(self):
        # TODO: update when we know step -> wavelength relationship
        self.wavelength =  self.stepcount/10 - self.wavelengthmin
        return 0