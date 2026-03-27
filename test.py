import cv2
import numpy as np
import mss

scale = 1

# 读取模板
template = cv2.imread("images/1t.png", 0)

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

while True:
    screen = np.array(sct.grab(monitor))
    gray = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)

    # 用缩放后的 template
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)

    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.9:
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(screen, top_left, bottom_right, (0, 255, 0), 2)
        print("detected", max_val)

    cv2.imshow("Detect", screen)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()