# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os.path as path
import argparse

parser = argparse.ArgumentParser()  # 创建ArgumentParser()对象
parser.add_argument("-a", "--algorithm", help="m (or nothing) for meanShift and c for camshift")
# 添加参数，这里意思是：在命令窗口输入时加入”-a XXX“ 可以采用不同的苏昂啊
args = vars(parser.parse_args())  # 解析添加参数
font = cv2.FONT_HERSHEY_SIMPLEX


class Pedestrian():
    def __init__(self, id, frame, track_window):
        self.id = int(id)
        x, y, w, h = track_window
        self.track_window = track_window
        self.roi = cv2.cvtColor(frame[y:y + h, x:x + w], cv2.COLOR_BGR2HSV)
        roi_hist = cv2.calcHist([self.roi], [0], None, [16], [0, 180])
        self.roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

        self.kalman = cv2.KalmanFilter(4, 2)
        self.kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        self.kalman.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
        self.kalman.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                                               np.float32) * 0.03
        self.measurement = np.array((2, 1), np.float32)
        self.prediction = np.zeros((2, 1), np.float32)
        self.term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
        self.center = None
        self.update(frame)

    def __del__(self):
        print("Pedestrian %d destroyed" % self.id)

    def update(self, frame):
        print("Updating %d" % self.id)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        back_project = cv2.calcBackProject([hsv], [0], self.roi_hist, [0, 180], 1)

        if args.get("algorithm") == "c":
            ret, self.track_window = cv2.CamShift(back_project, self.track_window, self.term_crit)
            pts = cv2.boxPoints(ret)
            pts = np.int0(pts)
            self.center = center(pts)
            cv2.polylines(frame, [pts], True, 255, 1)

        if not args.get("algorithm") or args.get("algorithm") == "m":  # 默认采用meanShift方法
            ret, self.track_window = cv2.meanShift(back_project, self.track_window, self.term_crit)
            x, y, w, h = self.track_window
            self.center = center([[x, y], [x + w, y], [x, y + h], [x + w, y + h]])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

        self.kalman.correct(self.center)
        prediction = self.kalman.predict()
        cv2.circle(frame, (int(prediction[0]), int(prediction[1])), 4, (0, 255, 0), -1)

        cv2.putText(frame, "ID:%d -> %s" % (self.id, self.center), (11, (self.id + 1) * 25 + 1), font, 0.6, (0, 0, 0),
                    1, cv2.LINE_AA)
        cv2.putText(frame, "ID:%d -> %s" % (self.id, self.center), (10, (self.id + 1) * 25), font, 0.6, (0, 255, 0), 1,
                    cv2.LINE_AA)


def center(points):
    x = (points[0][0] + points[1][0] + points[2][0] + points[3][0]) / 4
    y = (points[0][1] + points[1][1] + points[2][1] + points[3][1]) / 4
    return np.array([np.float32(x), np.float32(y)], np.float32)


def main():
    camera = cv2.VideoCapture('C:\\Users\\yuanpeng\\Desktop\\a.mp4')

    history = 20
    bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)
    bs.setHistory(history)

    cv2.namedWindow("surveillance")
    pedestrians = {}
    firstFrame = True
    frames = 0

    while True:
        print("-------------------- FRAME %d ----------------------" % frames)
        grabbed, frame = camera.read()
        if (grabbed is False):
            print("Failed to grab frame.")
            break
        #		ret, frame = camera.read()

        fgmask = bs.apply(frame)
        if frames < history:
            frames += 1
            continue

        th = cv2.threshold(fgmask.copy(), 127, 255, cv2.THRESH_BINARY)[1]
        th = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
        dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 3)), iterations=2)
        contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        counter = 0
        for c in contours:
            if cv2.contourArea(c) > 300:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                if firstFrame is True:
                    pedestrians[counter] = Pedestrian(counter, frame, (x, y, w, h))  # 这里调用了Pedestrian类，其中counter就是id
                counter += 1

        for i, p in pedestrians.items():
            p.update(frame)

        firstFrame = False
        frames += 1

        cv2.imshow("surveillance", frame)

        if cv2.waitKey(24) & 0xff == 27:
            break
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
