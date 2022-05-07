import time
import yaml
# local imports
from devices.nidaq import nidaq
from devices.QPX1200SP import QPX1200SP



# open test script and parse
with open('scripts/test.yaml', 'r', encoding='utf8') as f_yml:
    config = yaml.safe_load(f_yml)

    devices = {} # create empty dictionary
    for device in config['setup']['devices']:
        if device['type'] == 'nidaq':
            devices[device['name']] = nidaq(device['config'])
        elif device['type'] == 'QPX1200SP':
            devices[device['name']] = QPX1200SP(device['config'])
        else:
            print(f'unknown device type {device}')
        # else


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
