import spidev #hardware spi

ldr_pin = 0
temp_pin = 1
moisture1_pin = 6
moisture2_pin = 7

spi = spidev.SpiDev()
spi.open(0,0)

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    r = spi.xfer2([1,(8+adcnum)<<4,0])
    adcout = ((r[1]&3) << 8) + r[2]
    return adcout


def check_temp(tmp_pin): # check temperature and convert it to F
	tmp_analog = readadc(tmp_pin)
	temp = (tmp_analog /10) *1.800 + 32
	return str(temp)
	
def check_LDR(ldr_pin): # Check photocell values
	return readadc(ldr_pin)

def check_moisture(moisture_pin): # Check Moisture Sensor data
	return readadc(moisture_pin)


print "The temp in your room is: " + check_temp(temp_pin) + " F"
print check_LDR(ldr_pin)
print "Moisture Sensor 7: " + str(check_moisture(moisture1_pin))
print "Moisture Sensor 8: " + str(check_moisture(moisture1_pin))


