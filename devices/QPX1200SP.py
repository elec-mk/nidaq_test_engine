import serial


class QPX1200SP:
    def __init__(self, config):
        self.com_port = config['com_port']
        self.baud = config['baud']
        self.ser = serial.Serial(self.com_port, self.baud, timeout=1)

        self.ser.write(str.encode('*IDN?'))
        self.id = self.ser.readline()

        self.voltage_min = 0
        self.voltage_max = 60

        self.over_voltage = 0
        self.voltage = 0
        self.voltage_actual = 0

        self.current_min = 0
        self.current_max = 50

        self.over_current = 0
        self.current = 0
        self.current_actual = 0

    # def

    def set_voltage(self, voltage):

        self.voltage = self._check_within_bounds(voltage, self.voltage_min, self.voltage_max)

        self.ser.write(f'V1 {self.voltage}')
    # def

    def get_voltage(self):

        self.ser.write(f'V1?')
        self.voltage_actual = self.ser.readline()
    # def


    def _check_within_bounds(self, val, val_min, val_max):
        ret_val = 0

        if val <= val_min:
            ret_val = val_min
        elif val >= val_max:
            ret_val = val_max
        else:
            ret_val = val
        # else

        return ret_val
    # def
# class
