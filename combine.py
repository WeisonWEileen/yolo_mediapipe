import cv2
import mediapipe as mp
import numpy as np
from ultralytics import YOLO
import math

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



distance = 0

# hand_position = np.array([0,0])
# cup_position = np.array([0,0])

#用于记录是否识别到 bottle 和 hand
box_flag = False
hand_flag = False

while True:

    hand_position = np.array([0,0])
    cup_position = np.array([0,0])
    hand_flag = False


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
                    yolo_model
                    # 将xy的比例坐标转换成像素坐标
                    h, w, c = frame.shape # 分别存放图像长\宽\通道数
                    
                    # 中心坐标(小数)，必须转换成整数(像素坐标)
                    cx ,cy =  int(lm.x * w), int(lm.y * h) #比例坐标x乘以宽度得像素坐标
                    hand_position = np.array([int(lm.x * w),int(lm.y * h)])
                    # 打印显示21个关键点的像素坐标
                    print(index, cx, cy)
                    
                    # 存储坐标信息
                    # lmList.append([index, cx, cy])
                        
                    # 在21个关键点上换个圈，img画板，坐标(cx,cy)，半径5，蓝色填充
                    cv2.circle(frame, (cx,cy), 5, (0,0,255), cv2.FILLED)
                    text = f'({cx}, {cy})'
                    cv2.putText(frame, text, (cx, cy - 10), font, font_scale, font_color, font_thickness)
                    

                    #识别到了，调整flag
                    hand_flag = True
    # cv2.imshow('MediaPipe Hands', frame)
    yolo_results = yolo_model.predict(frame, show=True,)
    for r in yolo_results:
        for box in r.boxes:
            if box.cls.cpu().numpy().astype(int) == 39 and hand_flag == True:  #bottle的id是39
                four_points = box.xyxy.squeeze()
                cup_position = np.array([
                    (int(four_points[2]) - int(four_points[0])) / 2 + int(four_points[0]),
                    (int(four_points[3]) - int(four_points[1])) / 2 + int(four_points[1])
                    ])
                
                distance = np.linalg.norm(hand_position - cup_position)
                print("两点之间的距离:", distance)
                # cv2.line(frame, cup_position, hand_position, (0,0,255), font_thickness)
                # cv2.line(frame, (hand_position[0], hand_position[1]), (cup_position[0], cup_position[1]), (0, 0, 255), 2)
                cv2.line(frame, (int(hand_position[0]), int(hand_position[1])), (int(cup_position[0]), int(cup_position[1])), (0, 0, 255), 5)
                
                


    # for r in yolo_results:
    #     i = 0



    # print("----------------begin----------------------\n")
    # if yolo_results:
    #     print(yolo_results[0])
    # print("-----------------end---------------------\n")


    # exit_flag = False
    # #计算模块，我好像懂了，是不是两个results是类，boxes是个数
    # if yolo_results:
    #     # for box in yolo_results.pred_boxes:
    #     for r1 in yolo_results:
    #         for box in r1.boxes:
    #             if 'bottle' in box.name_handler:
    #                 box_flag = True
    #                 if box_flag and hand_flag:
    #                     distance = math.sqrt((box.center_handler[0]- hand_position[0])^2
    #                                         +(box.center_handler[1]- hand_position[1])^2)
    #                     text = f'the distance is {distance}'
    #                     print(text)
    #                     # cv2.putText(frame, text, (cx+20, cy+20), font, font_scale, font_color, font_thickness)
    #                     cv2.line(frame, box.center_handler, hand_position, (0,0,255), font_thickness)
                        

    #                     exit_flag = True  # 外面的for循环的设置退出标志，避免多个检测结果
    #                     break
    #             if exit_flag:
                    # break
    

    #文件之间的通信，失败
    # if current_cup_detect_flag and hand_flag:
    #     distance = math.sqrt((current_cup_position[0]- hand_position[0])^2
    #                 +(current_cup_position[1]- hand_position[1])^2)
    #     cv2.line(frame, current_cup_position, hand_position, (0,0,255), font_thickness)
    #     current_cup_detect_flag = False
    #     hand_flag = False
    #     #next frame
        


    box_flag = False
    hand_flag = False

        
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()