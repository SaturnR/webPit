#!/usr/bin/env python3.4

import socket
import time
from bottle import Bottle, run, template, request, redirect, static_file
import os
import serial as pys
from srthread import Thread
import pydude

ser = pys.Serial('/dev/ttyUSB0', 9600)
app = Bottle()

serial_data = ''
prog_data = ''

@app.route('/')
def main():
    return template('view')

@app.route('/upload', method='POST')
def do_upload():
    #category   = request.forms.get('category')
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext != '.hex' :
        return 'File extension not allowed.'

    print('downloading file: ', name)
    fpath = './firmware.hex'
    with open(fpath, 'wb') as open_file:
        open_file.write(upload.file.read())
    err = pydude.write_flash(fpath)
    global prog_data
    prog_data = err
    return redirect("/")


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
        serial_data += str(ser.readline().strip())[2:-1]+'\n'
        #print(serial_data)

run(app, host='0.0.0.0', port=6886, debag = False)

    

