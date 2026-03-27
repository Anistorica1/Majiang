from ultralytics import YOLO
import cv2

# 加载模型（会自动下载）
model = YOLO("yolov8n.pt")

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 进行检测
    results = model(frame)

    # 绘制结果
    annotated_frame = results[0].plot()

    # 显示
    cv2.imshow("YOLOv8 Detection", annotated_frame)

    # 按 q 退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()