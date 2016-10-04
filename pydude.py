from subprocess import Popen, PIPE

PROGRAM = 'avrdude'
PROGRAMMER = 'usbasp'

def write_flash(hex_file, mcu = 'm644p'):
    
    args = ['-c', PROGRAMMER, '-p', mcu, '-u', '-U']
    prog = 'flash:w:'
    
    process = Popen([PROGRAM]+args+[hex_file], stderr = PIPE)
    out, err = process.communicate()
    exit_code = process.wait()
    return err

def write_eeprom():
    pass

def write_fuses():
    pass

def read():
    pass


