import cv2
platecascade = cv2.CascadeClassifier("C:\\Users\\ojhaa\\Desktop\\NUMBER-PLATE\\Numberplate.xml")
minArea = 500 
cap = cv2.VideoCapture(0)
count = 0
while True:
    success,img=cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    numberplate = platecascade.detectMultiScale(imgGray,1.1,4)
    for(x,y,w,h) in numberplate:
        area = w*h 
        if area >minArea:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.putText(img,"NUMBER PLATE",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            imgRoi = img[y:y+h,x:x+w]
            cv2.imshow("ROI",imgRoi)
    cv2.imshow("result",img)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("C:\\Users\\ojhaa\\Desktop\\NUMBER-PLATE\\Numberplate"+str(count)+".jpg",imgRoi)
        cv2.rectangle(img,(0,200),(640,300),(255,0,0),cv2.FILLED)
        cv2.putText(img,"Scan Saved",(15,265),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,255),2)
        cv2.imshow("Result",imgRoi)
        cv2.waitKey(500)
        count+=1