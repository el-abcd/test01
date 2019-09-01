

# https://www.raspberrypi.org/forums/viewtopic.php?t=219201

"""
import PySimpleGUI27 as sg

sg.Popup('Hello From PySimpleGUI!', 'This is the shortest GUI program ever!')
"""

#import PySimpleGUI as sg
import PySimpleGUIQt as sg
#import PySimpleGUIWeb as sg

layout = [[sg.Text('Filename', text_color='red')],
          [sg.Input(), sg.FileBrowse()],
          [sg.OK(), sg.Cancel()]]
#event, values = sg.Window('Get filename example').Layout(layout).Read()
window = sg.Window('Get filename example').Layout(layout)

# The Event Loop
while True:
    event, values = window.Read()
    if event is None:
        break
    if event == 'OK':
        print(values[0])
