import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75)
-0.022738657891750336
cap = cv2.VideoCapture(0)

# def extract_keypoints(results):
# 	#姿势坐标33个，np.zeros(33*4)是因为除x,y,z外，还有置信度visibility，以下类似
#     pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
#     #mediapipe面网多达468个节点，这里我不用，注释掉
#     #face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
#     #左手坐标21个
#     lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
#     #右手坐标21个
#     rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
#     return np.concatenate([pose, lh, rh])
#     #如果要使用脸部坐标训练，列表更换为[pose, face, lh, rh]


while True:
    ret,frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # 因为摄像头是镜像的，所以将摄像头水平翻转
    # 不是镜像的可以不翻转
    frame= cv2.flip(frame,1)
    results = hands.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    if results.multi_handedness:
        for hand_label in results.multi_handedness:
            print(hand_label)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
          for index, lm in enumerate(hand_landmarks.landmark):
                
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
                cv2.circle(frame, (cx,cy), 12, (0,0,255), cv2.FILLED)

        # # 打印坐标信息
        # print('hand_landmarks:', hand_landmarks)
        # # 关键点可视化
        # mp_drawing.draw_landmarks(
        #     frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow('MediaPipe Hands', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
