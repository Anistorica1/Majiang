import pyautogui
import time

print("请将鼠标移动到目标位置，5秒后获取坐标...")
time.sleep(5)
x, y = pyautogui.position()
print(f"当前鼠标坐标: ({x}, {y})")