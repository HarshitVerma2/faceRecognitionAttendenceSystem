#import tkinter
from tkinter import *
import cv2
import numpy
import face_recognition
import os
from datetime import datetime
import cx_Oracle

def doEncodings(images):
    encodeList =[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def putAttendence(name):
    sql_fetch = "select * from project"
    cursor.execute(sql_fetch)
    allRowData = cursor.fetchall()
    #print(allRowData)
    # inserting name
    namelist = []
    for i in allRowData:
        namelist.append(i[0])
    #print(namelist)
    if name not in namelist:
        sql_insert = "insert into project values(:c1,:c2)"
        now = datetime.now()
        dtString = now.strftime('%H:%M:%S')
        cursor.execute(sql_insert, [name, dtString])
    connection.commit()



def doCapture():
 cap=cv2.VideoCapture(0)

 while True:
     success , img =cap.read()
     imgS=cv2.resize(img,(0,0),None,0.25,0.25)
     imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

     facesCurFrame = face_recognition.face_locations(imgS)
     encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

     for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
         matches =face_recognition.compare_faces(encodeListKnown,encodeFace)
         faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
         print(faceDis)
         matchIndex=numpy.argmin(faceDis)

         if matches[matchIndex]:
             name =classNames[matchIndex].upper()
             print(name)
             y1,x2,y2,x1 =faceLoc
             y1, x2, y2, x1= y1*4,x2*4,y2*4,x1*4
             cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
             cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
             cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
             putAttendence(name)


     cv2.imshow('Webcam',img)
     cv2.waitKey(1)
     if cv2.waitKey(1) & 0xFF==ord('q'):# press q to exit video
         break
 cap.release()
 cv2.destroyAllWindows()

def closeProgram():
 cursor.close()
 connection.close()
 exit()

m=Tk()
m.geometry("1000x700")
m.resizable(width=0,height=0)
img=PhotoImage(file="bgImage.png")
label=Label(m,image=img)
label.place(x=0,y=0)
button1=Button(m,text='Capture Video',font=('Airal Bold',18),bg='blue', command=doCapture)
button1.place(x=450,y=600)

button2=Button(m,text='Close',font=('Airal Bold',18),bg='blue',command=closeProgram)
button2.place(x=500,y=655)

connection=cx_Oracle.connect("harshitverma/password@localhost/XE")
cursor=connection.cursor()
path = 'atImage'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

encodeListKnown = doEncodings(images)
print('Encoding Complete')

m.mainloop()







