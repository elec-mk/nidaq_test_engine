import nidaqmx
from nidaqmx import system

class nidaq:
    def __init__(self, config):
        self.device = config['device']

        self.sys = system.System.local()
        self.driver = f'{self.sys.driver_version.major_version}.{self.sys.driver_version.minor_version}.{self.sys.driver_version.update_version}'

    # def

    def get_available_devices(self):

        print('available nidaq devices:')
        for device in self.sys.devices:
            print(device)
        # for
    # def

    def set_digital_out(self, pins, value):
        with nidaqmx.Task() as task:
            pin_alias = step['input']['pin']
            pin_device = f'{self.device}\pins'
            pin_value = step['input']['val']
            task.do_channels.add_do_chan(pins)
            task.write(pin_value, auto_start=True)
        # with
    # def

    def get_digital_in(pins):

        pin_val
        return pin_val
# class
