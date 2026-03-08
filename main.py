import cv2
import mediapipe as mp
from gesture_predictor import predict_gesture
from text_to_speech import speak

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

previous_gesture = ""

while True:

    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    gesture = ""

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            landmark_list = []

            for lm in hand_landmarks.landmark:
                landmark_list.append(lm.x)
                landmark_list.append(lm.y)
                landmark_list.append(lm.z)

            # Predict gesture
            gesture = predict_gesture(landmark_list)

            # Speak only when gesture changes
            if gesture != previous_gesture and gesture != "":

                print("Gesture:", gesture)
                speak(gesture)

                previous_gesture = gesture

            # Draw hand landmarks
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    # Display gesture text
    cv2.putText(
        frame,
        f"Gesture: {gesture}",
        (50, 70),
        cv2.FONT_HERSHEY_DUPLEX,
        1,
        (0, 0, 0),
        2
    )

    # Project title
    cv2.putText(
        frame,
        "GestureBridge AI",
        (20, 450),
        cv2.FONT_HERSHEY_DUPLEX,
        0.7,
        (0, 0, 0),
        2
    )

    cv2.imshow("GestureBridge", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()