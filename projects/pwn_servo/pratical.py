import RPi.GPIO as GPIO
import spidev
from time import sleep
from threading import Thread
from queue import Queue

class ParallaxServo:
    def __init__(self, assigned_pin):
        self.assigned_pin = assigned_pin
        self.queue = Queue()
        self.thread = None

    def start(self, initial_angle=45) -> Queue:
        self.thread = Thread(target=self.__thread, args=(initial_angle,))
        self.thread.start()
        return self.queue

    def set_angle(self, angle):
        regulated = angle
        if not 0 <= angle <= 90:
            print("[!] Angle must be between 0 to 90, clamping")
            regulated = min(max(angle, 90), 0)

        self.queue.put(regulated, block=False)

    def __thread(self, initial_angle):
        on = self.angle_to_duration(initial_angle)

        while True:
            if not self.queue.empty():
                on = self.angle_to_duration(self.queue.get(block=False))

            GPIO.output(self.assigned_pin, GPIO.HIGH)
            sleep(on)
            GPIO.output(self.assigned_pin, GPIO.LOW)
            sleep(0.020)

        return

    def angle_to_duration(self, angle):
        dur = 0.001 + (angle / 90 * 0.001)
        return dur

class SHARP2Y0A02:

    def __init__(self, spi_client_num):
        self.spi = spidev.SpiDev()
        self.latestly_read = None
        self.thread = None

        self.spi.open(spi_client_num, 0)
        self.spi.max_speed_hz = 1_000_000

    def start(self):
        self.thread = Thread(target=self.__thread)
        self.thread.start()

    def read(self):
        while self.latestly_read is None:
            pass

        return self.latestly_read

    def __thread(self):
        while True:
            # BITS
            #   6543210 76543210
            #       XXXXXXXXXXXX
            #   SSCM
            #   TGHS
            #   ALAB
            #   R NF
            #   T
            resp = self.spi.xfer2([0b1101000, 0b0000000])
            volume = ((resp[0] << 8) + resp[1]) & 0x3FF
            self.latestly_read = volume
            sleep(0.1)

def main():
    pin = 11

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)

    servo = ParallaxServo(pin)
    servo.start()

    dist = SHARP2Y0A02(0)
    dist.start()
    
    (minimum, maximum) = (146, 731)
    while True:
        d = dist.read()
        percent = (d - 146) / 731
        angle = 90 * (percent > 0.75)

        servo.set_angle(angle)

        print("\x1b[A{:3}%, {:2}deg".format(int(percent * 100), angle))

        sleep(0.1)
        

if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()
