import os
import cv2
import cvzone
from cvzone.PoseModule import PoseDetector

def get_shoulder_width_from_user():
    while True:
        try:
            shoulder_width = float(input("Enter your shoulder width in inches: "))
            return shoulder_width
        except ValueError:
            print("Please enter a valid number.")

# Function to dynamically resize the shirt based on user's shoulder width
def resize_shirt(imgShirt, shoulderWidth, shirtRatioHeightWidth):
    shirtWidth = int(shoulderWidth * 8)  # Adjust scale factor as needed
    shirtHeight = int(shirtWidth * shirtRatioHeightWidth)
    imgShirt = cv2.resize(imgShirt, (shirtWidth, shirtHeight))
    return imgShirt

# Get the user's shoulder width
user_shoulder_width = get_shoulder_width_from_user()

cap = cv2.VideoCapture(0)
detector = PoseDetector()

shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)

imageNumber = 0

imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip horizontally for mirror view

    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

    if lmList:
        lm11 = lmList[11][1:3]  # Left shoulder
        lm12 = lmList[12][1:3]  # Right shoulder

        # Calculate shoulder width in pixels
        shoulderWidth = abs(lm11[0] - lm12[0])
        print(f"Shoulder Width: {shoulderWidth}")

        # Load and resize shirt based on user's shoulder width
        try:
            imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
            imgShirt = resize_shirt(imgShirt, user_shoulder_width, 1.32)  # Adjust shirt ratio as needed

            # Adjust offset based on your body and shirt positioning
            offsetX = int(shoulderWidth * 0.5)  # Adjust as needed
            offsetY = int(shoulderWidth * 0.5)  # Adjust as needed

            img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offsetX, lm12[1] - offsetY))

            img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
            img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

            # Button interactions based on hand positions
            if lmList[16][1] < 300:
                counterRight += 1
                if counterRight * selectionSpeed > 360:
                    counterRight = 0
                    if imageNumber < len(listShirts) - 1:
                        imageNumber += 1

            elif lmList[15][1] > 900:
                counterLeft += 1
                if counterLeft * selectionSpeed > 360:
                    counterLeft = 0
                    if imageNumber > 0:
                        imageNumber -= 1

        except Exception as e:
            print(f"Error overlaying image: {e}")

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
