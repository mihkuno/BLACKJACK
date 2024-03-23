from ultralytics import YOLO



# Build a YOLOv9c model from scratch
model = YOLO('yolov9c.yaml')

# Build a YOLOv9c model from pretrained weight
model = YOLO('yolov9c.pt')

# Display model information (optional)
model.info()


# Train the model for 100 epochs
results = model.train(data='blackjack.yaml', epochs=30, imgsz=640, verbose=True, batch=-1)