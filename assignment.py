from __future__ import print_function

import time
from sr.robot import *

""" Inizialization global variable"""

""" Initializing list which contain codes find and grabbed"""
list_code = []


""" float: Threshold for the control of the linear distance"""
a_th = 2.0

""" float: Threshold for the control of the orientation"""
d_th = 0.4

""" instance of the class Robot"""
R = Robot()

def drive(speed, seconds):
        """
    	Function for setting a linear velocity
    
    	Args: speed (float): the speed of the wheels
	      seconds (float): the time interval
        """
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

def turn(speed, seconds):
	"""
    	Function for setting an angular velocity
    
    	Args: speed (float): the speed of the wheels
	      seconds (float): the time interval
    	"""
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = -speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

def find_golden_token():
	"""
        Function to find the closest golden token

        Returns:
	       dist (float): distance of the closest golden token (-1 if no token is detected)
	       rot_y (float): angle between the robot and the golden token (-1 if no token is detected)
	       code (int): token's identification code (-1 if no token is detected)
	"""
	dist=100
	for token in R.see():
        	if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
	    		print("Golden token found: ", token.info.code)
	    		if token.info.code in list_code: #if the token seen is the list, it searches another token
	    			# dist = 100
	    			print("Seen token") 
	    			continue
	    		dist=token.dist
	    		rot_y=token.rot_y
	    		code = token.info.code
	if dist==100:
		return -1, -1, -1
    	else:
   		return dist, rot_y, code

def find_centre_token():

	"""Function to find the token which is used as the reference one where the robot bring all other tokens. 
	In this case the reference frame is the first token which is seen by the robot
	
	Returns:
		dist (float): the distance from robot to the reference token (-1 if no token is detected)
		rot_y (float): the angle betwwe the robot and the reference token (-1 if no token is detected)
		code (int): token's identification code (-1 if no token is detected)
	"""
	
	dist=100
	for token in R.see():
        	if token.info.code == list_code[0]:

	    		print("token centred found")

	    		dist=token.dist
	    		rot_y=token.rot_y
	    		code = token.info.code

	if dist==100:
		return -1, -1, -1
    	else:
   		return dist, rot_y, code

def bring_to_golden(n):
	"""
	Function to find the reference token where to bring other tokens and it release the token in the correct position near to the reference token
	
	Args: n (int): number of token in the arena
	
	"""
	while 1:
		dist, rot_y, code = find_centre_token()

		if dist==-1: # if no token is detected (because dist = -1),the robot turn 
			print("I don't see token 1!")
			turn(10, 0.5)
			
		elif dist <1.5*d_th: # if we are close to the golden token, we try release it.
		
			if R.release(): # if we release the token
				print("I released the token to the reached position")
				n-=1 #we decrease the value of tokens remainig each time a token is released in the centred position
				
				if n==0: # when n=0 we understand that the robot has done its job, so we've finished all its tasks
					print('Good job! :)')
					exit() #When n=0 the program will finish through exit() function
					
				drive(-30.0, 1) #the robot need to drive back to not collide with the token released
				turn(2,0.5)
				break
		else:
				
			if -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
				drive(30, 0.1)
				print("I'm correcting the position to 1")
			
	    		elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left
				turn(-2, 0.5)
				print("I'm correcting the position to 1")
			
	    		elif rot_y > a_th:
				turn(+2, 0.5) # if the robot is not well aligned with the token, we move it on the right
				print("I'm correcting the position to 1")

def grab_golden(n):
	"""
	Function to grab tokens to the reference token
	
	Args: n (int): number of token in the arena
	
	"""
	while 1:
		dist, rot_y, code = find_golden_token()
		
		if code in list_code: # If code is in golden_code list, we assign dist = -1
			dist = -1
		
		if dist==-1: # if no token is detected (because dist = -1), we make the robot turn 
			print("I don't see any golden token!!")
			turn(+10, 0.5)
			
		elif dist <d_th: # if we are close to the token, we can try grab it.
			print("Found it!")
			if R.grab(): # if we grab the token
				print("Gotcha!")
				list_code.append(code) # we append the token's code inside golden_code list when it is grabbed
				n-=1 # we decrease n value each time we grab a golden token
				bring_to_golden(n)
			else: # this else needs to move forward the robot in order to grab the token at the right distance
				drive(10, 0.5)
				    	
		elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
			drive(30.0, 0.1)
			print("I'm correcting the position search")
		
	    	elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left
			turn(-2.0, 0.5)
			print("I'm correcting the position to search")
			
	    	elif rot_y > a_th:
			turn(+2.0, 0.5) # if the robot is not well aligned with the token, we move it on the right
			print("I'm correcting the position to search")
			
			
def main():
	
	dist, rot_y, code = find_golden_token() #The roboto search the first token that it sees
	list_code.append(code) #the first token seen is fixed on the top of the list (index vector = 0)
	n=6 #number of token in the arena
	grab_golden(n)

main()
