import nidaqmx
from nidaqmx import system

import logging





class nidaq:
    def __init__(self, config):
        logging.basicConfig(format='%(name)s:%(levelname)s:%(message)s', level=logging.INFO)
        self.logger = logging.getLogger('nidaq')

        self.device = ''
        self.pins = {}

        self.sys = system.System.local()
        self.driver = f'{self.sys.driver_version.major_version}.{self.sys.driver_version.minor_version}.{self.sys.driver_version.update_version}'
        self.logger.info('nidaqmx driver %s', self.driver)


        self.load_config(config)
    # def

    @staticmethod
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

    def handle_test_step(self, step):
        step_type = step['type']
        step_pin = self.pins[step['param']['pin']]
        step_val = step['param']['val']


        if step_type == 'set_digital_out':
            self.set_digital_out(step_pin, step_val)
        elif step_type == 'get_digital_in':
            measured = self.get_digital_in(step_pin)
            if measured == step_val:
                self.logger.info('step passed')
            else:
                self.logger.error('step failed measured %s expected %s', measured, step_val)
            # else
        elif step_type == 'set_analog_out':
            pass
        elif step_type == 'get_analog_in':
            pass
        else:
            self.logger.error('Invalid test step for nidaq device : %s', step_type)
    # def

    def check_for_device(self, device):
        ret_val = True # default error
        if device in system.System.local().devices:
            ret_val = False
            self.logger.info('nidaq device %s found', device)
        else:
            self.logger.error('device not found %s', device)
        # else
        return ret_val
    # def

    def check_for_pins(self, pins):
        ret_val = True
        device = self.sys.local().devices[self.device]
        # validate pins are valid
        device_pins = []
        device_pins.extend(device.ai_physical_chans.channel_names)
        device_pins.extend(device.ao_physical_chans.channel_names)
        device_pins.extend(device.di_ports.channel_names)
        device_pins.extend(device.di_lines.channel_names)
        device_pins.extend(device.do_ports.channel_names)
        device_pins.extend(device.do_lines.channel_names)
        device_pins.extend(device.ci_physical_chans.channel_names)
        device_pins.extend(device.co_physical_chans.channel_names)
        new_pin = []
        for pin in device_pins:
            new_pin.append(pin.replace(f'{self.device}/',''))

        device_pins = new_pin

        for pin in pins:
            try:
                device_pins.index(pins[pin])
                ret_val = False
            except ValueError:
                self.logger.error("couldn't find %s in list of available pins for %s", pin, self.device)
                ret_val = True
                break
            # if
        # for
        return ret_val
    # def


    def load_config(self, config):
        # is try/except necessary?
        if isinstance(config, dict):
            # sanity check that the expected device exists/is attached to system
            if 'device' in config and isinstance(config['device'], str):

                if self.check_for_device(config['device']):
                    raise Exception('Could not find device specified in config')
                else:
                    self.device =config['device']
            else:
                self.logger.error('No device field found in config')
            # else

            if 'pins' in config and isinstance(config['pins'], dict):
                if self.check_for_pins(config['pins']):
                    raise Exception('Could not find pin(s) specified in config')
                else:
                    self.pins = config['pins'].copy()
            else:
                self.logger.error('No pins field found in config')
            # else
        # if
    # def


    def set_digital_out(self, pins, value):
        with nidaqmx.Task() as task:
            self.logger.info('setting %s digital output %s value : %d', self.device, pins, value)
            task.do_channels.add_do_chan(f'{self.device}/{pins}')
            task.write(value, auto_start=True)
        # with
    # def

    def get_digital_in(self, pins):
        with nidaqmx.Task() as task:
            task.di_channels.add_di_chan(f'{self.device}/{pins}')
            pin_val = task.read()
            self.logger.info('getting %s digital input %s value : %d', self.device, pins, pin_val)
        return pin_val
    # def

    def set_analogue_out(self, pins, value):
        with nidaqmx.Task() as task:
            self.logger.info(f'setting {self.device} analogue output {pins} value : {value}')
            task.ao_channels.add_ao_voltage_chan(f'{self.device}/{pins}', max_val=5.0, min_val=0.0)
            task.write(value, auto_start=True)
        # with
    # def

    def get_analogue_in(self, pins, samples=1):
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan(f'{self.device}/{pins}', max_val=5.0, min_val=0.0)
            pin_val = task.read(number_of_samples_per_channel=samples)
            self.logger.info(f'getting {self.device} analogue input {pins} value : {pin_val}')
        return pin_val
    # def

    def get_analogue_stream(self, pins='ai0', samples=1):
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan(f'{self.device}/{pins}', max_val=5.0, min_val=0.0)
            in_stream = task.in_stream
            pin_val = in_stream.read(number_of_samples_per_channel=samples)
            self.logger.info(f'getting {self.device} analogue input stream - pins:{pins} - samples:{samples} - value:{pin_val}')
        return pin_val
    # def

# class

if __name__ == '__main__':
    nidaq.get_nidaq_devices()

    dev1 = nidaq({'device':'Dev1', 'pins':{'do_test': 'port0/line0', 'di_test':'port0/line1', 'ao_test':'ao0', 'ai_test':'ai0'}})
    test_step = {'id':2, 'desc':'set dout_1 high', 'device': 'nidaq', 'type':'set_digital_out', 'param':{'pin':'do_test', 'val':True}}


    dev1.handle_test_step(test_step)
    dev1.set_analogue_out('ao0', 0.0)


    dev1.set_digital_out('port0', 0)

    dev1.get_digital_in('port0/line0')
    dev1.set_digital_out('port0/line1', True)
    dev1.get_digital_in('port0/line0')


    dev1.set_analogue_out('ao0', 2.5)
    dev1.get_analogue_in('ai0')
    dev1.get_analogue_stream('ai0')
    dev1.set_analogue_out('ao0', 5.0)

    dev1.get_analogue_in('ai0', 2)
    dev1.get_analogue_stream('ai0', 2)

    dev1.set_analogue_out('ao1', [0.0,1.0,2.0,3.0,4.0,5.0,4.0,3.0,2.0,1.0,0.0])
# if
