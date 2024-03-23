from ultralytics import YOLO


model = YOLO('./runs/detect/train3/weights/best.pt', verbose=True)

results = model.predict(source="0", show=True, conf=0.8, half=True)

print(results)