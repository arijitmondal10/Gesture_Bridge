import cv2
import mediapipe as mp
import time
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

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

previous_gesture = ""
gesture = ""

gesture_start_time = None
GESTURE_HOLD_TIME = 1.0   # seconds

while True:

    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    detected_gesture = ""

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            landmark_list = []

            for lm in hand_landmarks.landmark:
                landmark_list.extend([lm.x, lm.y, lm.z])

            # Predict gesture
            detected_gesture = predict_gesture(landmark_list)

            # Draw landmarks
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    # Start timer when gesture appears
    if detected_gesture != "":
        if gesture_start_time is None:
            gesture_start_time = time.time()

        elapsed_time = time.time() - gesture_start_time

        # If gesture held long enough
        if elapsed_time > GESTURE_HOLD_TIME:

            gesture = detected_gesture

            if gesture != previous_gesture:
                print("Gesture:", gesture)
                speak(gesture)

                previous_gesture = gesture

            gesture_start_time = None

    else:
        gesture_start_time = None

    # Display gesture
    cv2.putText(
        frame,
        f"Gesture: {gesture}",
        (50, 70),
        cv2.FONT_HERSHEY_DUPLEX,
        1,
        (0, 0, 0),
        2
    )

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