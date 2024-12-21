import cv2
import time
from ultralytics import YOLO

import robot.drive as drive
import robot.buzzer as buzzer
import utils.cameral as cameral
from lib.robot import Robot

# 0:'green', 1:'left', 2:'red', 3:'right', 4:'slow', 5:'stop', 6:'uturn'

def main():
    Kp = 0.02
    base_speed = 0.7
    
    sign_flag = [True, True, True, True, True, True, True]
    start_time = None
    
    model = YOLO("best.onnx")
    camera = cv2.VideoCapture("nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),format=NV12,width=1280,height=720,framerate=30/1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1",cv2.CAP_GSTREAMER)
    
    robot = Robot()
    
    while (camera.isOpened()):
        ret, frame = camera.read()
        if not ret:
            print("failed")
            break
        
        # box_size = results[0].boxes.xywhn.to('cpu').tolist()
        
        # if len(box_size) != 0:
        #     box_size = [box_size[0][2], box_size[0][3]] # normalized width, height
        # else:
        #     box_size = [0, 0]
        
        # if box_size[0] < 0.3 and box_size[1] < 0.3: # 박스가 가로 세로 0.3 이하일때 무시
        #     #todo 값 조정
        #     sign = []
        
        # results = model.predict(source=frame, save=True, save_txt=True, imgsz=640, verbose=False)
        
        
        results = model.predict(source=frame, imgsz=640)
        
        sign = results[0].boxes.cls.to('cpu').tolist()
        
        if len(sign) != 0:
            
            if sign_flag[0] is True and sign[0] == 0.0: # green light
                buzzer.buzzer_on(1)

                sign_flag[0] = False
                sign_flag[2] = False
                continue
                
            if sign_flag[2] is True and sign[0] == 2.0: # red light
                drive.set_left(robot, 0)
                drive.set_right(robot, 0)
                
                continue
            
            if sign_flag[4] is True and sign[0] == 4.0: # slow
                if start_time is None:
                    start_time = time.time()
                
                cx = cameral.getCenterX(frame)
                drive.drive(robot, cx, Kp, base_speed / 2)
            
                if time.time() - start_time >= 5:
                    sign_flag[4] = False
                    start_time = None
                continue
            
            if sign_flag[5] is True and sign[0] == 5.0: # stop
                drive.stop(robot) # 2초간 정지
                time.sleep(2)
                
                sign_flag[5] = False
                continue
                        
            if sign_flag[1] is True and sign[0] == 1.0: # left
                if start_time is None:
                    start_time = time.time()
                
                cx = cameral.getCenterX(frame, left=True)
                drive.drive(robot, cx, Kp, base_speed)
                
                if time.time() - start_time >= 2:
                    sign_flag[1] = False
                    start_time = None
                continue
            
            if sign_flag[3] is True and sign[0] == 3.0: # right
                if start_time is None:
                    start_time = time.time()
                
                cx = cameral.getCenterX(frame, right=True)
                drive.drive(robot, cx, Kp, base_speed)
                
                if time.time() - start_time >= 2:
                    sign_flag[3] = False
                    start_time = None
                continue
            
            if sign_flag[6] is True and sign[0] == 6.0: # uturn
                drive.stop(robot) # 2초
                drive.uturn(robot)
                buzzer.buzzer_on(2)
                robot.stop()
                
                sign_flag[6] = False
                break

        cx = cameral.getCenterX(frame)
        drive.drive(robot, cx, Kp, base_speed)
        
        #todo 인식한 신호 confidence가 일정 이상일때 조건
        
    
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()