import cv2
import mediapipe as mp
import csv

gesture_label = input("Enter gesture name: ")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

file = open("dataset/gesture_dataset.csv", "a", newline="")
writer = csv.writer(file)

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

            landmark_list.append(gesture_label)

            writer.writerow(landmark_list)

            print("Sample collected")

    cv2.imshow("Dataset Collection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

file.close()
cap.release()
cv2.destroyAllWindows()