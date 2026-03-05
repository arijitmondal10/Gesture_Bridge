import cv2
import mediapipe as mp
import time
from gesture_predictor import predict_gesture
from text_to_speech import speak

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

previous_gesture = ""
last_time = 0
cooldown = 0.7   # seconds

while True:

    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            landmark_list = []

            for lm in hand_landmarks.landmark:
                landmark_list.append(lm.x)
                landmark_list.append(lm.y)
                landmark_list.append(lm.z)

            gesture = predict_gesture(landmark_list)

            current_time = time.time()

            # Allow different gestures immediately
            # Allow same gesture after cooldown
            if gesture != previous_gesture or current_time - last_time > cooldown:

                print("Gesture:", gesture)
                speak(gesture)

                previous_gesture = gesture
                last_time = current_time

            cv2.putText(frame, gesture, (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0,255,0), 2)

    cv2.imshow("GestureBridge", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()