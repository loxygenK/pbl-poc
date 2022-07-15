import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
from queue import Queue

class ParallaxServo:
    def __init__(self, assigned_pin):
        self.assigned_pin = assigned_pin
        self.queue = Queue()
        self.thread = None

    def start(self) -> Queue:
        self.thread = Thread(target=self.__thread)
        self.thread.start()
        return self.queue

    def __thread(self):
        print("Self:", self)
        return

inst = ParallaxServo(1)
inst.start()
inst.thread.join()


# pin = 11 # Correspondes to GPIO 17
# servo = None
# 
# def init():
#     global servo
# 
#     GPIO.setmode(GPIO.BOARD)
#     GPIO.setup(pin, GPIO.OUT)
#     # servo = GPIO.PWM(pin, 800_000)
# 
#     print("--> Successfully configured GPIO Output pin")
# 
# def main():
#     duty = 7
#     # servo.start(duty)
# 
#     for _ in range(1000):
#         GPIO.output(pin, GPIO.HIGH)
#         sleep(0.001)
#         GPIO.output(pin, GPIO.LOW)
#         sleep(0.020)
# 
#     #for d in range(0, 101, 1):
#     #    if(d % 1 == 0):
#     #        print("\x1b[ANow {} percent".format(d))
#     #    servo.ChangeDutyCycle(d)
#     #    sleep(0.1)
# 
#     #for d in range(100, -1, -1):
#     #    if(d % 1 == 0):
#     #        print("\x1b[ANow {} percent".format(d))
#     #    servo.ChangeDutyCycle(d)
#     #    sleep(0.1)
# 
#     print("Stopping PWM Generation")
#     servo.stop()
# 
# def finalize():
#     print("Cleaning up")
#     servo.stop()
#     GPIO.cleanup()
# 
# if __name__ == "__main__":
#     try:
#         init()
#         main()
#     finally:
#         finalize()
