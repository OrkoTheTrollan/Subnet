#!/usr/bin/env python
from os import system
import PySimpleGUI as sg
import io
import platform
import ctypes
import base64

logo='logo_small.png'

# Fix Bug on Windows when using multiple screens with different scaling
def make_dpi_aware():
    global logo
    if platform.system() == 'Windows' and int(platform.release()) >= 8: 
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
        logo='logo_large.png'
    #return logo        


cprint = sg.cprint
MLINE_KEY = '-ML-' #+sg.WRITE_ONLY_KEY   # multiline element's key. Indicate it's an output only element

output_key = MLINE_KEY

def make_window():

    sg.user_settings_filename(path='.', filename='user_settings.json')
    sg.theme(sg.user_settings_get_entry('-theme-', 'DarkBlue2'))  # set the theme

    layout = [[sg.Text('Settings Window')],
              [sg.Listbox(sg.theme_list(), default_values=[sg.user_settings_get_entry('theme')], size=(15, 10), k='-LISTBOX-')],
              [sg.T('Settings file = ' + sg.user_settings_filename())],
              [sg.Button('Save'), sg.Button('Exit without saving', k='Exit')]]

    return sg.Window('A Settings Window', layout)


def settings_window():
    """
    Create and interact with a "settings window". You can a similar pair of functions to your
    code to add a "settings" feature.
    """

    window = make_window()
    current_theme = sg.theme()

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break
        if event == 'Save':
            # Save some of the values as user settings
            #sg.user_settings_set_entry('-input-', values['-IN-'])
            sg.user_settings_set_entry('-theme-', values['-LISTBOX-'][0])
            #sg.user_settings_set_entry('-option1-', values['-CB1-'])
            #sg.user_settings_set_entry('-option2-', values['-CB2-'])

        # if the theme was changed, restart the window
        if values['-LISTBOX-'][0] != current_theme:
            current_theme = values['-LISTBOX-'][0]
            window.close()
            window = make_window()

def second_window():

    layout = [[sg.Text('The second form is small \nHere to show that opening a window using a window works')],
              [sg.OK()]]

    window = sg.Window('Second Form', layout)
    event, values = window.read()
    window.close()

class IP4_Subnets:
    
    def __init__(self, ip_part1, ip_part2, ip_part3, ip_part4, number_subnets):
        self.ip_part1 = ip_part1
        self.ip_part2 = ip_part2
        self.ip_part3 = ip_part3
        self.ip_part4 = ip_part4
        self.number_subnets = number_subnets
    
    def output_subnets(self):
        if self.ip_part1 == '' or self.ip_part2 == '' or self.ip_part3 == '' or self.ip_part4 == '' or self.number_subnets == '':
            cprint('Input incomplete')
        else:
            try:
                self.ip_part1 = int(self.ip_part1)
                self.ip_part2 = int(self.ip_part2)
                self.ip_part3 = int(self.ip_part3)
                self.ip_part4 = int(self.ip_part4)
                self.number_subnets = int(self.number_subnets)
                if self.ip_part1 in range(192, 224) and self.ip_part2 in range(0, 256) and self.ip_part3 in range(0, 256) and self.ip_part4 in range(0, 256):
                    cprint('Here are the', self.number_subnets,'subnets for the given IP4-adress')
                    cprint('')
                    self.ip_part4 = 0
                    number = 1
                    while (self.ip_part4 < 255):
                        cprint(number,'.', 'Subnet')
                        cprint('Network:     ', self.ip_part1, '.', self.ip_part2, '.', self.ip_part3, '.', self.ip_part4)
                        cprint('First Host:   ', self.ip_part1, '.', self.ip_part2,'.', self.ip_part3, '.', self.ip_part4 + 1)
                        cprint('Last Host:   ', self.ip_part1, '.', self.ip_part2, '.',self.ip_part3, '.', self.ip_part4 + 256 // self.number_subnets - 2)
                        cprint('Broadcast:  ', self.ip_part1, '.', self.ip_part2, '.',self.ip_part3, '.', self.ip_part4 + 256 // self.number_subnets - 1)
                        cprint('')
                        self.ip_part4 = self.ip_part4 + (256 // self.number_subnets)
                        number+=1
                else:
                    cprint('The input is not a valid IP4-adress for class-c-network.')

            except:
                cprint('Only Integer are allowed')
   

def main():
    global logo
    make_dpi_aware()
    sg.user_settings_filename(path='.', filename='user_settings.json')
    sg.theme(sg.user_settings_get_entry('-theme-', 'DarkBlue2'))
    sg.set_global_icon(icon = 'Network.ico') if platform.system() == 'Windows' else sg.set_global_icon(base64.b64encode(open('network 2.png', 'rb').read())) 
    sg.set_options(element_padding=(0, 5))

    col1 = sg.Column([[sg.Image(logo, pad=(20,35))]], expand_x=True, pad=(40, 0))
    col2 = sg.Column([[sg.Text('Enter IP4-adress and choose number of subnets')],
                [sg.Text('IP4-adress:      '), sg.Input(key='-IP1-', s=3), sg.Text('.'), sg.Input(key='-IP2-', s=3), sg.Text('.'), sg.Input(key='-IP3-', s=3), sg.Text('.'), sg.Input(key='-IP4-', s=3)],
                [sg.Text('Number of subnets: '), sg.Combo([1,2,4,8,16,32,64], default_value=2, bind_return_key = True, readonly=True, key='-subn-')],   
                [sg.Button('Run')]],
                pad=(40,10))
    col3 = sg.Column([[sg.HSep(pad=(8,6))],[sg.Multiline(no_scrollbar=True, size=(90,15), pad=(15,15), key=MLINE_KEY)]], pad=(0,0))
    

    # ------ Menu Definition ------ #
    menu_def = [['&File', ['&Save', '&Settings', 'E&xit' ]],
                ['&Help', '&About...'],]

    #right_click_menu = ['Unused', ['Right', '!&Click', '&Menu', 'E&xit', 'Properties']]

     # ------ GUI Defintion ------ #
    layout = [
              [sg.MenubarCustom(menu_def, tearoff=False)],
              [col1, col2], [col3]
              ]
    
    window = sg.Window("Subnet Calc",
                       layout,
                       default_element_size=(10, 1),
                       grab_anywhere=True,
                       margins=(0,0),
                       font='Verdana` 10',
                       #right_click_menu=right_click_menu,
                       default_button_element_size=(10, 1))

    sg.cprint_set_output_destination(window, output_key)
   
    
    # ------ Loop & Process button menu choices ------ #
    while True:
        event, values = window.read()
        if event is None or event == 'Exit':
            return
        if event == 'Run':
            window[output_key]('')
            ip = IP4_Subnets(values['-IP1-'], values['-IP2-'], values['-IP3-'], values['-IP4-'], values['-subn-'])
            ip.output_subnets()         
        # ------ Process menu choices ------ #
        if event == 'About...':
            window.disappear()
            sg.popup('Subnet Calculator','Version 1.0', 'PySimpleGUI rocks...', grab_anywhere=True)
            window.reappear()
        elif event == 'Save':
            with io.open("data.txt", "w", encoding="utf8") as f:
                f.write(values[output_key])
            f.close()
        elif event == 'Settings':
            settings_window()

main()