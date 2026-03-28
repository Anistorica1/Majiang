import time

import cv2
import numpy as np
import mss
import glob
from Majiang_test import RiichiAI
import pyautogui
import os
scale = 1
hand = []
# 读取模板
def button():
    scale = 1
    hand = []
    # 读取模板
    templates = []
    for path in glob.glob("images2/*.png"):
        img = cv2.imread(path, 0)  # 灰度读取
        templates.append((path, img))

    resized_templates = []

    for name, template in templates:
        template = cv2.resize(template, None, fx=scale, fy=scale)
        resized_templates.append((name, template))

    # 缩放模板
    template = cv2.resize(template, None, fx=scale, fy=scale)

    # 用缩放后的尺寸
    w, h = template.shape[::-1]

    sct = mss.mss()

    monitor = {
        "top": 540,
        "left": 200,
        "width": 800,
        "height": 100
    }

    screen = np.array(sct.grab(monitor))
    gray = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)

    threshold = 0.8
    detections = []
    for name, template in resized_templates:
        w, h = template.shape[::-1]

        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)

        points = list(zip(*loc[::-1]))

        for pt in points:
            x, y = pt

            # 简单去重：如果附近已经检测过就跳过
            duplicate = False
            for dx, dy in detections:
                if abs(x - dx) < 10 and abs(y - dy) < 10:
                    duplicate = True
                    break

            if not duplicate:
                detections.append((x, y))
                cv2.rectangle(screen, pt, (x + w, y + h), (0, 255, 0), 2)
                hand.append(name)

    for i in hand:
        print(i)
        if i == "images2\\hu.png":
            find2("images2/hu.png")
            break
        elif i == "images2\\lizhi.png":
            find2("images2/lizhi.png")
            break
        elif i == "images2\\zimo.png":
            find2("images2/zimo.png")
            break
        elif i == "images2\\chi.png" or i == "images2\\peng.png" or i == "images2\\gang.png":
            print("mark2")
            find2("images2/tiao.png")
            break


def find2(string):
    scale = 1

    # 读取模板
    template = cv2.imread(string, 0)

    # 缩放模板
    template = cv2.resize(template, None, fx=scale, fy=scale)

    # 用缩放后的尺寸
    w, h = template.shape[::-1]

    sct = mss.mss()

    monitor = {
        "top": 540,
        "left": 200,
        "width": 800,
        "height": 100
    }

    screen = np.array(sct.grab(monitor))
    gray = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)

    # 用缩放后的 template
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)

    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.5:
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2

        # 👉 转换为屏幕坐标
        screen_x = center_x + monitor["left"]
        screen_y = center_y + monitor["top"]
        pyautogui.click(screen_x, screen_y)
def find(string):
    print("find"+string)
    scale = 1

    # 读取模板
    template = cv2.imread(string, 0)

    # 缩放模板
    template = cv2.resize(template, None, fx=scale, fy=scale)

    # 用缩放后的尺寸
    w, h = template.shape[::-1]

    sct = mss.mss()

    monitor = {
        "top": 640,
        "left": 100,
        "width": 800,
        "height": 100
    }

    screen = np.array(sct.grab(monitor))
    gray = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)

    # 用缩放后的 template
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)

    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.7:
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2

        # 👉 转换为屏幕坐标
        screen_x = center_x + monitor["left"]
        screen_y = center_y + monitor["top"]
        pyautogui.click(screen_x, screen_y)
        time.sleep(0.1)
        pyautogui.click(screen_x, screen_y)

templates = []
while True:
    button()
    for path in glob.glob("images/*.png"):
        img = cv2.imread(path, 0)  # 灰度读取
        templates.append((path, img))

    resized_templates = []

    for name, template in templates:
        template = cv2.resize(template, None, fx=scale, fy=scale)
        resized_templates.append((name, template))
    template = cv2.imread("images/dong.png", 0)

    # 缩放模板
    template = cv2.resize(template, None, fx=scale, fy=scale)

    # 用缩放后的尺寸
    w, h = template.shape[::-1]

    sct = mss.mss()

    monitor = {
        "top": 640,
        "left": 100,
        "width": 800,
        "height": 100
    }

    screen = np.array(sct.grab(monitor))
    gray = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)


    threshold = 0.8
    detections = []
    for name, template in resized_templates:
        w, h = template.shape[::-1]

        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        if name == "images\\9p.png" or name == "images\\8p.png":
            threshold = 0.7
        if (name == "images\\7t.png" or name == "images\\9t.png"):
            threshold = 0.85
        loc = np.where(result >= threshold)

        points = list(zip(*loc[::-1]))

        for pt in points:
            x, y = pt

            # 简单去重：如果附近已经检测过就跳过
            duplicate = False
            for dx, dy in detections:
                if abs(x - dx) < 10 and abs(y - dy) < 10:
                    duplicate = True
                    break

            if not duplicate:
                detections.append((x, y))
                cv2.rectangle(screen, pt, (x + w, y + h), (0, 255, 0), 2)
                path = name
                path = os.path.splitext(os.path.basename(path))[0]
                hand.append(path)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    print(len(hand))
    if len(hand) == 14:
        print("test")
        ai = RiichiAI(hand)
        find(f"images/{ai.recommend_discard()}.png")
        time.sleep(1)
        pyautogui.moveTo(100, 100)
        hand = []
        time.sleep(2)
    hand = []
    time.sleep(0.1)