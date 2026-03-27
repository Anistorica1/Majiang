import cv2
import numpy as np
import mss
import glob
from Majiang_test import MahjongAI

scale = 1
hand = []
# 读取模板
templates = []

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


threshold = 0.9
detections = []
while True:
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

    cv2.imshow("Detect", screen)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
print(hand)