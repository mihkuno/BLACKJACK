import cv2
import base64
import numpy as np
import json
from ultralytics import YOLO

card_model = YOLO('./model/detect/blackjack-model-final/weights/best.pt')   

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
    global card_model, corner_model, orientation_model, orientation_names

    cards = []
    
    try:
        
        # get the converted image from the b64 uri
        img = from_b64(img)
                
        # get whole card detection results
        result_card = card_model.track(img, conf=0.65, persist=True, tracker="botsort.yaml")
        
        
        for r in result_card:
            for box in r.boxes:
                id = box.id.item()
                b = box.xyxy[0]                         # get box coordinates in (left, top, right, bottom) format
                c = box.cls                             # class index
                confidence = round(float(box.conf), 2)  # confidence score
                left, top, right, bottom = map(int, b.tolist())  # Convert numpy scalars to Python integers
                
                print(id)
                
                card = card_model.names[int(c)] # class name
                cards.append((left, top, right, bottom, card, confidence, id))
        
    except:
        print('No image found.')
    
    return json.dumps(cards)
