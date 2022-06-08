import os
import PySimpleGUI as sg


WIDTH  = 100
HEIGHT = 300
VERSION = '0.0.1'

sg.theme('DarkAmber')
title = f'Test Engine v{VERSION}'
pad_char = '_'
padding = f'{"" :{pad_char}^{WIDTH}}'

tab1_layout = \
    [
        [sg.Text('Test Script'), sg.InputText(f'{os.getcwd()}/scripts/test.yaml', key='-fb_text-', expand_x=True), sg.FileBrowse(key='-fb-', file_types=(('YAML', '*.yaml'),)), sg.Button('Open')],
        [sg.Text(padding, expand_x=True)],
        [sg.Radio('Radio 1', 'test_rad', default=True), sg.Radio('Radio 2', 'test_rad'), sg.Radio('Radio 3', 'test_rad')],
        [sg.Checkbox('Checkbox 1', default=True), sg.Checkbox('Checkbox 2', disabled=True)],
        [sg.Multiline('>', background_color='grey', size=(10,20), expand_x=True, expand_y=True)],
        [sg.Text('Show messages :'), sg.Checkbox('Info <~>', text_color='blue', default=True), sg.Checkbox('Warning <?>', text_color='orange'), sg.Checkbox('Error <!>', text_color='red')]
    ]

tab2_frame1 =\
    [
        [sg.Text('d0'), sg.Radio('input', 'radio_0', default=True), sg.Radio('output', 'radio_0'), sg.Checkbox('', disabled=True, default=True), sg.Button(' ', button_color='red')]
    ]

tab2_layout = \
    [
        [sg.Text('Test Script'), sg.InputText(f'{os.getcwd()}/scripts/test.yaml', key='-fb_text-'), sg.FileBrowse(key='-fb-'), sg.Button('Open')],
        [sg.Text(padding)],
        [sg.Frame('digital', tab2_frame1)]
    ]

layout = [[sg.TabGroup([[sg.Tab('Test Script', tab1_layout), sg.Tab('NIdaq', tab2_layout)]], expand_x=True, expand_y=True)]]
#window = sg.Window(title="Hello World", layout=layout, margins=(WIDTH, HEIGHT), resizable=True)
window = sg.Window(title=title, layout=layout, resizable=True)

while True:
    event,values = window.read()

    if event == 'Open':
        window['-fb_text-'].update(disabled=True)
        window['-fb-'].update(disabled=True)

    elif event == 'OK' or event == sg.WIN_CLOSED:
        break
    # if
# while

window.close()

# EOF
