import cv2
import numpy as np
from pyzbar.pyzbar import decode
import psycopg2
from config import host, user, password, db_name


cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
delay = 1

while True:

    success, img = cap.read()

    connection = psycopg2.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db_name
                )

    for barcode in decode(img):

        myData = barcode.data.decode('utf-8')
        
        with connection.cursor() as cursor:
            cursor.execute(
                f"select * from Студентики where id = {myData};"
            )
            Reslt = cursor.fetchone()
            print(f'id: {Reslt}')
            cv2.waitKey(2000)

        pts = np.array([barcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(255,0,255),5)
        pts2 = barcode.rect
        cv2.putText(img,f'{Reslt}',(50, 50) ,cv2.FONT_HERSHEY_COMPLEX, 0.9,(255,0,255),2)

    
       
    if cv2.waitKey(delay) & 0xFF == ord('q'):
        connection.close()
        break
    
    
    
    

    cv2.imshow('Result',img)
    cv2.waitKey(1)
    
    