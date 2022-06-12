import nidaqmx
from nidaqmx import system

import logging

def get_nidaq_devices():
    """prints a list of available nidaq devices to the terminal
    """
    print('available nidaq devices:')
    for device in system.System.local().devices:
        print(device.name)

        print('analog inputs:')
        for channel in device.ai_physical_chans.channel_names:
            print(f'   - {channel}')
        print('analog outputs:')
        for channel in device.ao_physical_chans.channel_names:
            print(f'   - {channel}')
        print('digital io:')
        for channel in device.di_lines.channel_names:
            print(f'   - {channel}')

    # for
# def

class nidaq:
    def __init__(self, config):
        logging.basicConfig(format='%(name)s:%(levelname)s:%(message)s', level=logging.INFO)
        self.logger = logging.getLogger('nidaq')
        self.device = config['device']

        self.sys = system.System.local()
        self.driver = f'{self.sys.driver_version.major_version}.{self.sys.driver_version.minor_version}.{self.sys.driver_version.update_version}'

        self.logger.info(f'nidaq device {self.device}')
        self.logger.info(f'nidaqmx driver {self.driver}')

    # def

    def set_digital_out(self, pins, value):
        with nidaqmx.Task() as task:
            self.logger.info(f'setting {self.device} digital output {pins} value : {value}')
            task.do_channels.add_do_chan(f'{self.device}/{pins}')
            task.write(value, auto_start=True)
        # with
    # def

    def get_digital_in(self, pins):
        with nidaqmx.Task() as task:
            task.di_channels.add_di_chan(f'{self.device}/{pins}')
            pin_val = task.read()
            self.logger.info(f'getting {self.device} digital input {pins} value : {pin_val}')
        return pin_val
    # def

    def set_analogue_out(self, pins, value):
        with nidaqmx.Task() as task:
            self.logger.info(f'setting {self.device} analogue output {pins} value : {value}')
            task.ao_channels.add_ao_voltage_chan(f'{self.device}/{pins}', max_val=5.0, min_val=0.0)
            task.write(value, auto_start=True)
        # with
    # def

    def get_analogue_in(self, pins):
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan(f'{self.device}/{pins}', max_val=5.0, min_val=0.0)
            pin_val = task.read()
            self.logger.info(f'getting {self.device} analogue input {pins} value : {pin_val}')
        return pin_val
    # def

# class

if __name__ == '__main__':
    get_nidaq_devices()

    dev1 = nidaq({'device':'Dev1'})
    dev1.set_analogue_out('ao0', 0.0)


    dev1.set_digital_out('port0', 0)

    dev1.get_digital_in('port0/line0')
    dev1.set_digital_out('port0/line1', True)
    dev1.get_digital_in('port0/line0')


    dev1.set_analogue_out('ao0', 2.5)
    dev1.get_analogue_in('ai0')
    dev1.set_analogue_out('ao1', [0.0,1.0,2.0,3.0,4.0,5.0,4.0,3.0,2.0,1.0,0.0])
