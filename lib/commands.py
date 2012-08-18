import struct

class DroneCommand(object):
    def __init__(self):
        self.cmd = None 
        self.params = []
        self.seq = 0
     
    @staticmethod
    def f2i(f):
        return struct.unpack('i', struct.pack('f', f))[0]

    def set_seq(self, seq):
        self.seq = seq

    def __str__(self):
        param_string = ''
        for param in self.params:
            param_string += {
                int: lambda p: "," + str(p),
                float: lambda p: "," + str(DroneCommand.f2i(p)),
                str: lambda p: ',"' + p + '"'
            }[type(param)](param)

        msg = "AT*%s=%i%s\r" % (self.cmd, self.seq, param_string)

        return msg

class RefCommand(DroneCommand):
    def __init__(self, takeoff, emergency=False):
        DroneCommand.__init__(self)
        self.cmd = "REF"
        p = 0b10001010101000000000000000000

        if takeoff:
            p += 0b1000000000
        if emergency:
            p += 0b010000000

        self.params.append(p)

class ProgressCommand(DroneCommand):
    def __init__(self, progressive, lr, rb, vv, va):
        DroneCommand.__init__(self)
        self.cmd = "PCMD"

        p = 1 if progressive else 0
        self.params.extend([p, float(lr), float(rb), float(vv), float(va)])

class HoverCommand(ProgressCommand):
    def __init__(self):
        ProgressCommand.__init__(self, False, 0, 0, 0, 0)

class FTrimCommand(DroneCommand):
    def __init__(self):
        DroneCommand.__init__(self)
        self.cmd = "FTRIM"

class ZapCommand(DroneCommand):
    def __init__(self, stream):
        DroneCommand.__init__(self)
        self.cmd = "ZAP"
        self.params.append(stream)

class ConfigCommand(DroneCommand):
    def __init__(self, option, value):
        DroneCommand.__init__(self)
        self.cmd = "CONFIG"
        self.params.extend([str(option), str(value)])

class ComWdgCommand(DroneCommand):
    def __init__(self):
        DroneCommand.__init__(self)
        self.cmd = "COMWDG"

class AFlightCommand(DroneCommand):
    def __init__(self, start=True):
        DroneCommand.__init__(self)
        self.cmd = "AFLIGHT"
        self.params.append(1 if start else 0)

class AnimCommand(DroneCommand):
    def __init__(self, anim, d):
        DroneCommand.__init__(self)
        self.cmd = "ANIM"
        self.params.extend([anim, d])
