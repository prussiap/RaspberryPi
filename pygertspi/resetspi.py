#!/usr/bin/env python

# W. Greathouse - 1-Feb-2013
#       Reset GPIO settings for alternate SPI operation
#
# #######
# For SPI configuration test
import os
import mmap

BCM2708_PERI_BASE=0x20000000
GPIO_BASE=(BCM2708_PERI_BASE + 0x00200000)
BLOCK_SIZE=4096

# there is a better way to do conversions, but this works

# Convert character array to integer
def _strto32bit_(str):
    return ((ord(str[3])<<24) + (ord(str[2])<<16) + (ord(str[1])<<8) + ord(str[0]))

# Convert integer to character array
def _32bittostr_(val):
    return chr(val&0xff) + chr((val>>8)&0xff) + chr((val>>16)&0xff) + chr((val>>24)&0xff)


# Use /dev/mem to access BCM GPIO configuration registers
def spiConfig():
    # Use /dev/mem to gain access to peripheral registers
    mf=os.open("/dev/mem", os.O_RDWR|os.O_SYNC)
    m = mmap.mmap(mf,BLOCK_SIZE, mmap.MAP_SHARED, 
            mmap.PROT_READ|mmap.PROT_WRITE,offset=GPIO_BASE)
    # can close the file after we have mmap
    os.close(mf)

    # Read first two registers (have SPI pin function assignements)
    # GPFSEL0
    m.seek(0)
    reg0=_strto32bit_(m.read(4))
    # GPFSEL1
    m.seek(4)
    reg1=_strto32bit_(m.read(4))
    # print bin(reg0)[2:].zfill(32)[2:]
    # print bin(reg1)[2:].zfill(32)[2:]

    # GPFSEL0 bits --> x[2] SPI0_MISO[3] SPI0_CE0[3] SPI0_CE1[3] x[21]
    #                        GPIO 9       GPIO 8      GPIO 7 
    # We only use SPI0_CEx depending on setup, but make sure all are set up
    m0 = 0b00111111111000000000000000000000 
    s0 = 0b00100100100000000000000000000000
    b0 = reg0 & m0
    if b0 <> s0:
        print "SPI reg0 configuration not correct. Updating."
        reg0 = (reg0 & ~m0) | s0
        m.seek(0)
        m.write(_32bittostr_(reg0))

    # GPFSEL1 bits --> x[26] SPI0_MOSI[3] SPI0_SCLK[3]
    #                        GPIO 11       GPIO 10
    m1 = 0b00000000000000000000000000111111 
    s1 = 0b00000000000000000000000000100100
    b1 = reg1 & m1
    if b1 <> s1:
        print "SPI reg1 configuration not correct. Updating."
        reg1 = (reg1 & ~m1) | s1
        m.seek(4)
        m.write(_32bittostr_(reg1))

    # No longer need the mmap
    m.close()


if __name__ == '__main__':
    spiConfig()

