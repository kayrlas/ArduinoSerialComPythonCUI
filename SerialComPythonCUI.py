# coding:utf-8
# Copyright 2019 Kayrlas (https://github.com/kayrlas)


import time
import threading

import serial
from serial.tools import list_ports


# return port description of None
def select_comport():
    # making comports list
    ports = list_ports.comports()
    devices = [info.device for info in ports]

    # select comport
    if len(devices) == 0:
        print("Device not found.")
        return None
    elif len(devices) == 1:
        print("Only found %s" % devices[0])
        return devices[0]
    else:
        for i in range(len(devices)):
            print("%s : %d" % (devices[i], i))
        inp_num = int(input("Input the number of your target port >> "))
        if inp_num in range(len(devices)):
            return devices[inp_num]
        else:
            print("%s is out of the number" % inp_num)
            return None


# return True or False
def open_comport(ser):
    inp_yn = input("Connect [Y]es/[N]o? >> ").lower()

    if inp_yn in ["y", "yes"]:
        print("Connecting...")
        try:
            ser.open()
        except Exception as e:
            print(e)
            return False
        else:
            return True
    elif inp_yn in ["n", "no"]:
        print("Canceled.")
        return False
    else:
        print("Oops, you didn't enter [Y]es/[N]o. Please try again.")
        return False


def serial_read(ser):
    format = "%Y/%m/%d %H:%M:%S"

    while ser.is_open:
        t1 = time.strftime(format, time.localtime())
        recv_data = ser.readline()
        if recv_data != b'':
            print(t1 + " | " + recv_data.strip().decode("utf-8"))
        time.sleep(1)


def serial_write(ser):
    while ser.is_open:
        send_data = input()
        if send_data == "kill":
            ser.is_open = False
            break
        ser.write(send_data.encode("utf-8"))
        time.sleep(1)


def main():
    ser = serial.Serial(baudrate=9600, timeout=1.0)
    ser.port = select_comport()

    # exit main if serial.Serial.port is None
    if ser.port is None:
        return

    # exit main if port is still closed
    if not open_comport(ser):
        return

    print("If you want to disconnect, please input 'kill'")
    thread_sread = threading.Thread(target=serial_read, args=(ser, ))
    thread_swrite = threading.Thread(target=serial_write, args=(ser, ))

    thread_sread.start()
    thread_swrite.start()

    thread_sread.join()
    thread_swrite.join()

    ser.close()
    print("Disconnected.")
    return


if __name__ == "__main__":
    print("main start")

    main()

    print("main end")
