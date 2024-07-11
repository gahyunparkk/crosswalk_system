import cv2
import torch
import time
import threading
import pygame
import serial
import numpy as np

pygame.mixer.init()

warning_sound = pygame.mixer.Sound("warning_guide.mp3")
cross_sound = pygame.mixer.Sound("cross_guide.mp3")

def warning_guide():
    pygame.mixer.Sound.play(warning_sound)
def cross_guide():
    pygame.mixer.Sound.play(cross_sound)

model = torch.hub.load('ultralytics/yolov5', 'custom', path='runs/train/exp/weights/best.pt')

cap = cv2.VideoCapture(0)
ser = serial.Serial('COM9', 115200, timeout=1)

def capture_frame():
    ret, frame = cap.read()
    if not ret:
        return None
    return frame

def detect_objects(frame):
    results = model(frame)
    objects = results.xyxy[0].cpu().numpy()
    objects = sorted(objects, key=lambda x: (x[0], x[1]))
    return objects

def monitor_serial():
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            print(f'Received: {data}')

            if data == '1':
                previous_frame = capture_frame()
                previous_results = detect_objects(previous_frame)
                time.sleep(0.5)#0.5초
                current_frame = capture_frame()
                current_results = detect_objects(current_frame)

                print(f'Previous frame detected {len(previous_results)} objects.')
                print(f'Current frame detected {len(current_results)} objects.')

                if len(current_results) == 0:
                    threading.Thread(target=cross_guide).start()
                    continue

                significant_change = False
                all_still = True

                # 좌표 비교
                for i in range(min(len(previous_results), len(current_results))):
                    p_xmin, p_ymin, p_xmax, p_ymax, _, p_cls = previous_results[i]
                    c_xmin, c_ymin, c_xmax, c_ymax, _, c_cls = current_results[i]

                    if model.names[int(p_cls)] == 'car' and model.names[int(c_cls)] == 'car':
                        diff_xmin = c_xmin - p_xmin
                        diff_ymin = c_ymin - p_ymin
                        diff_xmax = c_xmax - p_xmax
                        diff_ymax = c_ymax - p_ymax

                        print(f'변화된 물체 ID: {i}, 좌표 변화: (xmin: {diff_xmin:.0f}, ymin: {diff_ymin:.0f}, xmax: {diff_xmax:.0f}, ymax: {diff_ymax:.0f})')

                        if abs(diff_xmin) >= 70 or abs(diff_ymin) >= 70 or abs(diff_xmax) >= 70 or abs(diff_ymax) >= 70:
                            significant_change = True
                            break
                        

                if significant_change:
                    threading.Thread(target=warning_guide).start()
                else:
                    threading.Thread(target=cross_guide).start()

def display_frame():
    while True:
        frame = capture_frame()
        if frame is None:
            break

        results = detect_objects(frame)
        for i, (xmin, ymin, xmax, ymax, confidence, cls) in enumerate(results):
            label = model.names[int(cls)]
            cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
            cv2.putText(frame, f'{label} {confidence:.2f}', (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

threading.Thread(target=monitor_serial, daemon=True).start()
threading.Thread(target=display_frame, daemon=True).start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    cap.release()
    cv2.destroyAllWindows()
    ser.close()
