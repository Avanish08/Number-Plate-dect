import cv2
import easyocr
import time
import pandas as pd
from openpyxl import Workbook
import os

# Initialize EasyOCR reader for English
reader = easyocr.Reader(['en'])

# Start capturing video from the first camera
cap = cv2.VideoCapture(0)

# Create Excel workbook and worksheet
wb = Workbook()
ws = wb.active
ws.title = 'Number Plate Data'
ws.append(['Date', 'Time', 'Number Plate', 'Image Path'])

# Create a directory to store the captured images
if not os.path.exists('./Numberplate/images'):
    os.makedirs('./Numberplate/images')

prev_time = 0

while True:
    ret, frame = cap.read()

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges using Canny edge detector
    edges = cv2.Canny(blur, 50, 150)

    # Dilate and erode edges to improve contour detection
    dilated = cv2.dilate(edges, None, iterations=2)
    eroded = cv2.erode(dilated, None, iterations=1)

    # Find contours in the eroded image
    contours, _ = cv2.findContours(eroded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)

        # Check if the aspect ratio is within the expected range for a number plate
        if aspect_ratio > 1.6 and aspect_ratio < 3.6:
            # Extract the region containing the number plate
            number_plate = gray[y:y + h, x:x + w]

            # Use EasyOCR to read the number plate
            text = reader.readtext(number_plate)

            # Extract text from OCR results
            text_str = ''
            for line in text:
                text_str += line[1] + ' '

            # Clean the extracted text
            text_str = ' '.join(text_str.split())

            if text_str:  # Only save if a valid number plate is detected
                # Save the current time and the detected number plate in the Excel sheet
                current_time = time.strftime('%Y-%m-%d %H:%M:%S')

                # Save image with detected number plate
                image_filename = f"./Numberplate/images/{current_time.replace(':', '-')}.jpg"
                cv2.imwrite(image_filename, frame)

                # Append data to the Excel sheet
                ws.append([current_time, current_time, text_str, image_filename])
                wb.save('./Numberplate/number_plate_data.xlsx')

                # Draw rectangle around detected number plate and display text
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, text_str, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Calculate FPS (frames per second)
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # Display FPS on the frame
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # Show the frame
    cv2.imshow('Frame', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close any open windows
cap.release()
cv2.destroyAllWindows()
