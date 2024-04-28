import cvzone
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import pyautogui as auto

cap = cv2.VideoCapture(0)

detector = FaceMeshDetector(maxFaces=1)

idList = [23, 24, 25, 26, 22, 110, 157, 158, 159, 160, 161, 130, 243]

plotY = LivePlot(500, 280, [25, 45], invert=True)

RatioList = []

blinkCounter = 0

counter = 0
while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()

    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 3, (0, 255, 0), 3, cv2.FILLED)

    leftUp = face[159]
    leftDown = face[23]
    leftLeft = face[130]
    leftRight = face[243]

    cv2.line(img, leftUp, leftDown, (0, 0, 255), 3)
    cv2.line(img, leftLeft, leftRight, (0, 0, 255), 3)
    lengthVer, _ = detector.findDistance(leftUp, leftDown)
    lengthHor, _ = detector.findDistance(leftLeft, leftRight)

    ratio = 100 * lengthVer / lengthHor
    RatioList.append(ratio)
    if len(RatioList) > 3:
        RatioList.pop(0)
    ratioAvg = sum(RatioList) / len(RatioList)
    print(ratioAvg)

    if ratioAvg < 34.5 :
        auto.press('space')

    cvzone.putTextRect(img, f'Blink Counter {blinkCounter}', (50, 44), scale=2, thickness=1, colorT=(0, 0, 0),
                       colorR=(0, 255, 0))

    cv2.imshow("stack", img)

    cv2.waitKey(1)
