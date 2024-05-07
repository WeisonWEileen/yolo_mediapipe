import cv2
import mediapipe as mp
import pickle 

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75)

cap = cv2.VideoCapture(0)
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

    frame_keypoints = []


            
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        # print(len(hand_landmarks))
        print('hand_landmarks:' ,hand_landmarks)
        # 关键点可视化
        mp_drawing.draw_landmarks(
            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        

    frame_keypoints = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for p in range(21):
                #print(p, ':', hand_landmarks.landmark[p].x, hand_landmarks.landmark[p].y)
                # pxl_x = int(round(frame0.shape[1]*hand_landmarks.landmark[p].x))
                # pxl_y = int(round(frame0.shape[0]*hand_landmarks.landmark[p].y))
                pxl_x = (hand_landmarks.landmark[p].x)
                pxl_y = (hand_landmarks.landmark[p].y)
                pxl_z = (hand_landmarks.landmark[p].z)
                kpts = [pxl_x, pxl_y, pxl_z]
                frame_keypoints.append(kpts)
        # for p_x = hand_landmarks
                
        
        with open('frame_keypoints.pkl', 'wb') as f:
            pickle.dump(frame_keypoints, f)
    cv2.imshow('MediaPipe Hands', frame)



    if cv2.waitKey(1) & 0xFF == 27:
        break




cap.release()
