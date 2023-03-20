import cv2
import numpy as np
import face_recognition
import streamlit as st
import os
from datetime import datetime
import pandas as pd
import smtplib
from email.message import EmailMessage
import imghdr
import pytesseract
import telepot
from app import fcr
path = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

pytesseract.pytesseract.tesseract_cmd = path
bot = telepot.Bot('6231514727:AAF6YqiiJ6zxSFsKxwtp3hcjC8_rJ8WUFOg')
email = ''
path = './Training_images'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    encodeList = []


    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# def email_me(frame,mail,time):
#     Sender_Email = "odelapradeep12@gmail.com"
#     Reciever_Email = mail
#     Password = '@Pradeep9246'
#     img = frame
#     newMessage = EmailMessage()                         
#     newMessage['Subject'] = "Accused found !!!!!!!" 
#     newMessage['From'] = Sender_Email                   
#     newMessage['To'] = Reciever_Email                   
#     newMessage.set_content(f'The following accused found at Time {time} at area Hyderabad here is the picture of accused ') 

#     with open(img, 'rb') as f:
#         image_data = f.read()
#         image_type = imghdr.what(f.name)
#         image_name = f.name

#     newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        
#         smtp.login(Sender_Email, Password)              
#         smtp.send_message(newMessage)
#     print('success msg went')


def email_me(frame,mail,time):
    # mail = 
    bot.sendPhoto(5053711674, photo=open(frame, 'rb'))
    data = f'Accused Found!!\n\n-------------------------------\nName: {name}\nTime: \nFound at: VNRVJIET\nLocation: https://www.google.com/maps?q=17.5368066,78.3844026&z=17&hl=en \n-------------------------------'
    bot.sendMessage(5053711674, data)
    print('Sucessfully sent the image to telegrm')

def markAttendance(name,image,email):
    with open('data.csv', 'r+') as f:
        myDataList = f.readlines()


        nameList = []
        for line in myDataList:
            df = pd.read_csv(r'data.csv')
            entry = line.split(',')
            nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M')
                n_input = name
                TIME = df[(df == n_input).any(1)].stack()[lambda x: x != n_input].unique()
                
                if dtString not in list(TIME):
                   
                    f.writelines(f'\n{name},{dtString}')
                    
                    time_now = dtString.replace(':','.')
                    try:
                        cv2.imwrite(f'accused_pics/{time_now}.png',image)
                        email_me(f'accused_pics/{time_now}.png',email,dtString)
                    except :
                        print('could not save image')



encodeListKnown = findEncodings(images)
print('Encoding Completed')

# st.markdown('**Accused detecation started**')
def atn(frame,eml):
    
            
    return frame

def get_text(frame):
    print('Trying to extract text...')
    text = pytesseract.image_to_string(frame)
    if text == '':
        print('No text found')
    return text
   




