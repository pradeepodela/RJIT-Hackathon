import cv2
import numpy as np
import face_recognition
import os
import time
import requests
global flag
import telepot
# import datetime
from send import senddata
# current_time = datetime.datetime.now()
flag = 0
bot = telepot.Bot('5981392455:AAHbYGVYJ1P9XntMvDfPDWzVbrRd-Lb7jJs')
path = 'Images'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)
# import datetime

def findEncodings(images):
    encodeList = []


    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
encodeListKnown = findEncodings(images)
print('Encoding Completed')





cap = cv2.VideoCapture(1)

def fcr(img):
    time_stamp = str(time.time())
    success, img = cap.read()
    

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)
        # print(matches[matchIndex])
        if matches[matchIndex]:
            global flag
            flag = flag + 1
            name = classNames[matchIndex].upper()
            
            

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            img = cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            img = cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            if flag == 8:
                cv2.imwrite(f'detectedimages/{time_stamp}_VNRVJIET{name}.png',img)
                # bot.sendPhoto(5053711674, photo=open(f'detectedimages/{time_stamp}_VNRVJIET{name}.png', 'rb'))
                data = f'Accused Found!!\n\n-------------------------------\nName: {name}\nFound at: University Rajasthan College \nLocation: https://www.google.com/maps/@30.755755,76.7913552,15z \n-------------------------------'
                # bot.sendMessage(5053711674, data)
                senddata(f'detectedimages/{time_stamp}_VNRVJIET{name}.png',data)


    

    # cv2.imshow('Webcam', img)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    #     cap.release()
    #     cv2.destroyAllWindows()

if __name__ == '__main__':
    while True:
        time_stamp = str(time.time())
        success, img = cap.read()
        fcr(img)
        

        # imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        # imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        # facesCurFrame = face_recognition.face_locations(imgS)
        # encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        # for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        #     matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        #     faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        #     matchIndex = np.argmin(faceDis)
        #     # print(matches[matchIndex])
        #     if matches[matchIndex]:
        #         flag = flag + 1
        #         name = classNames[matchIndex].upper()
                
                

        #         y1, x2, y2, x1 = faceLoc
        #         y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        #         img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        #         img = cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        #         img = cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        #         if flag == 8:
        #             cv2.imwrite(f'detectedimages/{time_stamp}_VNRVJIET{name}.png',img)
        #             bot.sendPhoto(5053711674, photo=open(f'detectedimages/{time_stamp}_VNRVJIET{name}.png', 'rb'))
        #             data = f'Accused Found!!\n\n-------------------------------\nName: {name}\nTime: {current_time}\nFound at: VNRVJIET\nLocation: https://www.google.com/maps?q=17.5368066,78.3844026&z=17&hl=en \n-------------------------------'
        #             bot.sendMessage(5053711674, data)

        #             print('sending request')
        #             requests.get('http://192.168.137.168//ledon')
        #             flag = 0
        

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
