import cv2
import numpy as np
from mss import mss

sct = mss()

monitor = {
    "top": 640,
    "left": 100,
    "width": 800,
    "height": 100
}

while True:
    # 截图
    screen = np.array(sct.grab(monitor))

    # 显示
    cv2.imshow('Screen Capture', screen)

    # 必须有这行才能刷新显示
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print("Test")

cv2.destroyAllWindows()