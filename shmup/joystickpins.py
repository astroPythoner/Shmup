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
            },
            "PLAYSTATION(R)3 Controller" : {
                "A"         : 13,   # circle
                "B"         : 14,   # cross
                "X"         : 12,   # triangle
                "Y"         : 15,   # square
                "SELECT"    : 0,
                "START"     : 3,
                "SH_LEFT"   : 10,   # L1
                "SH_RIGHT"  : 11,   # R1
                "AXIS_X"    : 0,  # -1 = links, +1 = rechts
                "AXIS_Y"    : 1   # -1 = oben,  +1 = unten
            },
        }

class JoystickPins():
    def __init__(self, joystick, mapping = None):
        self.joystick = joystick
        self.name = joystick.get_name().strip()
        if mapping is not None:
            self.mapping = mapping
        elif self.name in joystick_mappings.keys():
            self.mapping = joystick_mappings[self.name]
        else:
            self.mapping = {}
        self._A = self.mapping.get("A")
        self._B = self.mapping.get("B")
        self._X = self.mapping.get("X")
        self._Y = self.mapping.get("Y")
        self._select = self.mapping.get("SELECT")
        self._start  = self.mapping.get("START")
        self._shoulder_left  = self.mapping.get("SH_LEFT")
        self._shoulder_right = self.mapping.get("SH_RIGHT")
        self._axis_x = self.mapping.get("AXIS_X")
        self._axis_y = self.mapping.get("AXIS_Y")

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

    def get_A(self):
        return self.joystick.get_button(self.A)
    def get_B(self):
        return self.joystick.get_button(self.B)
    def get_X(self):
        return self.joystick.get_button(self.X)
    def get_Y(self):
        return self.joystick.get_button(self.Y)
    def get_select(self):
        return self.joystick.get_button(self._select)
    def get_start(self):
        return self.joystick.get_button(self._start)
    def get_shoulder_left(self):
        return self.joystick.get_button(self._shoulder_left)
    def get_shoulder_right(self):
        return self.joystick.get_button(self._shoulder_right)
    def get_axis_left(self):
        return self.joystick.get_axis(self._axis_x) < -0.9
    def get_axis_right(self):
        return self.joystick.get_axis(self._axis_x) >  0.9
    def get_axis_up(self):
        return self.joystick.get_axis(self._axis_y) < -0.9
    def get_axis_down(self):
        return self.joystick.get_axis(self._axis_y) >  0.9
