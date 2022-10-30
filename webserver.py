#!/usr/bin/env python3

import socket
import time
from bottle import Bottle, run, template, request, redirect, static_file
import os
import serial as pys
from srthread import Thread
import pydude
import json
import sys
from google_api import file_api

if len(sys.argv) > 1:
    SERDEV = sys.argv[1]
else:
    SERDEV = '/dev/ttyUSB1'

#57600 #9600 #38400 #115200 #9600
BOD = 115200

selected_mcu = "m644p"

ser = None
app = Bottle()


def init_serial():
    global ser
    try:
        ser = pys.Serial(SERDEV, BOD)
    except pys.serialutil.SerialException as ser_ex:
        print(ser_ex)


serial_data = b''
prog_data = ''


@app.route('/')
def main():
    return template('view', request=request)


@app.route('/upload', method='POST')
def upload():
    global prog_data
    # category   = request.forms.get('category')
    postdata = request.params

    fus = request.forms.get("program_fuses")
    mcu = request.forms.get("mcu")
    print(f'SLECTED MCU: {mcu}')

    if fus == 'true':
        print('program fuses')
        low = '0x' + postdata['low_fuses']
        high = '0x' + postdata['high_fuses']
        ext = '0x' + postdata['ext_fuses']
        err = pydude.setfuses(low, high, ext, mcu=mcu)
        print(low, high, ext)
        # pydude.reprint(err)
        prog_data = err
    upload_req = request.files.get('upload')
    if upload_req is not None:
        # postdata['upload'] == 'Upload' and
        name, ext = os.path.splitext(upload_req.filename)
        if ext != '.hex':
            return 'File extension not allowed.'

        print('uploading file: ', name)
        fpath = './firmware.hex'
        with open(fpath, 'wb') as open_file:
            open_file.write(upload_req.file.read())

        erase = request.forms.get("erase")
        print('-------------- ', erase, '--------------')
        if erase == 'true':
            err = pydude.write_flash(fpath, erase=True, mcu=mcu)
        else:
            err = pydude.write_flash(fpath, mcu=mcu)

        prog_data = err
    elif request.forms.get("download") == 'Read':
        pydude.read(mcu=mcu)
        return static_file('flash.hex', root='./', download='flash.hex')
        print('reading a file')
    elif request.forms.get('lock_read') == 'Lock read':
        err = pydude.lock_read(mcu=mcu)
        print('lock bits written')
        prog_data = err

    return redirect("/")


@app.route('/serialin')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    data = request.params.get('data')
    print(data)
    try:
        numbers = data.split(',')
        b = bytes([int(n) for n in numbers])
        ser.write(b)
    except Exception as ex:
        return json.dumps({'status': str(ex)})

    return json.dumps({'status': 'Send OK'})


@app.route('/clear', method='GET')
def clear():
    global serial_data
    global ser
    serial_data = b''
    if ser != None:
        ser = pys.Serial(SERDEV, BOD)
    return redirect('/')


@app.route('/program', method='GET')
def get_serial_data():
    print(prog_data)
    return prog_data


@app.route('/serial/<filepath:path>')
def serial_json(filepath):
    return static_file(filepath, root='/serial/')


@app.route('/static/<filepath:path>')
def static_js(filepath):
    return static_file(filepath, root='./static/')


@Thread()
def readSerial():
    while True:
        global serial_data
        if ser is not None:
            rec = ser.read()
            # rec = str(ser.readline().strip())[2:-1]+'\n'
            serial_data += rec
            print(rec)
        time.sleep(0.001)


if __name__ == "__main__":
    # file_api.Download()
    init_serial()
    run(app, host='127.0.0.1', port=6886, debag=True)
