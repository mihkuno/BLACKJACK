import cv2
import base64
import numpy as np
    
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
        Sample input: 'timestamp, card_stack, data:image/jpg;base64, /9j/4AAQSkZJR......'
    '''
    
    encoded_data = uri.split(',')
    
    try:
        
        img = encoded_data[-1]
        img = base64.b64decode(img)
        img = np.fromstring(img, np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        
        timestamp = int(encoded_data[0])
        card_stack = encoded_data[1:-2]
        
        if card_stack == ['']:
            card_stack = []
            
        if timestamp == 0:
            timestamp = int(time.time())
    
        return timestamp, card_stack, img
    except:
        return None


def to_b64(timestamp, card_stack, img):
    '''
        Convert from OpenCV image to b64 uri
        Sample output: 'data:image/jpg;base64,/9j/4AAQSkZJR......'
    '''
    _, buffer = cv2.imencode('.jpg', img)
    img = base64.b64encode(buffer).decode('utf-8')
    
    return f"{timestamp},{','.join(card_stack)},data:image/jpg;base64,{img}"


def detect(data):
    global model
    global card_values
    
    data = from_b64(data)
    
    if data is None:        
        return ''
    
    timestamp, card_stack, img = data
                
            
    # calculate card count
    card_count = sum([card_values[card] for card in card_stack])
    
    # Count the number of elements in list1 that are also in list2
    ace_cards = ['CA', 'DA', 'HA', 'SA']
    ace_count = sum(1 for elem in ace_cards if elem in card_stack)
        
    # while greater than 21, check for aces and subtract 9 for each ace
    while card_count > 21 and ace_count > 0:
        card_count -= 10
        ace_count -= 1

       
    if timestamp != -1 and timestamp <= int(time.time()):           
        timestamp = -1
        card_stack = []
        card_count = 0
      
        
    elif timestamp == -1 and card_count >= 21:            
        # Schedule the function to be executed after 3 seconds
        timestamp = int(time.time() + 3)
      
      
    if timestamp != -1 and timestamp > int(time.time()):
        
        # if card count is equals 21, display blackjack in green text for 3 seconds
        if card_count == 21:
            cv2.putText(img, 'Blackjack', (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2)
        
        # else if card count is still greater than 21, display bust in red text for 3 seconds
        elif card_count > 21:
            cv2.putText(img, 'Bust', (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 2)
           
    else:
        results = model.predict(img, conf=0.85)

        for r in results:
            for box in r.boxes:
                
                b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                c = box.cls      # class index
                
                left, top, right, bottom = map(int, b.tolist())  # Convert numpy scalars to Python integers
                card = model.names[int(c)] # class name
                
                # note the card in the card stack
                if not card in card_stack:
                    card_stack.append(card)
                
                
                # draw square and text on image
                cv2.putText(img, card, (left, top-10), cv2.FONT_HERSHEY_DUPLEX, 0.4, (254 ,155, 162), 2)
                cv2.rectangle(img, (left, top), (right, bottom), (254 ,155, 162), 2)
            

    # display card count
    cv2.putText(img, f'Card Count: {card_count}', (10, 100), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
    
    # display card stack
    cv2.putText(img, f'Card Stack {card_stack}:', (10, 150), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
    

    return to_b64(timestamp, card_stack, img)
    