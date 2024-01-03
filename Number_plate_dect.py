import cv2
import easyocr
import time
import pandas as pd
from openpyxl import Workbook


reader = easyocr.Reader(['en'])


cap = cv2.VideoCapture(0)


wb = Workbook()
ws = wb.active
ws.title = 'Number Plate Data'


ws.append(['Date', 'Time', 'Number Plate'])

prev_time = 0

while True:
   
    ret, frame = cap.read()

   
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

   
    edges = cv2.Canny(blur, 50, 150)

    
    dilated = cv2.dilate(edges, None, iterations=2)
    eroded = cv2.erode(dilated, None, iterations=1)

   
    contours, _ = cv2.findContours(eroded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w/float(h)

        
        if aspect_ratio > 1.6 and aspect_ratio < 3.6:
            
            number_plate = gray[y:y+h, x:x+w]

            
            text = reader.readtext(number_plate)

            
            text_str = ''
            for line in text:
                text_str += line[1] + ' '

            
            text_str = ' '.join(text_str.split())
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            ws.append([current_time, current_time, text_str])
            wb.save('./Numberplate/number_plate_data.xlsx')

            
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, text_str, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    
    curr_time = time.time()
    fps = 1/(curr_time - prev_time)
    prev_time = curr_time

  
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    cv2.imshow('Frame', frame)

   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()