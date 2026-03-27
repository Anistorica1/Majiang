from ultralytics import YOLO
import cv2
import numpy as np
import mss

# 加载模型
model = YOLO("yolov8n.pt")

# 创建截图对象
sct = mss.mss()

# 选择屏幕（主屏）
monitor = {
    "top": 100,
    "left": 100,
    "width": 800,
    "height": 600
}

while True:
    # 截图
    screenshot = sct.grab(monitor)

    # 转成 numpy 格式
    frame = np.array(screenshot)

    # BGRA → BGR（opencv格式）
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    # YOLO检测
    results = model(frame)

    # 绘制结果
    annotated_frame = results[0].plot()

    # 显示
    cv2.imshow("Screen Detection", annotated_frame)

    # 按 q 退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()