import cv2
import threading
from ultralytics import YOLO


model = YOLO('./runs/detect/train3/weights/last.pt')
cap = cv2.VideoCapture(0)


card_values = {
    'C2': 2, 'C3': 3, 'C4': 4, 'C5': 5, 'C6': 6, 'C7': 7, 'C8': 8, 'C9': 9, 'C10': 10, 'CA': 11, 'CJ': 10, 'CK': 10, 'CQ': 10,
    'D2': 2, 'D3': 3, 'D4': 4, 'D5': 5, 'D6': 6, 'D7': 7, 'D8': 8, 'D9': 9, 'D10': 10, 'DA': 11, 'DJ': 10, 'DK': 10, 'DQ': 10,
    'H2': 2, 'H3': 3, 'H4': 4, 'H5': 5, 'H6': 6, 'H7': 7, 'H8': 8, 'H9': 9, 'H10': 10, 'HA': 11, 'HJ': 10, 'HK': 10, 'HQ': 10,
    'S2': 2, 'S3': 3, 'S4': 4, 'S5': 5, 'S6': 6, 'S7': 7, 'S8': 8, 'S9': 9, 'S10': 10, 'SA': 11, 'SJ': 10, 'SK': 10, 'SQ': 10
}

card_stack = []

is_display_result = False

def reset_display_result():
    global is_display_result
    global card_stack
    is_display_result = False
    card_stack.clear()


while True:
    _, img = cap.read()
    
    
    if not is_display_result:
        # BGR to RGB conversion is performed under the hood
        # see: https://github.com/ultralytics/ultralytics/issues/2575
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
            
            
            # calculate card count
            card_count = sum([card_values[card] for card in card_stack])
            
            # Count the number of elements in list1 that are also in list2
            ace_cards = ['CA', 'DA', 'HA', 'SA']
            ace_count = sum(1 for elem in ace_cards if elem in card_stack)
                
            # while greater than 21, check for aces and subtract 9 for each ace
            while card_count > 21 and ace_count > 0:
                card_count -= 10
                ace_count -= 1


            # check if card count is equals 21 or greater than 21
            if card_count == 21 or card_count > 21:
                is_display_result = True
                
                # Schedule the function to be executed after 5 seconds
                timer = threading.Timer(3, reset_display_result)
                timer.start()
        
        
    elif is_display_result:
        # if card count is equals 21, display blackjack in green text for 3 seconds
        if card_count == 21:
            cv2.putText(img, 'Blackjack', (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2)
        
        # else if card count is still greater than 21, display bust in red text for 3 seconds
        elif card_count > 21:
            cv2.putText(img, 'Bust', (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 2)
        
    
    # display card count
    cv2.putText(img, f'Card Count: {card_count}', (10, 100), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
    
    # display card stack
    cv2.putText(img, f'Card Stack {str(card_stack)}:', (10, 150), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
        
    cv2.imshow('Blackjack Counter', img)     
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break


cap.release()
cv2.destroyAllWindows()
