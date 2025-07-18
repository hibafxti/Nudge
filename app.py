# app.py Building Nudge

import FreeSimpleGUI as sg
import csv
import random
import time
import os
import sys
from datetime import datetime

# --- Color Palette & Pattern ---
ICED_PETAL = '#D2A4B4'
CHARCOAL_VELVET = '#3A3A3C'
PORCELAIN_BLUSH = '#F1E6E8'
DUST_PETAL = '#EDD2D9'
ONYX_SILK = '#2B2B2B'
CUTE_PATTERN = "𐙚⋆.˚"

# --- GUI Theme Definition ---
sg.theme_background_color(PORCELAIN_BLUSH)
sg.theme_text_element_background_color(PORCELAIN_BLUSH)
sg.theme_text_color(ONYX_SILK)
sg.theme_button_color((ONYX_SILK, DUST_PETAL))
sg.set_options(font=("Palatino", 17), border_width=0)

def load_questions(filename='questions.csv'):
    questions = []
    try:
        with open(filename, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                questions.append(row)
    except FileNotFoundError:
        sg.popup_error(f"Error: The file '{filename}' was not found.", background_color=DUST_PETAL)
        return None
    return questions

def create_question_window(question_data):
    """Creates a new question window."""
    layout_question = [
        [sg.Text(CUTE_PATTERN, font=("Palatino", 12), background_color=PORCELAIN_BLUSH)],
        [sg.Text(question_data['Question'], justification='center', pad=(10, 10), background_color=PORCELAIN_BLUSH)],
        [sg.Text(CUTE_PATTERN, font=("Palatino", 12), background_color=PORCELAIN_BLUSH)],
        [sg.Button("I remember!", key='-REMEMBERED-', button_color=(ONYX_SILK, ICED_PETAL)), sg.Button("I forgot!", key='-FORGOT-')]
    ]
    # --- Goodbye and End Session Button ---
    layout_answer = [
        [sg.Text(f"Answer: {question_data['Answer']}", justification='center', pad=(10, 20), background_color=PORCELAIN_BLUSH)],
        [
            sg.Button("Close", key='-CLOSE-', button_color=(ONYX_SILK, DUST_PETAL)),
            sg.Button("End & Say Goodbye", key='-END-', button_color=(ONYX_SILK, ICED_PETAL))
        ]
    ]
    column_question = sg.Column(layout_question, key='-COL_Q-', element_justification='center', background_color=PORCELAIN_BLUSH)
    column_answer = sg.Column(layout_answer, key='-COL_A-', visible=False, element_justification='center', background_color=PORCELAIN_BLUSH)
    bordered_layout = [[sg.Frame('', [[column_question, column_answer]], background_color=ICED_PETAL, border_width=0, pad=(5,5))]]
    return sg.Window("Nudge", bordered_layout, no_titlebar=True, keep_on_top=True, grab_anywhere=True, location=(None, None), finalize=True, margins=(0,0), background_color=PORCELAIN_BLUSH)

def show_goodbye_message():
    """Shows the final goodbye message."""
    goodbye_layout = [[sg.Column([
        [sg.Text("Great work! ✨", font=("Palatino", 18), background_color=PORCELAIN_BLUSH)],
        [sg.Text("Closing your Nudge session.", background_color=PORCELAIN_BLUSH)],
        [sg.Text(CUTE_PATTERN, font=("Palatino", 12), background_color=PORCELAIN_BLUSH)]
    ], background_color=PORCELAIN_BLUSH, pad=(20,20), element_justification='center')]]
    goodbye_window = sg.Window("Goodbye!", goodbye_layout, no_titlebar=True, keep_on_top=True, location=(None, None), finalize=True, background_color=PORCELAIN_BLUSH)
    goodbye_window.read(timeout=3000)
    goodbye_window.close()

def main():
    popup_interval_seconds = 60
    
    # --- Intro Message ---
    intro_layout = [[sg.Column([
        [sg.Text(CUTE_PATTERN, font=("Palatino", 12), background_color=PORCELAIN_BLUSH)],
        [sg.Text("Nudge session starting...", pad=(10,5), background_color=PORCELAIN_BLUSH)],
        [sg.Text(f"A question will pop up every minute.", font=("Palatino", 14), background_color=PORCELAIN_BLUSH)],
        [sg.Text(CUTE_PATTERN, font=("Palatino", 12), background_color=PORCELAIN_BLUSH)]
    ], background_color=PORCELAIN_BLUSH, pad=(10,10), element_justification='center')]]
    bordered_intro = [[sg.Frame('', intro_layout, background_color=ICED_PETAL, border_width=0, pad=(5,5))]]
    intro_window = sg.Window("Nudge Start", bordered_intro, no_titlebar=True, keep_on_top=True, grab_anywhere=True, location=(None, None), finalize=True, background_color=PORCELAIN_BLUSH)
    intro_window.read(timeout=4000)
    intro_window.close()

    all_questions = load_questions()
    if not all_questions:
        return
    
    review_queue = []
    last_popup_time = time.time() - popup_interval_seconds + 5
    popup_window = None
    
    keep_running = True
    while keep_running:
        if popup_window:
            event, _ = popup_window.read(timeout=100)
            if event in (sg.WIN_CLOSED, '-CLOSE-'):
                popup_window.close()
                popup_window = None
            elif event == '-END-':
                # This is the new, graceful way to stop
                popup_window.close()
                popup_window = None
                keep_running = False # Signal the main loop to stop
            elif event in ('-REMEMBERED-', '-FORGOT-'):
                popup_window['-COL_Q-'].update(visible=False)
                popup_window['-COL_A-'].update(visible=True)
                popup_window.refresh()
        
        if popup_window is None and keep_running and (time.time() - last_popup_time) > popup_interval_seconds:
            if not review_queue:
                review_queue = all_questions.copy()
                random.shuffle(review_queue)
            question_to_show = review_queue.pop()
            popup_window = create_question_window(question_to_show)
            last_popup_time = time.time()
        
        time.sleep(0.1)

    # This code only runs after the loop has been stopped by the '-END-' button
    show_goodbye_message()

if __name__ == "__main__":
    main()