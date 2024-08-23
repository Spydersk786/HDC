import cv2
import os
from camera import get_video_capture
from motion_detection import detect_motion
from human_detection import detect_humans
from alerts import send_alert

def main():
    alert_url = "http://127.0.0.1:5000/api/alert"
    cfg_path = "yolov3.cfg"
    weights_path = "yolov3.weights"
    
    if not os.path.isfile(cfg_path):
        raise FileNotFoundError(f"Configuration file not found: {cfg_path}")
    if not os.path.isfile(weights_path):
        raise FileNotFoundError(f"Weights file not found: {weights_path}")

    # Load YOLO
    net = cv2.dnn.readNet(weights_path, cfg_path)
    layer_names = net.getLayerNames()
    print("Layer names:", layer_names)
    out_layer_indices = net.getUnconnectedOutLayers()
    print("Unconnected out layers:", out_layer_indices)
    
    # Adjust indexing for flat array
    output_layers = [layer_names[i - 1] for i in out_layer_indices]
    print("Output layers:", output_layers)

    # Load COCO names
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    cap = get_video_capture()
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    while cap.isOpened():
        contours = detect_motion(frame1, frame2)
        boxes, confidences, class_ids, indexes = detect_humans(frame1, net, output_layers, classes)
        
        for contour in contours:
            if cv2.contourArea(contour) < 500:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            send_alert("Motion detected!",alert_url)
        
        for i in indexes:
            x, y, w, h = boxes[i[0]]
            label = str(classes[class_ids[i[0]]])
            color = (0, 255, 0)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame1, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            send_alert("Human detected!",alert_url)

        cv2.imshow('Surveillance Feed', frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

