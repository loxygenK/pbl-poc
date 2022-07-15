import spidev
import time
import sys

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

while True:
	try:
		resp = spi.xfer2([0x68, 0x00])
		volume = ((resp[0] << 8) + resp[1]) & 0x3FF
		print(volume, resp)
		time.sleep(1)
	except KeyboardInterrupt:
		spi.close()
		sys.exit()
