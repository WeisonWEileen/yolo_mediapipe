import cv2
import mediapipe as mp
import numpy as np
from ultralytics import YOLO
import threading
import matplotlib.pyplot as plt

# 加载 YOLO 模型
yolo_model = YOLO('hand_detection/yolov8x.pt')

# 加载 Mediapipe 手部模型
mp_hands = mp.solutions.hands
hands_model = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75)

# 初始化距离数据
distances = []

# 获取摄像头
cap = cv2.VideoCapture(0)

# 更新距离数据的函数
def update_distance(hand_position, cup_position):
    distance = np.linalg.norm(hand_position - cup_position)
    distances.append(distance)

# 实时绘制距离变化的函数
def plot_distance():
    plt.ion()  # 开启交互模式
    plt.figure()
    plt.xlabel('Frame')
    plt.ylabel('Distance')
    plt.title('Distance over Time')
    while True:
        plt.clf()  # 清除之前的图形
        plt.plot(distances)  # 绘制距离变化
        plt.pause(0.1)  # 暂停一小段时间
        if cv2.waitKey(1) & 0xFF == 27:  # 按下 ESC 键退出循环
            break

# 创建一个新线程用于实时绘制距离变化
plot_thread = threading.Thread(target=plot_distance)
plot_thread.start()

# 主循环
while True:
    # 从摄像头获取图像并处理
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, 1)
    results = hands_model.process(frame)

    # 检测手部和杯子的位置
    hand_position = np.array([0, 0])
    cup_position = np.array([0, 0])
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for index, lm in enumerate(hand_landmarks.landmark):
                if index == 9:
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    hand_position = np.array([cx, cy])
                    break

    # yolo_results = yolo_model.predict(frame,)
    yolo_results = yolo_model.predict(frame)
                
    for r in yolo_results:
        for box in r.boxes:
            if box.cls.cpu().numpy().astype(int) == 39:
                four_points = box.xyxy.squeeze()
                cup_position = np.array([
                    (int(four_points[2]) - int(four_points[0])) / 2 + int(four_points[0]),
                    (int(four_points[3]) - int(four_points[1])) / 2 + int(four_points[1])
                ])
                break

    # 更新距离数据
    update_distance(hand_position, cup_position)

# 释放摄像头资源
cap.release()
cv2.destroyAllWindows()
