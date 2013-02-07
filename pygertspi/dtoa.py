#! /usr/bin/env python

# W. Greathouse - 1-Feb-2013

# Simple conversion of Gert's C code to Python for SPI access to DAC and ADC
# using spidev

#       Python code derived from examining dtoa.c
#       Original code header with Copyright follows.

##
## Gertboard Demo
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

import time
import gb_spi


#
#  Do digital to analogue to digital conversion
#
def main():
    while True:
        chan = raw_input ("Which channel do you want to test? Type 0 or 1. ")
        if (chan == '0' or chan == '1'):
            break;

    chan = ord(chan) - ord('0');

    print "These are the connections for the digital to analogue test:"
    print "jumper connecting GP11 to SCLK"
    print "jumper connecting GP10 to MOSI"
    print "jumper connecting GP9 to MISO"
    print "jumper connecting GP7 to CSnB"
    print "Multimeter connections (set your meter to read V DC):"
    print "  connect black probe to GND"
    print "  connect red probe to DA%d on J29" % chan
    raw_input ("When ready hit enter.")

    # enable and access SPI
    spi = gb_spi.gb_spi()
    spi.setup_spi()

    # Most likely, the DAC you have installed is an 8 bit one, not 12 bit so 
    # it will ignore that last nibble (4 bits) we send down the SPI interface.
    # So the number that we pass to write_dac will need to be the number
    # want to set (between 0 and 255) multiplied by 16. In hexidecimal,
    # we just put an extra 0 after the number we want to set.
    # So if we want to set the DAC to 64, this is 0x40, so we send 0x400
    # to write_dac.

    # To calculate the voltage we get out, we use this formula from the
    # datasheet: V_out = (d / 256) * 2.048


    d = 0x000
    spi.write_dac(chan, d);
    # V_out = 0 / 256 * 2.048 (gives 0)
    print "Your meter should read about 0V"
    raw_input ("When ready hit enter.")

    d = 0x400
    spi.write_dac(chan, d);
    # V_out = 64 / 256 * 2.048 (gives 0.512)
    print "Your meter should read about 0.5V"
    raw_input ("When ready hit enter.")

    d = 0x7F0
    spi.write_dac(chan, d);
    # V_out = 127 / 256 * 2.048 (gives 1.016)
    print "Your meter should read about 1.02V"
    raw_input ("When ready hit enter.")

    d = 0xAA0
    spi.write_dac(chan, d);
    # V_out = 170 / 256 * 2.048 (gives 1.36)
    print "Your meter should read about 1.36V"
    raw_input ("When ready hit enter.")
  
    d = 0xFF0
    spi.write_dac(chan, d);
    # V_out = 255 / 256 * 2.048 (gives 2.04)
    print "Your meter should read about 2.04V"
    raw_input ("When ready hit enter.")
  

if __name__ == '__main__':
    main()

