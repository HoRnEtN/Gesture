import cv2
import mediapipe as mp
import pyautogui

# Initialize VideoCapture and Hand tracking
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

# Screen size
screen_width, screen_height = pyautogui.size()
index_y = 0

while True:
    _, frame = cap.read()
    if not _:
        print("Error: Failed to capture frame")
        continue
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hands
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            # Draw landmarks on the frame
            drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
            
            # Calculate the movement since the last frame
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=14, color=(0, 255, 255), thickness=3)
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y


            # Move the mouse cursor
            pyautogui.moveTo(index_x, index_y)
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                # Check for the thumb landmark using its index (4)
                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 0), thickness=2)
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    print('outside', abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 20:
                        pyautogui.click()
                        pyautogui.sleep(1)

    # Display the frame with landmarks and cursor
    cv2.imshow("Virtual Mouse", frame)
    key = cv2.waitKey(1)
    if key == 27:  # Press ESC to exit
        break

# Release the resources
cap.release()
cv2.destroyAllWindows()
