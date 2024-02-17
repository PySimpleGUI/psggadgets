'''
Copyright 2023 PySimpleSoft, Inc. and/or its licensors. All rights reserved.

Redistribution, modification, or any other use of PySimpleGUI or any portion thereof is subject
to the terms of the PySimpleGUI License Agreement available at https://eula.pysimplegui.com.

You may not redistribute, modify or otherwise use PySimpleGUI or its contents except pursuant
to the PySimpleGUI License Agreement.
'''

import PySimpleGUI as sg
import psutil
import sys

"""
    Another simple Desktop Widget using PySimpleGUI
    This time a RAM indicator.  The Widget is square.  The bottom section will be shaded to 
    represent the total amount of RAM currently in use.
    The % and number of bytes in use is shown on top in text.
    Uses the theme's button color for colors.
"""

THEME = 'Dark Green 5'
GSIZE = (180, 180)
UPDATE_FREQUENCY_MILLISECONDS = 10 * 1000


def saved_alpha():
    return sg.user_settings_get_entry('-alpha-', 10)


def right_click_menu():
    alpha = saved_alpha()
    menu = [[''], [
                     'Transparency', [f'{x}{" "+sg.SYMBOL_CHECK_SMALL if x == alpha else "  "}::alpha' for x in range(1, 11)],
                     'Edit Me',
                     'Version',
                     'Exit',]
                        ]
    return menu



def human_size(bytes, units=(' bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB')):
    """ Returns a human readable string reprentation of bytes"""
    return str(bytes) + ' ' + units[0] if bytes < 1024 else human_size(bytes >> 10, units[1:])



def main(location):
    sg.theme(THEME)

    graph = sg.Graph(GSIZE, (0, 0), GSIZE, key='-GRAPH-', enable_events=True, tooltip='Right click for menu')
    layout = [[graph]]

    window = sg.Window('RAM Usage Widget Square', layout, location=location, no_titlebar=True, grab_anywhere=True, margins=(0, 0), element_padding=(0, 0), alpha_channel=saved_alpha()/10, finalize=True, right_click_menu=right_click_menu(), enable_close_attempted_event=True, keep_on_top=True, auto_save_location=True)


    while True:  # Event Loop
        # ----------- update the graphics and text in the window ------------
        ram = psutil.virtual_memory()
        rect_height = int(GSIZE[1] * float(ram.percent) / 100)
        rect_id = graph.draw_rectangle((0, rect_height), (GSIZE[0], 0), fill_color=sg.theme_button_color()[1], line_width=0)
        text_id1 = graph.draw_text(f'{int(ram.percent)}%', (GSIZE[0] // 2, GSIZE[1] // 2), font='Any 40', text_location=sg.TEXT_LOCATION_CENTER,
                                   color=sg.theme_button_color()[0])
        text_id2 = graph.draw_text(f'{human_size(ram.used)} used', (GSIZE[0] // 2, GSIZE[1] // 4), font='Any 20', text_location=sg.TEXT_LOCATION_CENTER, color=sg.theme_button_color()[0])

        event, values = window.read(timeout=UPDATE_FREQUENCY_MILLISECONDS)
        if event in (sg.WIN_CLOSED, 'Exit', sg.WIN_CLOSE_ATTEMPTED_EVENT):
            if event != sg.WIN_CLOSED:
                sg.user_settings_set_entry('-location-', window.current_location())  # The line of code to save the position before exiting
            break

        if event.endswith('alpha') and not sg.SYMBOL_CHECK_SMALL in event:     # if a new alpha is chosen
            alpha = int(event.split('::')[0])
            window.set_alpha(alpha/10)
            sg.user_settings_set_entry('-alpha-', alpha)
            window['-GRAPH-'].set_right_click_menu(right_click_menu())

        if event == 'Edit Me':
            sg.execute_editor(__file__)
        elif event == 'Version':
            sg.popup_scrolled(__file__, sg.get_versions(), location=window.current_location(), keep_on_top=True, non_blocking=True)

        graph.delete_figure(rect_id)
        graph.delete_figure(text_id1)
        graph.delete_figure(text_id2)
    window.close()

if __name__ == '__main__':

    location = sg.user_settings_get_entry('-location-', (None, None))
    main(location)
