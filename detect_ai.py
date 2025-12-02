import threading
import time

import cv2
from ultralytics import YOLO


class DetectAI:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.frame = None
        self.can_run = True

        self.type = 0
        self.ai_frame = None
        self.box = None
        self.new_box = False

    def add_frame(self, frame):
        self.frame = frame

    def start_detection(self):
        self.can_run = True

        def detection():
            while self.can_run:
                if self.frame is not None:
                    results = self.model.predict(self.frame.copy(), conf=0.5, verbose=False)
                    for r in results:
                        for box in r.boxes:
                            target_box = box.xyxy[0]
                            self.box = (int(target_box[0]), int(target_box[1]),
                                        int(target_box[2]), int(target_box[3]))

                            self.ai_frame = frame
                            self.new_box = time.time()
                            self.type = 0
                            break
                        break
                time.sleep(0.01)

        threading.Thread(target=detection).start()

    def start_tracking(self):
        self.can_run = True

        def tracking():
            _tracker = cv2.TrackerKCF().create()
            _is_init = False
            while self.can_run:
                if (self.ai_frame is not None) and (time.time() - self.new_box < 2):
                    if not _is_init or time.time() - self.new_box > 0.5:
                        (x1, y1, x2, y2) = self.box
                        box_xywh = tuple(int(round(x)) for x in (x1, y1, x2 - x1, y2 - y1))
                        _tracker.init(self.ai_frame, box_xywh)
                        _is_init = True

                    success, bbox = _tracker.update(self.frame)
                    if success:
                        (x, y, w, h) = [int(v) for v in bbox]
                        self.type = 1
                        self.box = (int(x), int(y), int(x + w), int(y + h))

                time.sleep(0.01)

        threading.Thread(target=tracking).start()

    def get_box(self):
        return self.box

    def stop(self):
        self.can_run = False


def decorate_frame(frame, detector):
    ai_box = detector.get_box()
    if ai_box is not None:
        (x1, y1, x2, y2) = ai_box
        return cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0) if detector.type == 0 else (255, 0, 0), 3)
    return frame


if __name__ == '__main__':

    detector = DetectAI("yolov12n-face_ncnn_model")
    detector.start_detection()
    detector.start_tracking()

    camera = cv2.VideoCapture(0)
    while True:
        _, frame = camera.read()
        detector.add_frame(frame)
        display_frame = decorate_frame(frame, detector)
        cv2.imshow("UAV Camera", display_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    detector.stop()
    time.sleep(1)
    cv2.destroyAllWindows()
