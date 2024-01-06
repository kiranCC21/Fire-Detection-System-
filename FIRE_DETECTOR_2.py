import torch
import numpy as np
import cv2
from time import time
from ultralytics import YOLO

import supervision as sv

import smtplib

class FireDetection:

    def __init__(self, vid_path):

        self.vid_path = vid_path


        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        print("Using Device: ", self.device)

        self.model = self.load_model()

        self.CLASS_NAMES_DICT = self.model.model.names

        self.box_annotator = sv.BoxAnnotator(color=sv.ColorPalette.default(), thickness=3, text_thickness=3,
                                             text_scale=1.5)

    def load_model(self):

        model = YOLO("detector.pt")
        model.fuse()

        return model

    def predict(self, frame):

        results = self.model(frame)

        return results

    def plot_bboxes(self, results, frame):

        xyxys = []
        confidences = []
        class_ids = []


        for result in results[0]:
            class_id = result.boxes.cls.cpu().numpy().astype(int)

            if class_id == 0:
                xyxys.append(result.boxes.xyxy.cpu().numpy())
                confidences.append(result.boxes.conf.cpu().numpy())
                class_ids.append(result.boxes.cls.cpu().numpy().astype(int))
            if class_id ==1:
                xyxys.append(result.boxes.xyxy.cpu().numpy())
                confidences.append(result.boxes.conf.cpu().numpy())
                class_ids.append(result.boxes.cls.cpu().numpy().astype(int))


        # Setup detections for visualization

        detections = sv.Detections.from_ultralytics(results[0])

        frame = self.box_annotator.annotate(scene=frame, detections=detections)

        return frame, class_ids

    def __call__(self):

        cap = cv2.VideoCapture(self.vid_path)
        assert cap.isOpened()
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        frame_count = 0

        while True:

            start_time = time()

            ret, frame = cap.read()
            assert ret

            results = self.predict(frame)
            frame, class_ids = self.plot_bboxes(results, frame)

            if len(class_ids) > 0:
                print("Fire Detected")
            else:
                print("Smoke Detected")

            end_time = time()
            fps = 1 / np.round(end_time - start_time, 2)
            cv2.namedWindow("Fire Detection",cv2.WINDOW_NORMAL)
            #cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
            cv2.resizeWindow("Fire Detection",800,600)
            cv2.imshow('Fire Detection', frame)


            frame_count += 1

            if cv2.waitKey(5) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

