import cv2
import base64
import numpy as np
import json
    
import time
from ultralytics import YOLO


model = YOLO('./runs/detect/train/weights/last.pt')


card_values = {
    'C2': 2, 'C3': 3, 'C4': 4, 'C5': 5, 'C6': 6, 'C7': 7, 'C8': 8, 'C9': 9, 'C10': 10, 'CA': 11, 'CJ': 10, 'CK': 10, 'CQ': 10,
    'D2': 2, 'D3': 3, 'D4': 4, 'D5': 5, 'D6': 6, 'D7': 7, 'D8': 8, 'D9': 9, 'D10': 10, 'DA': 11, 'DJ': 10, 'DK': 10, 'DQ': 10,
    'H2': 2, 'H3': 3, 'H4': 4, 'H5': 5, 'H6': 6, 'H7': 7, 'H8': 8, 'H9': 9, 'H10': 10, 'HA': 11, 'HJ': 10, 'HK': 10, 'HQ': 10,
    'S2': 2, 'S3': 3, 'S4': 4, 'S5': 5, 'S6': 6, 'S7': 7, 'S8': 8, 'S9': 9, 'S10': 10, 'SA': 11, 'SJ': 10, 'SK': 10, 'SQ': 10
}


def from_b64(uri):
    '''
        Convert from b64 uri to OpenCV image
        Sample input: 'data:image/jpg;base64,/9j/4AAQSkZJR......'
    '''
    encoded_data = uri.split(',')[1]
    data = base64.b64decode(encoded_data)
    np_arr = np.fromstring(data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

    
def to_b64(img):
    '''
        Convert from OpenCV image to b64 uri
        Sample output: 'data:image/jpg;base64,/9j/4AAQSkZJR......'
    '''
    _, buffer = cv2.imencode('.jpg', img)
    img = base64.b64encode(buffer).decode('utf-8')
    
    return f"data:image/jpg;base64,{img}"


def detect(img):
    global model

    cards = []
    
    try:
        img = from_b64(img)
        results = model.predict(img, conf=0.6)
        
        for r in results:
            for box in r.boxes:

                b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                c = box.cls      # class index
                confidence = round(float(box.conf), 2)  # confidence score
                
                left, top, right, bottom = map(int, b.tolist())  # Convert numpy scalars to Python integers
                card = model.names[int(c)] # class name
                
                cards.append((left, top, right, bottom, card, confidence))
                
    except:
        print('No image found.')
    
    return json.dumps(cards)
