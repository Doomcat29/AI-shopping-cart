from ultralytics import YOLO
import cv2
import serial
import time
import keyboard 
port = "COM4"  #("/dev/ttyUSB0" on macOS)
baud_rate = 9600

model = YOLO("yolov8n.pt")
arduino = serial.Serial(port, baud_rate)
basket_list = ["empty"]

# Open camera (1 = default webcam for Sams MacBook)
cap = cv2.VideoCapture(0)

filterLables = []
with open('labels.txt','r') as f:
    content = f.read()
    filterLables = content.splitlines()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection
    results = model(frame, stream=True)  # stream=True yields results in real-time

    # Loop through results and draw boxes
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            cls = int(box.cls[0])
            conf = box.conf[0]
            label = r.names[cls]
            
            if label in filterLables:
                if "apple" in label:
                   print("apple price $0.75/lb")
                if "banana" in label:
                   print("banana price $0.54/lb")
                if "orange" in label:
                   print("orange price $1.33/lb")

            # Draw rectangle + label
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (int(x1), int(y1) - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            cv2.putText(frame, f"Basket List: {basket_list}", (425,50),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            
            if label == "apple":
                command = "ON"
                arduino.write((command + "\n").encode('utf-8'))
                time.sleep(.050)
                command = "OFF"
                arduino.write((command + "\n").encode('utf-8'))

    cv2.imshow("YOLO Live Detection", frame)
    if cv2.waitKey(1) == 27:  # ESC key to stop
        break
cap.release()
cv2.destroyAllWindows()
