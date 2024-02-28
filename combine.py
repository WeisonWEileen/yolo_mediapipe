import cv2
import mediapipe as mp
import numpy as np
from ultralytics import YOLO

# Load YOLO model
yolo_model = YOLO('hand_detection/yolov8x.pt')

#Mediapipe的字体设置
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.5
font_thickness = 1
font_color = (255, 255, 255)

# Load MediaPipe hands model
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands_model = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # 因为摄像头是镜像的，所以将摄像头水平翻转
    # 不是镜像的可以不翻转
    frame= cv2.flip(frame,1)
    results = hands_model.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    if results.multi_handedness:
        for hand_label in results.multi_handedness:
            print(hand_label)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
          for index, lm in enumerate(hand_landmarks.landmark):
                if index == 9:
                    # 索引为0代表手底部中间部位，为4代表手指关键或指尖
                    # print(index, lm)  # 输出21个手部关键点的xyz坐标(0-1之间)，是相对于图像的长宽比例
                    # 只需使用x和y查找位置信息
                    
                    # 将xy的比例坐标转换成像素坐标
                    h, w, c = frame.shape # 分别存放图像长\宽\通道数
                    
                    # 中心坐标(小数)，必须转换成整数(像素坐标)
                    cx ,cy =  int(lm.x * w), int(lm.y * h) #比例坐标x乘以宽度得像素坐标
                    
                    # 打印显示21个关键点的像素坐标
                    print(index, cx, cy)
                    
                    # 存储坐标信息
                    # lmList.append([index, cx, cy])
                        
                    # 在21个关键点上换个圈，img画板，坐标(cx,cy)，半径5，蓝色填充
                    cv2.circle(frame, (cx,cy), 5, (0,0,255), cv2.FILLED)
                    text = f'({cx}, {cy})'
                    cv2.putText(frame, text, (cx, cy - 10), font, font_scale, font_color, font_thickness)
    # cv2.imshow('MediaPipe Hands', frame)
    resuzlts = yolo_model(frame, show=True,)
    print("----------------begin----------------------\n")
    if resuzlts:
        print(resuzlts[0].names)
    print("-----------------end---------------------\n")

        
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()