#!/usr/bin/env python3

import socket
import time
from bottle import Bottle, run, template, request, redirect, static_file
import os
import serial as pys
from srthread import Thread
import pydude


SERDEV = '/dev/ttyUSB0'
BOD = 9600

ser = pys.Serial(SERDEV, BOD)
app = Bottle()

serial_data = b''
prog_data = ''

@app.route('/')
def main():
    return template('view')

#@route('/download/<filename:path>')
#def download(filename):

#@app.route('/')

@app.route('/upload', method='POST')
def upload():
    global prog_data
    #category   = request.forms.get('category')
    postdata = request.params

    fus = request.forms.get("program_fuses")
    #print('fuses', fus)
    if fus == 'true':
        print('program fuses')
        low = '0x' + postdata['low_fuses']
        high = '0x' + postdata['high_fuses']
        ext = '0x' + postdata['ext_fuses']
        err = pydude.setfuses(low, high, ext)
        print(low, high, ext)
        #pydude.reprint(err)
        prog_data = err
    #print('#################### data received ####################')
    #for data in postdata:
    #    print(data, postdata[data])
    #print('#######################################################')
    upload_req = request.files.get('upload')
    if upload_req != None:
        #postdata['upload'] == 'Upload' and 
        name, ext = os.path.splitext(upload_req.filename)
        if ext != '.hex' :
            return 'File extension not allowed.'
        
        print('uploading file: ', name)
        fpath = './firmware.hex'
        with open(fpath, 'wb') as open_file:
            open_file.write(upload_req.file.read())

        erase = request.forms.get("erase")
        print('-------------- ',erase, '--------------')
        if erase  == 'true':
            err = pydude.write_flash(fpath, erase = True)
        else:
            err = pydude.write_flash(fpath)
            
        prog_data = err
    elif request.forms.get("download")  == 'Read':
        pydude.read()
        return static_file('flash.hex', root='./', download='flash.hex')
        print('reading a file')
    elif request.forms.get('lock_read') == 'Lock read':
        err = pydude.lock_read()
        print('lock bits written')
        prog_data = err
        
    return redirect("/")


@app.route('/clear', method='GET')
def clear():
    global serial_data
    global ser
    serial_data = b''
    ser = pys.Serial(SERDEV, BOD)
    return redirect('/')

@app.route('/serial', method='GET')
def get_serial_data():
    return serial_data

@app.route('/program', method='GET')
def get_serial_data():
    print(prog_data)
    return prog_data


@app.route('/serial/<filepath:path>')
def serial_json(filepath):
    return static_file(filepath, root = '/serial/')

@app.route('/static/<filepath:path>')
def static_js(filepath):
    return static_file(filepath, root='./static/')

@Thread()
def readSerial():
    while True:
        global serial_data
        rec =  ser.read()
        #rec = str(ser.readline().strip())[2:-1]+'\n'
        serial_data += rec
        print(rec)

run(app, host='0.0.0.0', port=6886, debag = True)



