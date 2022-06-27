import serial
import time

class Monochromator:
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600, timeout = 2)
        self.stepcount = 0
        self.wavelength = 0
        self.wavelengthstart = 400
        self.status = "" # fwdlim, revlim, err, good
        self.enabled = False

        print(self.ser.readline())

        self.wavelength = self.wavelengthstart

        if input("Set monochromator to 400 nm (yes/no)? ") != "yes":
            raise Exception("Monochromator must be set to expected wavelength before use")

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
        if self.status == "good": self.enabled = True
        time.sleep(0.1)

    def disable(self):
        self.ser.write('4'.encode('ascii'))
        self.update_status()
        if self.status == "good": self.enabled = False
        time.sleep(0.1)

    def steponce(self, dir):

        if not self.enabled:
            raise Exception("Monochromator must be enabled before stepping")

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
        while wavelength != self.wavelength:
            if wavelength > self.wavelength: self.steponce(True)
            else: self.steponce(False)
            self.update_wavelength()

            if self.status != "good": raise Exception("received error ", self.status, "when setting to wavelength", wavelength)

    def update_wavelength(self):
        self.wavelength =  self.wavelengthstart + self.stepcount/10
        return 0

    def get_wavelength(self):
        return self.wavelength