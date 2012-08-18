from commands import *
import threading
import socket
from functools import wraps
import time

ARDRONE_NAVDATA_PORT = 5554
ARDRONE_VIDEO_PORT = 5555
ARDRONE_COMMAND_PORT = 5556
ARDRONE_IP = "192.168.1.1"

COMWDG_INTERVAL = 0.2

DEBUG = True

def send(fn):
    def net_send(res, self):
        res.set_seq(self.seq)
        self.comwdg_timer.cancel()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(str(res), (ARDRONE_IP, ARDRONE_COMMAND_PORT))
        self.comwdg_timer = threading.Timer(COMWDG_INTERVAL, self.comwdg)
        self.comwdg_timer.start()
        self.seq += 1

        if DEBUG:
            print res
 
    @wraps(fn)
    def wrapper(*args, **kw):
        self = args[0]

        res = fn(*args, **kw)

        if type(res) == list:
            for i in res:
                net_send(i, self)
        else:
            net_send(res, self)

    return wrapper

class PyARDrone(object):
    def __init__(self):
        self.seq = 1
        self._speed = 0.2

        self.comwdg_timer = threading.Timer(COMWDG_INTERVAL, self.comwdg)
        self.comwdg()

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, val):
        if val < 0 or val > 1: 
            raise ValueError("Speed must be in the 0..1 range")
        self._speed = val
         
    @send
    def comwdg(self):
        return ComWdgCommand() 

    @send
    def takeoff(self):
        return [FTrimCommand(), ConfigCommand("control:altitude_max", 2000), RefCommand(True)]

    @send
    def reset(self):
        return [RefCommand(False, False), RefCommand(False, True)]

    @send
    def land(self):
        return RefCommand(False)

    @send
    def hover(self):
        return HoverCommand()

    @send
    def move_left(self):
        return ProgressCommand(True, -self.speed, 0, 0, 0)

    @send
    def move_right(self):
        return ProgressCommand(True, self.speed, 0, 0, 0)

    @send
    def move_up(self):
        return ProgressCommand(True, 0, 0, self.speed, 0)

    @send
    def move_down(self):
        return ProgressCommand(True, 0, 0, -self.speed, 0)

    @send
    def move_forward(self):
        return ProgressCommand(True, 0, -self.speed, 0, 0)

    @send
    def move_backward(self):
        return ProgressCommand(True, 0, self.speed, 0, 0)

    @send
    def turn_left(self):
        return ProgressCommand(True, 0, 0, 0, -self.speed)

    @send 
    def turn_right(self):
        return ProgressCommand(True, 0, 0, 0, self.speed)
