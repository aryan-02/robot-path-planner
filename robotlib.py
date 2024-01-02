import math
import time

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile

WHEEL_DIAMETER = 4.32
WHEEL_RADIUS = WHEEL_DIAMETER / 2

ev3 = EV3Brick()
gyroSensor = GyroSensor(Port.S1)

def moveSteering(speed, steering, left_motor, right_motor):
    speed /= 1020
    speed *= 100
    speed1, speed2 = 0, 0
    if steering >= 0:
        speed1 = speed
        speed2 = (-speed * steering + 50*speed)/50
    else:
        speed2 = speed
        speed1 = (speed * steering + 50*speed)/50
    
    speed1 = speed1 / 100 * 1020
    speed2 = speed2 / 100 * 1020
    left_motor.run(speed1)
    right_motor.run(speed2)
    

def moveDistanceGyro(targetDistance, left_motor, right_motor):
    left_motor.brake()
    right_motor.brake()
    wait(1000)
    gyroSensor.reset_angle(0)
    wait(2000)
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)
    print("Called move distance = ", targetDistance)
    distance = 0
    
    error = 0
    lastError = 0
    kP = 3
    kD = 2

    while distance < targetDistance:
        # print(distance, targetDistance)
        angSpeed = 200

        angle = (left_motor.angle() + right_motor.angle()) / 2
        distance = angle * 2 * math.pi * WHEEL_RADIUS / 360
        
        gyroAngle = gyroSensor.angle()
        error = -gyroAngle
        
        derivative = error - lastError

        print("moveSteering", angSpeed, angSpeed, error * kP + derivative * kD)
        moveSteering(angSpeed, error * kP + derivative * kD, left_motor, right_motor)

        lastError = error
    left_motor.brake()
    right_motor.brake()

def moveDistance(targetDistance, left_motor, right_motor):
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)
    print("Called move distance gyro = ", targetDistance)
    distance = 0
    while distance < targetDistance:
        # print(distance, targetDistance)
        angSpeed = 200

        motorAngle = (left_motor.angle() + right_motor.angle()) / 2
        distance = motorAngle * 2 * math.pi * WHEEL_RADIUS / 360
        left_motor.run(angSpeed)
        right_motor.run(angSpeed)
    left_motor.brake()
    right_motor.brake()


def turn(targetAngle, left_motor, right_motor):
    left_motor.brake()
    right_motor.brake()
    wait(1000)
    gyroSensor.reset_angle(0)
    wait(1000)
    
    error = -(targetAngle - gyroSensor.angle())
    integral = 0
    lastError = 0
    start_time = time.time()
    while time.time() - start_time < 5:
        error = -(targetAngle - gyroSensor.angle())
        derivative = lastError - error
        integral += error

        kP = 5.3
        kD = 2
        kI = 0

        rightSpeed = error * kP + integral * kI + derivative * kD + 10
        leftSpeed = -1 * rightSpeed
        lastError = error
        left_motor.run(leftSpeed)
        right_motor.run(rightSpeed)

    left_motor.brake()
    right_motor.brake()

def turnSlow(targetAngle, left_motor, right_motor):
    left_motor.brake()
    right_motor.brake()
    wait(1000)
    gyroSensor.reset_angle(0)
    wait(1000)
    
    while abs(targetAngle - gyroSensor.angle()) > 1:
        print(targetAngle, gyroSensor.angle(), targetAngle - gyroSensor.angle())
        rightSpeed = -30 if targetAngle > gyroSensor.angle() else 30
        leftSpeed = rightSpeed * -1
        left_motor.run(leftSpeed)
        right_motor.run(rightSpeed)

    left_motor.brake()
    right_motor.brake()