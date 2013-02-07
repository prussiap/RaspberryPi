#!/usr/bin/env python

# W. Greathouse - 1-Feb-2013
#       Python code derived from examining gb_spi.c/h
#       Original code header with Copyright follows.

##
## Gertboard test
##
## SPI (ADC/DAC) control code
##
## This code is part of the Gertboard test suite
## These routines access the AD and DA chips
##
##
## Copyright (C) Gert Jan van Loo & Myra VanInwegen 2012
## No rights reserved
## You may treat this program as if it was in the public domain
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
## ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
## LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
## SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
## INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
## CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
## ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
## POSSIBILITY OF SUCH DAMAGE.
##
##
## Try to strike a balance between keep code simple for
## novice programmers but still have reasonable quality code
##

# End of original header and Copyright

import time

import resetspi
import spidev

# SPI clock rate (default is 1MHz)
SPI_SPEED = 1000000

class gb_spi():
    def __init__(self):
        # self.setup_spi()
        return

    # Use spidev for accessing ADC an DAC
    def setup_spi(self, speed=SPI_SPEED):
        self.speed=speed
        # Open interface for ADC on CE0
        self.adc = spidev.SpiDev()
        self.adc.open(0,0)
        self.adc.max_speed_hz=self.speed
        # Open interface for DAC on CE1
        self.dac = spidev.SpiDev()
        self.dac.open(0,1)
        self.dac.max_speed_hz=SPI_SPEED

        # assure GPIO configuration is for SPI operation
        resetspi.spiConfig()

    #
    # Read a value from one of the two ADC channels
    #
    # To understand this code you had better read the
    # datasheet of the AD chip (MCP3002)
    #
    def read_adc(self, ab):
        # Minimum SPI transaction is 15 bits... but we need to use 16 bits
        # so we shift right the "start" bit by one bit to have result returned
        # in the lower bits.
        #
        #       start      single       channel      msb
        reg = (1 << 14) + (1 << 13) + (ab << 12) + (1 << 11)
        # Send / receive 24-bits as 8-bit bytes (xfer is used for active CEx)
        val = self.adc.xfer([(reg >> 16) & 0xff , (reg >> 8) & 0xff, reg & 0xff])
        # Convert returned bytes to integer, masking lower 10 significant bits
        # We must mask the result because the value of the upper bits is 
        # indeterminant as the bus is floating at hi-z except for conversion
        # result.
        return ((val[1]<<8) + val[2]) & 0x3ff


    #
    # Write 12-bit value to DAC channel (must be 0 or 1)
    #
    # To understand this code you had better read the
    # datasheet of the AD chip (MCP4802/MCP4812/MCP4822)
    #
    def write_dac(self, ab, val):
        # Minimum SPI transaction is 15 bits... but we need to use 16 bits
        # so we shift right the "start" bit by one bit to have result returned
        # in the lower bits.
        #
        #       channel     x1 gain     active       output
        reg = (ab << 15) + (1 << 13) + (1 << 12) + (val & 0xfff)

        # Send 16-bits as 8-bit bytes (xfer is used for active CEx)
        # ignore return value
        self.dac.xfer([(reg >> 8) & 0xff , reg & 0xff])

