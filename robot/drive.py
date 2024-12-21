import time

def set_left(robot, speed):
    robot.left_motor.value = speed
    return

def set_right(robot, speed):
    robot.right_motor.value = speed
    return

def look_right(robot):
    robot.left_motor.value = 0.5
    robot.right_motor.value = -0.1
    return

def look_left(robot):
    robot.left_motor.value = -0.1
    robot.right_motor.value = 0.5
    return

def stop(robot):
    robot.left_motor.value = 0
    robot.right_motor.value = 0
    return

def uturn(robot):
    set_left(robot, 0.75)
    set_right(robot, -0.75)
    time.sleep(0.7)
    return

def _set_speed(robot, center_x, scenter_x, Kp, base_speed):
    # 오차 계산 (차선 중심과 화면 중앙의 차이)
    error = center_x - scenter_x
            
    # P제어를 적용해 보정값 계산
    control_output = Kp * error / 100
            
    # 모터 속도 계산
    left_val = base_speed - control_output
    right_val = base_speed + control_output

    # 모터 속도 제한 (0 ~ 1.0 범위 내)
    left_motor_speed = max(min(left_val, 1.0), 0)
    right_motor_speed = max(min(right_val, 1.0), 0)

    # 모터에 속도 적용
    robot.left_motor.value = left_motor_speed
    robot.right_motor.value = right_motor_speed
    
    return

def drive(robot, cx, Kp, base_speed):
    if cx is not False:
        _set_speed(robot, cx, 195, Kp, base_speed)
    else:
        if cx > 195:
            look_right(robot)
        else:
            look_left(robot)
    return


