#! /usr/bin/env python

# W. Greathouse - 1-Feb-2013

# Simple conversion of Gert's C code to Python for SPI access to DAC and ADC
# using spidev

#       Python code derived from examining dad.c
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
    print "These are the connections for the digital to analogue to digital test:"
    print "jumper connecting GP11 to SCLK"
    print "jumper connecting GP10 to MOSI"
    print "jumper connecting GP9 to MISO"
    print "jumper connecting GP8 to CSnA"
    print "jumper connecting GP7 to CSnB"
    print "jumper connecting DA1 on J29 to AD0 on J28"
    raw_input ("When ready hit enter.")


    # enable and access SPI
    spi = gb_spi.gb_spi()
    spi.setup_spi()

    # The value returned by the A to D can jump around quite a bit, so 
    # simply printing out the value isn't very useful. The bar graph
    # is better because this hides the noise in the signal.

    print "dig ana"

    # repeated write followed by read
    # from 0 to 256 stepping by 32
    for d in range(0,256+1,32):
        if d == 256:
            dac_val = 255 * 16
        else:
            dac_val = d * 16
        spi.write_dac(1, dac_val)
        time.sleep(0.01)    # allow output to settle (10 ms)
        v = spi.read_adc(0)
        # v should be in range 0-1023
        # map to 0-63
        s = v >> 4
        print "%3x %04d" % ( dac_val, v ) , 

        # show horizontal bar (repeated '#' characters, then spaces)
        print "#" * s,
        print " " * (64-s)

    # repeated write followed by read
    # from 224 down to 0 stepping by -32
    for d in range(224,0-1,-32):
        dac_val = d * 16
        spi.write_dac(1, dac_val)
        time.sleep(0.01)
        v = spi.read_adc(0)
        # v should be in range 0-1023
        # map to 0-63
        s = v >> 4
        print "%3x %04d" % ( dac_val, v ) , 

        # show horizontal bar (repeated '#' characters, then spaces)
        print "#" * s,
        print " " * (64-s)

    print ""


if __name__ == '__main__':
    main()

