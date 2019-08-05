#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-
# Created by kayrlas on Jul 18, 2019 (https://github.com/kayrlas)
# SerialComPythonCUI.py

import signal
import time
import threading

from serial import Serial
from serial.tools import list_ports


class SerialCom(object):
    """Class of serial communication"""
    def __init__(self):
        self.device = None        # select_comport()
        self.serial = None        # open_comport()
        self.thread_sread = None  # start_thread() for serial_read
        self.thread_swrite = None # start_thread() for serial_write

    def select_comport(self) -> bool:
        """Select comports from a list and save to self.device"""
        # making comports list
        _ports = list_ports.comports()
        _devices = [info for info in _ports]

        # select comport
        if len(_devices) == 0:
            # No device
            print("Device not found.")
            return False
        elif len(_devices) == 1:
            # Only one device
            print("Only found %s." % _devices[0])
            self.device = _devices[0].device
            return True
        else:
            # Some devices
            print("Connected comports are as follows:")
            for i in range(len(_devices)):
                print("%d : %s" % (i, _devices[i]))
            # Select device
            inp_num = input("Input the number of your target port >> ")
            if not inp_num.isdecimal():
                print("%s is not a number!" % inp_num)
                return False
            elif int(inp_num) in range(len(_devices)):
                self.device = _devices[int(inp_num)].device
                return True
            else:
                print("%s is out of the number!" % inp_num)
                return False

    def open_comport(self, baudrate, timeout) -> bool:
        """After select_comport, open the comport"""
        self.serial = Serial(baudrate=baudrate, timeout=timeout)

        if self.device is None:
            print("Device has not been specified yet! select_comport first.")
            return False
        else:
            self.serial.port = self.device

        inp_yn = input("Open %s ? [Yes/No] >> " % self.device).lower()
        if inp_yn in ["y", "yes"]:
            print("Opening...")
            try:
                self.serial.open()
            except Exception as e:
                print(e)
                return False
            else:
                return True
        elif inp_yn in ["n", "no"]:
            print("Canceled.")
            return False
        else:
            print("Oops, you didn't enter [Yes/No]. Please try again.")
            return False

    def serial_read(self):
        """Read line from serial port and print with time"""
        _format = "%Y/%m/%d %H:%M:%S"

        while self.serial.is_open:
            _t1 = time.strftime(_format, time.localtime())
            _recv_data = self.serial.readline()
            if _recv_data != b'':
                print(_t1 + " (RX) : " + _recv_data.strip().decode("utf-8"))
                time.sleep(1)

    def serial_write(self):
        """Write strings to serial port"""
        _format = "%Y/%m/%d %H:%M:%S"

        while self.serial.is_open:
            _t1 = time.strftime(_format, time.localtime())
            #_send_data = input(_t1 + " (TX) >> ")
            _send_data = input()
            self.serial.write(_send_data.encode("utf-8"))
            time.sleep(1)

    def start_thread(self):
        """Start serial communication thread"""
        self.thread_sread = threading.Thread(target=self.serial_read)
        self.thread_swrite = threading.Thread(target=self.serial_write)
        self.thread_sread.start()
        self.thread_swrite.start()

    def close_comport(self):
        self.serial.close()

    def stop_thread(self):
        self.thread_sread.join()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    com = SerialCom()

    if com.select_comport():
        if com.open_comport(9600, 0.1):
            com.start_thread()
