from pygame import joystick

#Pins-Mapping: (A, B, X, Y, SELECT, START, SHOULDER_LEFT, SHOULDER_RIGHT, AXIS_X, AXIS_Y)
joystick_mappings = {
            "USB Gamepad" :       {
                "A"         : 1,
                "B"         : 2,
                "X"         : 0,
                "Y"         : 3,
                "SELECT"    : 8,
                "START"     : 9,
                "SH_LEFT"   : 4,
                "SH_RIGHT"  : 5,
                "AXIS_X"    : 3,
                "AXIS_Y"    : 4
            },
            "GPIO Controller 1" : {
                "A"         : 0,
                "B"         : 1,
                "X"         : 3,
                "Y"         : 4,
                "SELECT"    : 10,
                "START"     : 11,
                "SH_LEFT"   : 7,
                "SH_RIGHT"  : 6,
                "AXIS_X"    : 0,  # -1 = links, +1 = rechts
                "AXIS_Y"    : 1   # -1 = oben,  +1 = unten
            }
        }

class JoystickPins():
    def __init__(self, joystick, mapping: None):
        self.joystick = joystick
        self.name = joystick.get_name()
        if mapping is not None:
            self.mapping = mapping
        else:
            self.mapping = joystick_mappings[self.name]
        self._A = mapping["A"]
        self._B = mapping["B"]
        self._X = mapping["X"]
        self._Y = mapping["Y"]
        self._select = mapping["SELECT"]
        self._start  = mapping["START"]
        self._shoulder_left  = mapping["SH_LEFT"]
        self._shoulder_right = mapping["SH_RIGHT"]
        self._axis_x = mapping["AXIS_X"]
        self._axis_y = mapping["AXIS_Y"]

    def A(self):
        return self._A
    def B(self):
        return self._B
    def X(self):
        return self._X
    def Y(self):
        return self._Y
    def select(self):
        return self._select
    def start(self):
        return self._start
    def shoulder_left(self):
        return self._shoulder_left
    def shoulder_right(self):
        return self._shoulder_right
    def axis_x(self):
        return self._axis_x
    def axis_y(self):
        return self._axis_y
