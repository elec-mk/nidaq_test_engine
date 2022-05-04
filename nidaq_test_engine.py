import time
import nidaqmx
from nidaqmx import system

import yaml
# from nidaqmx import system

with open('scripts/test.yaml', 'r') as f_yml:
    config = yaml.safe_load(f_yml)
    dvc = config['setup']['device']
    pinmap = config['setup']['pins']




sys = system.System.local()
print(f'driver version: {sys.driver_version.major_version}.{sys.driver_version.minor_version}.{sys.driver_version.update_version}')

print('searching for devices:')
for device in sys.devices:
    if device.name == config['setup']['device']:
        dev = device
        print(f'   -{device.name}*')
    else:
        print(f'   -{device.name}')
    # else
# for

print('analog input channels:')
for channel in dev.ai_physical_chans.channel_names:
    print(f'   - {channel}')
print('analog output channels:')
for channel in dev.ao_physical_chans.channel_names:
    print(f'   - {channel}')

print('digital input ports:')
for channel in dev.di_ports.channel_names:
    print(f'   - {channel}')
print('digital input lines:')
for channel in dev.di_lines.channel_names:
    print(f'   - {channel}')

print('digital output ports:')
for channel in dev.do_ports.channel_names:
    print(f'   - {channel}')
print('digital output lines:')
for channel in dev.do_lines.channel_names:
    print(f'   - {channel}')



for step in config['steps']:
    if step['type'] == 'print':
        print(step['input'])
    if step['type'] == 'ni_do':
        with nidaqmx.Task() as task:
            pin_alias = step['input']['pin']
            pin_device = f'{dvc}{pinmap[pin_alias]}'
            pin_value = step['input']['val']
            task.do_channels.add_do_chan(pin_device)
            task.write(pin_value, auto_start=True)
    if step['type'] == 'ni_di':
        with nidaqmx.Task() as task:
            pin_alias = step['input']['pin']
            pin_device = f'{dvc}{pinmap[pin_alias]}'
            pin_value = step['input']['val']
            task.di_channels.add_di_chan(pin_device)
            if(task.read() == pin_value):
                print('Success!')
            else:
                print('Failed!')
            # else
        # with
    # for
# EOF
