# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 20:53:15 2019

@author: fddot
"""

import pyautogui as auto
#from PIL import ImageGrab, ImageOps
#import numpy as np
import time
#import numpy as np

# %%

def main_screen_detection():
    main_screen = auto.locateOnScreen(r'IMG\LDP_detect.png', confidence = 0.6)
    main_x = main_screen[0]+1
    main_y = main_screen[1]+main_screen[3]
    return main_screen, main_x, main_y

# %%

def scanwindow():
    game_window = auto.screenshot(region=(main_x, main_y, 480, 860))
    return game_window

# %%
    
def click_buttons(button):
    window = scanwindow()
    location = auto.locate(r'IMG\%s.png' %button, window, confidence = 0.6)
    auto.click(main_x+auto.center(location)[0], main_y+auto.center(location)[1], duration = 1)
    
# %%
    
def world_boss_auto():
    #err_count = 0
    global reset_count
    
    print('Fighting Mona!')
    try:
        click_buttons('stage_WB_khepri')
        time.sleep(5)
    except TypeError:
        pass
    try:
        click_buttons('WB_trial_start')
        time.sleep(3)
    except TypeError:
        pass
    
    time.sleep(2)
    
    while True:
        try:
            time.sleep(2)
            click_buttons('WB_battle_start')
            print('Starting Battle...')
            time.sleep(2)
            try:
                click_buttons('purchase_ticket_yes')
                print(r"Tickets depleted. Let's buy some.")
                reset_count += 1
                time.sleep(2)
                click_buttons('WB_battle_start')
            except TypeError:
                pass
            time.sleep(2)
            print('waiting for the battle...')
            wb_timeout = time.time() + 400
            
            battle_sequence(wb_timeout)
            
        except TypeError:
            print('whoops! something error! restarting...')
            click_buttons('purchase_ticket_yes')
            print('The current connection was not reliable!')
            battle_sequence(time.time())
            break
    
    return

def battle_sequence(wb_timeout):
    global wb_count
    
    while True:
        try:
            window = scanwindow()
            a = auto.locate(r'IMG\DC_stopped.png', window, confidence = 0.7)
            if a:
                break
        except TypeError:
            pass
        time.sleep(3)
        window = scanwindow()
        end_check = auto.locate(r'IMG\wb_end.png', window, confidence = 0.7)
        location = auto.locate(r'IMG\battle_retry.png', window, confidence = 0.7)
        time.sleep(2)
        try:
            if end_check or location:
                print(r"Battle's done!")
                wb_count += 1
                print(r"reset count = " + str(reset_count))
                print(r"WB_count = " + str(wb_count))
                if location:
                    auto.click(main_x+auto.center(location)[0], main_y+auto.center(location)[1], clicks = 5, interval = 0.5, duration = 0.5)
                auto.click(main_x+150, main_y+300, duration = 0.5,  pause = 1.2)
                time.sleep(10)
                break
        except TypeError:
            pass
        
        if time.time() > wb_timeout:
            print(r"The battle's gone too long... Something's wrong. Probably not started properly. Resetting...")
            time.sleep(2)
            break
    
    return 
#%%

main_screen, main_x, main_y = main_screen_detection()
if 'reset_count' not in globals():
    reset_count = 0
if 'wb_count' not in globals():
    wb_count = 0
while True:
    try:
        world_boss_auto()
    except TypeError:
        print('something wrong, resetting...')
        auto.click(main_x+ 500, main_y+ 830, interval = 0.5, duration = 0.5)
        time.sleep(1)
        auto.moveTo(x = main_x+240, y = main_y+315, duration = 0.5)
        time.sleep(1)
        auto.dragRel(-300, 0, duration =  0.30)
        time.sleep(2)
        auto.click(main_x+ 500, main_y+ 750, interval = 0.5, duration = 0.5)
        time.sleep(2)
        click_buttons('destiny_child_app')
        time.sleep(5)
        while True:
            waiting = scanwindow()
            locate_start = auto.locate(r'IMG\press_start.png', waiting, confidence = 0.7)
            if locate_start:
                auto.click(main_x+240, main_y+315, duration = 0.5, interval = 0.5)
                time.sleep(10)
                auto.click(main_x+240, main_y+315, clicks = 10, duration = 0.5, interval = 0.5)
                while True:
                    try:
                        click_buttons('close_all_day')
                        time.sleep(2)
                    except TypeError:
                        auto.click(main_x+240, main_y+315, clicks = 10, duration = 0.5, interval = 0.5)
                        break
                break
            else:
                continue
    