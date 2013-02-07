#! /usr/bin/env python

# W. Greathouse - 1-Feb-2013

# Simple conversion of Gert's C code to Python for SPI access to DAC and ADC
# using spidev

#       Python code derived from examining atod.c
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
#  Read ADC input 0 and show as horizontal bar
#
def main():
    while True:
        chan = raw_input ("Which channel do you want to test? Type 0 or 1. ")
        if (chan == '0' or chan == '1'):
            break;

    chan = ord(chan) - ord('0');

    print "jumper connecting GP11 to SCLK"
    print "jumper connecting GP10 to MOSI"
    print "jumper connecting GP9 to MISO"
    print "jumper connecting GP8 to CSnA"
    print "Potentiometer connections:"
    print "  (call 1 and 3 the ends of the resistor and 2 the wiper)"
    print "  connect 3 to 3V3"
    print "  connect 2 to AD%d" % chan
    print "  connect 1 to GND"
    raw_input ("When ready hit enter.")

    # enable and access SPI
    spi = gb_spi.gb_spi()
    spi.setup_spi()

    # The value returned by the A to D can jump around quite a bit, so 
    # simply printing out the value isn't very useful. The bar graph
    # is better because this hides the noise in the signal.

    # repeated read
    for r in range(100000):
        v = spi.read_adc(chan)
        # V should be in range 0-1023
        # map to 0-63
        s = v >> 4;
        print "\r%04d" % v , 
        # show horizontal bar (repeated '#' characters, then spaces)
        print "#" * s,
        print " " * (64-s),
        time.sleep(0.0001)   # short_wait() replacement (0.1ms)

    print ""


if __name__ == '__main__':
    main()

