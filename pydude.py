#!/usr/bin/env python3
from subprocess import Popen, PIPE

PROGRAM = 'avrdude'
PROGRAMMER = 'usbasp'



mcu = {}
programmer = {}


'''
-p <partno>: This is just to tell it what microcontroller its programming. For example, if you are programming an ATtiny2313, use attiny2313 as the partnumber
-b <baudrate>: This is for overriding the serial baud rate for programmers like the STK500. Don't use this switch, the default is correct.
-B <bitrate>: This is for changing the bitrate, which is how fast the programmer talks to the chip. If your chip is being clocked very slowly you'll need to talk slowly to it to let it keep up. It'll be discussed later, for now don't use it.
-C <config-file>: The config file tells avrdude about all the different ways it can talk to the programmer. Theres a default configuration file, so lets just use that: don't use this command switch
-c <programmer>: Here is where we specify the programmer type, if you're using an STK500 use stk500, if you're using a DT006 programmer use dt006, etc.
-D: This disables erasing the chip before programming. We don't want that so don't use this command switch.
-P <port>: This is the communication port to use to talk to the programmer. It might be COM1 for serial or LPT1 for parallel or USB for, well, USB.
-F: This overrides the signature check to make sure the chip you think you're programming is. The test is strongly recommended as it tests the connection, so don't use this switch.
-e: This erases the chip, in general we don't use this because we auto-erase the flash before programming.
-U <memtype>:r|w|v:<filename>[:format]: OK this one is the important command. Its the one that actually does the programming. The <memtype> is either flash or eeprom (or hfuse, lfuse or efuse for the chip configuration fuses, but we aren't going to mess with those). the r|w|v means you can use r (read) w (write) or v (verify) as the command. The <filename> is, well, the file that you want to write to or read from. and [:format] means theres an optional format flag. We will always be using "Intel Hex" format, so use i
So, for example. If you wanted to write the file test.hex to the flash memory, you would use -U flash:w:test.hex:i. If you wanted to read the eeprom memory into the file "eedump.hex" you would use -U eeprom:r:eedump.hex:i
-n: This means you don't actually write anything, its good if you want to make sure you don't send any other commands that could damage the chip, sort of a 'safety lock'.
-V: This turns off the auto-verify when writing. We want to verify when we write to flash so don't use this.
-u: If you want to modify the fuse bits, use this switch to tell it you really mean it.
-t: This is a 'terminal' mode where you can type out commands in a row. Don't use this, it is confusing to beginners.
-E: This lists some programmer specifications, don't use it.
-v: This gives you 'verbose' output...in case you want to debug something. If you want you can use it, but in general we won't.
-q: This is the opposite of the above, makes less output. In general we won't use it but maybe after a while you wold like to.
The ones you'll use 99% of the time are highlighted in red. Let's review them in more detail
'''


class Fuses():

    '''
    CKDIV8 = False # Divide clock by 8
    OCDEN = False # Enable OCD
    CKOUT = False # Clock output
    JTAGEN = False # Enable JTAG
    SUT1 = False # Select start-up time
    SPIEN = True # Enable Serial programming and Data Downloading
    SUT0 = False # Select start-up time
    WDTON = False # Watchdog timer always on
    CKSEL3 = False # Select Clock Source
    EESAVE = False # EEPROM memory is preserved through chip erase
    CKSEL2 = False # Select Clock Source
    BOOTSZ1 = False # Select Boot Size
    BODLEVEL2 = False # Brown-out Detector trigger level
    CKSEL1 = False # Select Clock Source
    BOOTSZ0 = False # Select Boot Size
    BODLEVEL1 = False # Brown-out Detector trigger level
    CKSEL0 = False # Select Clock Source
    BOOTRST = False # Select Reset Vector
    BODLEVEL0 = False # Brown-out Detector trigger level
    '''

    def __init__(self,
                 CKDIV8 = False, OCDEN = False, CKOUT = False, JTAGEN = False, SUT1 = False,
                 SPIEN = True, SUT0 = False,  WDTON = False,  EESAVE = False, BOOTSZ0 = True, BOOTSZ1 = True,
                 CKSEL0 = False, CKSEL1 = False, CKSEL2 = False, CKSEL3 = False,
                 BOOTRST = True, BODLEVEL0 = False, BODLEVEL1 = False, BODLEVEL2 = False):

        # default 
        # SPIEN = True, BOOTSZ0 = True, BOOTSZ1 = True, BOOTRST = True,
        
        
        #EXTENDED = 0xFF (valid)
        #HIGH = 0xD8 (modified)
        #LOW = 0xEF (modified)

        self.CKDIV8 = CKDIV8
        self.CKOUT = CKOUT   
        self.SUT1 = SUT1
        self.SUT0 =  SUT0
        self.CKSEL3 = CKSEL3 
        self.CKSEL2 = CKSEL2
        self.CKSEL1 = CKSEL1
        self.CKSEL0 = CKSEL0  

        self.OCDEN = OCDEN
        self.JTAGEN = JTAGEN
        self.SPIEN = SPIEN   
        self.WDTON = WDTON
        self.EESAVE = EESAVE
        self.BOOTSZ1 = BOOTSZ1
        self.BOOTSZ0 = BOOTSZ0
        self.BOOTRST = BOOTRST
        
        self.BODLEVEL2 = BODLEVEL2
        self.BODLEVEL1 = BODLEVEL1
        self.BODLEVEL0 = BODLEVEL0


        self.Low = ((self.CKDIV8 << 7) + (self.CKOUT << 6) + (self.SUT1 << 5) + (self.SUT0 << 4) +\
        (self.CKSEL3 << 3) + (self.CKSEL2 << 2) + (self.CKSEL1 << 1) + self.CKSEL0)^0xFF
        
        self.High = ((self.OCDEN << 7) + (self.JTAGEN << 6) + (self.SPIEN << 5) + (self.WDTON << 4) + (self.EESAVE << 3) +\
        (self.BOOTSZ1 << 2) + (self.BOOTSZ0 << 1) + self.BOOTRST)^0xFF
    
        self.Ext = ((self.BODLEVEL2 << 3) + (self.BODLEVEL1 << 2) + (self.BODLEVEL0 << 1))^0xFF

        

        self.fdata = '-U lfuse:w:{}:m -U hfuse:w:{}:m -U efuse:w:{}:m'.format(hex(self.Low), hex(self.High), hex(self.Ext))

        
    def read(self):
        process = Popen(['avrdude', '-c', 'usbasp', '-p', 'm644p', '-v', '-u', '-U', 'lfuse:r:-:h', '-U', 'hfuse:r:-:h', '-U', 'efuse:r:-:h' ], stdout = PIPE)
        a = process.stdout.read()
        data = str(a)[2:-1].split('\\n')
        print('low {}, high {}, ext {} '.format(data[0], data[1], data[2])) 

        # save to file
        # -U  lfuse:r:low_fuse_val.hex:h -U hfuse:r:high_fuse_val.hex:h
        
    def write(self):
        print(self.fdata, '\n'*10)
        process = Popen(['avrdude', '-c', 'usbasp', '-p', 'm644p', '-v', '-e', '-u', '-U', self.fdata], stderr = PIPE)
        out, err = process.communicate()
        exit_code = process.wait()
        return err
    

    def verbose(self, low, high, ext):
        CKDIV8 = low >> 7 
        CKOUT  = (low >> 6) & 1  
        SUT1 = (low >> 5) & 1
        SUT0 = (low >> 4) & 1
        CKSEL3 = (low >> 3) & 1
        CKSEL2 = (low >> 2) & 1
        CKSEL1 = (low >> 1) & 1
        CKSEL0 = low & 1
        print('CKDIV8={}, CKOUT={}, SUT1={}, SUT0={}, CKSEL3={}, CKSEL2={}, CKSEL1={}, CKSEL0={}'.format(CKDIV8, CKOUT, SUT1, SUT0, CKSEL3, CKSEL2, CKSEL1, CKSEL0))
        
        OCDEN = high >> 7 
        JTAGEN = (high >> 6) & 1  
        SPIEN = (high >> 5) & 1
        WDTON = (high >> 4) & 1
        EESAVE  = (high >> 3) & 1
        BOOTSZ1 = (high >> 2) & 1
        BOOTSZ0 = (high >> 1) & 1
        BOOTRST = high & 1        
        print('OCDEN={}, JTAGEN={}, SPIEN={}, WDTON={}, EESAVE={}, BOOTSZ1={}, BOOTSZ0={}, BOOTRST={}'.format(OCDEN, JTAGEN, SPIEN, WDTON, EESAVE, BOOTSZ1, BOOTSZ0, BOOTRST))

        BODLEVEL2 = (ext >> 2) & 1
        BODLEVEL1 = (ext >> 1) & 1
        BODLEVEL0 = ext & 1
        print('BODLEVEL2={}, BODLEVEL1={}, BODLEVEL0={}'.format(BODLEVEL2, BODLEVEL1, BODLEVEL0))
        
        
        
def write_flash(hex_file = 'BankSecurity.hex', mcu = 'm644p', erase = False):
    args = ['-c', PROGRAMMER, '-p', mcu]
    
    if not erase :
        args+=['-D']
        
    prog = 'flash:w:'+hex_file
    print([PROGRAM]+args+['-U']+[prog])
    process = Popen([PROGRAM]+args+['-U']+[prog], stderr = PIPE)
    out, err = process.communicate()
    exit_code = process.wait()
    return err


def write_eeprom():
    pass

def write_fuses():
    pass


def config_bootloader(mcu = 'm644p'):
    s = '-v -e -U efuse:w:0xFF:m -U hfuse:w:0xD8:m -U lfuse:w:0xEF:m'
    rs = s.split(' ')
    args = ['-c', PROGRAMMER, '-p', mcu, *rs]
    
    process = Popen([PROGRAM]+args, stderr = PIPE)
    out, err = process.communicate()
    exit_code = process.wait()
    return err


def write_bootloader(hex_file = 'GprsBootloader.hex', mcu = 'm644p'):
    s = '-v -U flash:w:' + hex_file
    #     s = '-v -e -U flash:w:' + hex_file
    rs = s.split(' ')
    args = ['-c', PROGRAMMER, '-p', mcu, *rs]
    
    process = Popen([PROGRAM]+args+[hex_file], stderr = PIPE)
    out, err = process.communicate()
    exit_code = process.wait()
    return err
    
def read(format = 'hex'):
    f = 'r'
    if format == 'hex':
        f = 'i'
    elif format == 'bin':
        f = 'r'
    
    s = 'avrdude -c usbasp -p m644p -v -U flash:r:flash.'+format+':'+f
    
    process = Popen(s.split(), stderr = PIPE)
    out, err = process.communicate()
    exit_code = process.wait()
    return err
    

def reprint(data):
    for n in data.split(b'\n'):
        print(n)


def setfuses(low = '0xEF', high = '0xD8', ext = '0xFF'):
    process = Popen(['avrdude', '-c', 'usbasp', '-p', 'm644p', '-v', '-e', '-u', '-U',
                     'efuse:w:{}:m'.format(ext), '-U', 'hfuse:w:{}:m'.format(high), '-U', 'lfuse:w:{}:m'.format(low)], stderr = PIPE)
    out, err = process.communicate()
    exit_code = process.wait()
    print('efuse:w:{}:m'.format(ext), '-U', 'hfuse:w:{}:m'.format(high), '-U', 'lfuse:w:{}:m'.format(low))
    return err

    
def boot():
    process = Popen(['avrdude', '-c', 'usbasp', '-p', 'm644p', '-v', '-U','flash:w:GprsBootloader.hex'], stderr = PIPE)
    out, err = process.communicate()
    exit_code = process.wait()
    return err

def flash():
    process = Popen(['avrdude', '-c', 'usbasp', '-p', 'm644p', '-v','-D', '-U', 'flash:w:BankSecurity.hex'], stderr = PIPE)
    out, err = process.communicate()
    exit_code = process.wait()
    return err
