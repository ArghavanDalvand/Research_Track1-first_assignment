from __future__ import print_function

import time
from sr.robot import *



# Lists that store the silver and golden tokens that have already been paired
lst_silver_tokens = []
lst_golden_tokens = []

# Variable for letting the robot know if it has to look for a silver or for a golden token
silver = True
gold_th = 0.8

# Threshold for the control of the linear distance
a_th = 2.0

# Threshold for the control of the orientation
d_th = 0.4

# Instance of the class Robot
R = Robot()

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token   
    Returns:
    dist (float): distance of the closest token (-1 if no token is detected)
    rot_y (float): angle between the robot and the token (-1 if no token is detected)
    code: identifier of the silver token (-1 if no silver token is detected)
     """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and token.info.code not in lst_silver_tokens :
            dist = token.dist
            rot_y = token.rot_y
            code = token.info.code
           
    if dist==100:
        return -1, -1, -1
    else:
        return code, dist, rot_y

def find_gold_token():
    """
    Function to find the closest     
    Returns:
    dist (float): distance of the closest token (-1 if no token is detected)
    rot_y (float): angle between the robot and the token (-1 if no token is detected)
    code: identifier of the gold token (-1 if no gold token is detected)
     """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and token.info.code not in lst_golden_tokens:
            
            dist = token.dist
            rot_y = token.rot_y
            code = token.info.code
    if dist==100:
        return -1, -1, -1
    else:
        return code, dist, rot_y


while 1:
   
    if silver == True: #if silver is true , then we look for a silver token, otherwise for a golden token
        code , dist_silver , rot_y= find_silver_token()
        print("silver.info")
        if dist_silver==-1:
            print("I don't see any token!!")
            turn(+10, 1)
        elif dist_silver < d_th:
            print("Found it!")
            if R.grab():
                lst_silver_tokens.append(code)
                print("Gotcha!")
                # make the robot turn
                turn(20, 2)
                silver = not silver 
            else:
                print("Aww, I'm not close enough!")
        elif -a_th <= rot_y <= a_th:
            # if the robot is well aligned with the token, we go forward
            print("Ah, that'll do.")
            # move the robot forward
            drive(30, 0.5)
        elif rot_y < -a_th:
            print("Left a bit ...")
            # make the robot turn
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit ...")
            # make the robot turn
            turn(+2, 0.5)
    else:
        code , dist_gold , rot_y = find_gold_token()
        print("Gold.info")
        if dist_gold==-1:
            print("I don't see any token!!")
            # make the robot turn
            turn(+10, 1)
        elif dist_gold < d_th:
            print("Found it!")
            if R.grab():
                print("Gotcha!")
                # make the robot turn
                turn(20, 2)
            else:
                print("Aww, I'm not close enough!")
        elif -a_th <= rot_y <= a_th:
            # if the robot is well aligned with the token, we go forward
            print("Ah, that'll do.")
            # move the robot forward
            drive(30, 0.5)
            if dist_gold <= gold_th and dist_gold != -1:
                R.release()
                lst_golden_tokens.append(code)
                # move the robot forward
                drive(-10, 2)
                silver = True
                print("")
        elif rot_y < -a_th:
            print("Left a bit ...")
            # make the robot turn
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit ...")
            # make the robot turn
            turn(+2, 0.5)
    
