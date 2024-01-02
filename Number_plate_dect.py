import cv2
import easyocr
import matplotlib.pyplot as mp
import csv
import pandas 

img = cv2.imread('0.jpg')
reader = easyocr.Reader(['en'],gpu=True)
result = reader.readtext(img,detail=1,paragraph=False)
# print(result)

for cord,text,confi in result:
    (topleft,topright,bottomright,bottomleft )=cord
    tx,ty =topleft[0],topleft[1]
    bx,by =bottomright[0],bottomright[1]
    
    cv2.rectangle(img ,(tx,ty),(bx,by),(0,255,255),5)
    cv2.putText(img , text, (tx-100,ty-50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),4)
    print(text)
    
mp.imshow(img)
mp.show()       



