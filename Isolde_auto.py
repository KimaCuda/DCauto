# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 10:49:08 2019

@author: fddot
"""

import pyautogui as auto
from wand.image import Image
import cv2
import pytesseract as ocr
#from PIL import ImageGrab, ImageOps
#import numpy as np
import time
#import numpy as np
import re
ocr.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

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
    location = auto.locate(r'IMG\%s.png' %button, window, confidence = 0.7)
    auto.click(main_x+auto.center(location)[0], main_y+auto.center(location)[1], duration = 0.5)

#%%
class ocr_prep:
    
    def __init__(self, name):
        self.name = name
    
    @staticmethod
    def reader(query_img):
        with Image(filename = r'IMG\temp\%s.png' %query_img) as img:
            img.transform('300x300','900%')
            img.save(filename = r'IMG\temp\testla.png')
        
        img = cv2.imread(r'IMG\temp\testla.png')
        a = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        b = a.copy()
        for i in range(len(b)):
            for j in range(len(b[0])):
                if b[i][j] > 220 and b[i][j] < 255:
                    b[i][j] = 0
                else:
                    b[i][j] = 255
        
        return b
    
    
    def read_ticket_amount(self):
        raid_left = 99
        namesake = 'ticket_amount_pic'
        pattern = '[0-9]'
        window = scanwindow()
        raid_ticket = auto.locate(r'IMG\raid_ticket.png', window, confidence = 0.7)
        auto.screenshot(r'IMG\temp\%s.png' %namesake, region=(main_x+raid_ticket[0]+27, main_y+raid_ticket[1]+5, 17, 25))
        ticket_text_matrix = self.reader(namesake)
        for i in range(4):
            ticket_text = ocr.image_to_string(ticket_text_matrix, config = '--oem %s --psm 7' %i)
            timer_regex = re.search(pattern, ticket_text)
            if timer_regex:
                print('There are ' + str(timer_regex[0]) + ' tickets left.')
                raid_left = int(timer_regex[0])
                break
            else:
                continue
        
        if raid_left == 99:
            print('ticket amount not identified. will check again in the next 2 minutes..')
            time.sleep(120)
        return raid_left    

#%%

def summer_scandal():
    a = ocr_prep('a')
    no_raid_test_count = 0
    while True:
        try:
            click_buttons('ragna_break_main')
        except:
            pass
        time.sleep(5)
        raid_left = a.read_ticket_amount()
        if raid_left == 99:
            continue
        time.sleep(2)
        if raid_left >= max_idling_ticket:
            print(r'the raid ticket is almost full! time to use it.')
            print('choosing raid...')
            click_buttons('change_order')
            time.sleep(1)
            click_buttons('not_joining_checklist')
            time.sleep(1)
            click_buttons('sort_participants')
            time.sleep(1)
            window = scanwindow()
            no_raid_test = auto.locate(r'IMG\no_raid.png', window, confidence = 0.7)
            if no_raid_test:
                print(r"there's no raid suitable.. Waiting for a bit...")
                time.sleep(60)
                no_raid_test_count += 1
                if no_raid_test_count >= 10:
                    break
            else:
                offset_y = 70
                location = auto.locate(r'IMG\refresh_button.png', window, confidence = 0.7)
                auto.click(main_x+auto.center(location)[0]+75, main_y+auto.center(location)[1]+offset_y, duration = 0.5)
                time.sleep(2)
                auto.click(main_x+420, main_y+195, duration = 0.5)
                time.sleep(2)
                click_buttons('raid_battle_start')
                print('starting battle..')
                time.sleep(5)
                try:
                    endtimecheck_window = scanwindow()
                    near_end = auto.locate(r'IMG\endtime_near_no.png', endtimecheck_window, confidence = 0.7)
                    if near_end:
                        offset_y = offset_y + 100
                        click_buttons('endtime_near_no')
                        time.sleep(1)
                        click_buttons('battle_x_button')
                        time.sleep(2)
                        auto.click(main_x+auto.center(location)[0]+75, main_y+auto.center(location)[1]+offset_y, duration = 0.5)
                        time.sleep(2)
                        click_buttons('raid_battle_start')
                        print('starting battle..')
                        time.sleep(5)
                except TypeError:
                    pass
                raid_timeout = time.time() + 500
                battle_sequence(raid_timeout)
        else:
            print(r'The ticket is at a normal amount. Standing By...')
            time.sleep(600)
    return


def battle_sequence(raid_timeout):
    global raid_count
    
    while True:
        time.sleep(5)
        window = scanwindow()
        end_check1 = auto.locate(r'IMG\ragna_break_end.png', window, confidence = 0.7)
        end_check2 = auto.locate(r'IMG\ragna_break_end3.png', window, confidence = 0.7)
        time.sleep(2)
        try:
            if end_check1 or end_check2:
                print(r"Battle's done!")
                raid_count += 1
                print(r"raid_count = " + str(raid_count))
                if end_check2:
                    location = auto.locate(r'IMG\ragna_break_end4.png', window, confidence = 0.7)                    
                    auto.click(main_x+auto.center(location)[0], main_y+auto.center(location)[1], duration = 0.5)
                    time.sleep(2)
                auto.click(main_x+150, main_y+300, clicks = 2, interval = 0.5,  duration = 0.5)
                time.sleep(10)
                break
        except TypeError:
            pass
        
        if time.time() > raid_timeout:
            print(r"The battle's gone too long... Something's wrong. Probably not started properly. Resetting...")
            time.sleep(2)
            break
    
    return 

#%%

raid_count = 0
max_idling_ticket = 2
main_screen, main_x, main_y = main_screen_detection()
while True:
    try:
        summer_scandal()
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
