Python Robotics Simulator
================================
Tasks of the simulator
----------------------
The aim of this first assignment is to make a simulator for the robotics. The simulator is able to simulate a robot in a bidimensional environment, to make it move around the arena and interact with golden token which are the objects collocated around the arena. The robot is able to look around the space where it is moving and to make decisions in order to grab any token initially collocated around the environment and to make any token grabbed amd released in a specific part of the arena.

Installing and running
----------------------
The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or
`easy_install`.

---
How to run the code
-------------------
In order to copy this reposotiry, it is needed to clone the assignment folder:

    git clone https://github.com/ilacolo/Assignment1_Research_Track1/tree/main

To run the program, use `run.py`, passing it the file names.

```bash
$ python2 run.py assignment.py
```

It is neccesay to be in the folder that contain the program.

---

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

## Main of the code and Functions
In order to make the robot able to complete the tasks, six functions are implemented and they work together in the main() function which is recalled at the end.

Function used to implement the program
--------------------------------------
The code contains some functions which allows the robot to complete all of its tasks. The functions used are the following:
* `drive(speed, seconds)`: it sets the linear velocity
* `turn(speed, seconds)`: it sets the angular velocity
* `find_golden_token()` : it finds the closest golden token
* `fine_centre_token()` : it finds the token which is used as the reference one where the robot bring all other tokens. (In this case the reference frame is the first token detected by the robot)
* `bring_to_golden(n)` : it finds the reference token where to bring other tokens and it releases the token in the correct position near to the reference token
* `grab_golden(n)` : it grabs tokens to the reference token
* `main()` : In this fuction two values are set: the number of tokens in the arena and the reference token, which is the first one seen by the robot when it starts to turn.

Initialization of Global variables 
----------------------------------
Global variables set at the beginning are:
`list_code` = [] which is the list that contains the identification codes of grabbed tokens. It contians in the first position (index = 0) the first token seen by the robot in order to fix it at the begging and use it as the reference token where to bring the others.
`a_th` = 2.0 which is a float value. It is the threshold for the control of the linear distance.
`d_th` = 0.4 which is a float value. It is the threshold for the control of the orientation.

Main function
-------------
The main function `main()` is simple. In this part of the code it is possible to obtain the distance, the rotation angle and the code, which is the identification number of the token of the first detected token. Then it is need to fix the code of this first token in the list of codes `liste_code` initialized as global variable. In the end the number of token that it is possible to find in the arena is set to 6, and with this initialization the function grab_golden() is called. 

`grab_golden(n)` function
--------------------------
This is the only function called in the main function of the program. Through an infinite loop while, this function calls the function `find_golden_token()` in order to find golden token which is nearest the robot. Then this part of the code checks that the code of the detected token has not already grabbed and brought it to the reference token. If the nearest token has already grabbed, so its code is in `liste_code` list, the function assign -1 to the distance so that the robot turns around itself to find the other nearest golden token. Infact, if the distant is equal to -1, the robot does not detect any token, so it turns to find another one object and then it drives to it. There is also a control which helps the robot to correct the position to aligns its to the golden token to grab. If the robot arrives near to the token, the function allows the robot to grab the token, and the identification code of the token grabbed is fixed in list. There is also a counter which decreases when a token is grabbed, to help undestanding how many object the robot has to grab to complete its tasks. At the end, this function calls the function `bring_to_golden(n)` in order to bring the grabbed token to the reference token. 

`bring_to_golden(n)` function
-----------------------------
This function is called inside `grab_golden(n)` function once that robot has grabbed its nearest token. It is similar to the previus one, infact throught an infinite loop while, the function get the distance, the rotation angle and the code of the reference token which is the first one the robot has detected. If no reference token is detected, this function make the robot turn so that he can find it. When the robot finds the reference token where to release the grabbed token, it drive and turn to it. There is a control which helps the robot to be aligned with the reference token. When it is arrived near to the reference token with a spacific threshold, the grabbed token is released in front of the reference one. The function adds a counter which helps to count how many tokens have been released in the correct position. When the robot releases a new object, the number decreases and when it is equal to 0, it means that the robot has completed its tasks and it exits the program. The fucntion helps also the robot to drive back when it has released the token, to not collide with the released object.

`find_centre_token()` function
------------------------------
This function allows the tobot to find the reference token where to bring the others. When the robot sees a token it controls that this one is the first token in `list_code` list. If it is, he gets the distance, the rotation angle and the code variable and it updates them. If the reference token is found, this function updates the values of distance, rotation angle and code of the reference object found, otherwise, it return three values equal to -1. 

`find_golden_token()` function
------------------------------
This function is similar to the previous one, because its task is to find the token nearest to the robot. First of all, it finds from the tokens which are visible, the one that is golden and closer.If it finds the closest object it updates the distance, rotation angle anche code variables of the new found token. If the token seen is the list, it searches another token and if the distance from any token is equale to 100, it understand that there are no objects near to the robot, so the function return three values equal to -1. 

`drive(speed, seconds)` and `turn(speed, seconds)` functions
----------------------------------------------
These two functions set the linear and the angular velocity and they control the motor which moves the robot.

# Pseudocode of the Program
- Import necessary libraries and modules

- Initialize global variables and constants
    - an empyt list which will contain the codes of tokens grabbed
    - the threshold for the cotnrol of linear distance
    - the threshold for the control of orientation
- Define functions the Robot class

- Function `drive(speed, seconds)`:
    - Set linear velocity of robot wheels
    - Wait for specified time interval
    - Stop robot motors

- Function `turn(speed, seconds)`:
    - Set angular velocity of robot wheels for turning
    - Wait for specified time interval
    - Stop robot motors

- Function `find_golden_token()`:
    - Initialize distance
    - Iterate over visible tokens are seen by the robot:
        - If the token is closer than the initialize distance and it is a golden token:
            - Print the code of the detected token 
            - Update distance, rotation angle, and code variables
    - If the detected golden token is in list_code:
        -   Print that this token has been already bring to the reference one
        -   Continue to find another token
        - If token code is not in list_code:
        - Return distance, rotation angle, and code updated before
    - Else:
        - Return -1, -1, -1 indicating no golden token found

- Function `find_centre_token()`:
    - Initialize distance
    - Iterate over visible tokens are seen by the robot:
        - If the token is the reference token (first token in list_code):
            - Update distance, rotation angle, and code variables
    - If the reference token is found:
        - Print that the reference token is found
        - Return distance, rotation angle, and code
    - Else:
        - Return -1, -1, -1 indicating no reference token found

- Function `bring_to_golden(n)`:
    - Loop indefinitely:
        - Get distance, rotation angle, and code of the reference token
        - If no reference token is detected:
            - Turn the robot to search for the reference token
        - Else if robot is close to the golden token:
            - Release the token near the reference token
            - Decrement the number of token released near to the reference token (n)
            - If n becomes 0:
                - Print success message and exit the program
            - Move robot backward and turn slightly
            - Break the loop
        - Else:
            - Correct robot's position to align with the reference token driving, turning right and turning left the robot

- Function `grab_golden(n)`:
    - Loop indefinitely:
        - Get distance, rotation angle, and code of the golden token
        - If token code is in list_code:
            - Set distance to -1 to skip this token
        - If no golden token is detected:
            - Turn the robot to search for the token
        - Else if robot is close to the golden token:
           - Grab the token
            - Append token code to list_code
            - Decrement count of token grabbed (n)
            - Call bring_to_golden function to bring the grabbed token to the reference token
            - If token is not grabbed successfully:
                - Move robot forward to adjust distance for grabbing
        - Else:
            - Correct robot's position to align with the golden token driving, turning right and turning left the robot

- Function `main()`:
    - Get distance, rotation angle, and code of the first detected golden token
    - Append the token code to list_code
    - Set token count (n) to the total number of tokens in the arena
    - Call grab_golden function

- Call `main()` function to start the program

Possible improvements of the code
--------------------------------
The program could be improved in these ways:
 * It is possible to add another list where to fix the codes of token released. This list could be used in order to make the last token relased the reference one. In this way, it is possible to bring the grabbed golden token to the one which has been just released and not to the first one detected when the robot starts to turn. This improvement could decrease the collisions beteen the robot and tokens and also between the tokens released.
 * It is possible to create another function which makes the robot turn around itself of 360 degrees, in order to append all the codes of the tokens in a list and then to obtain variables of the token with the shortest distance from the robot. In this way the robot checks the distances from all the tokens and not only of the token that is in its line of sight. This improvement coud increase the time efficency.
 * It is also possible to work with Cartesian coordinates in order to fix the point where the robot could bring all the a tokens. This implementation is the most complicated because it is needed to fix a reference frame in the arena, then to calculate all the coordinates using the distances between the objects. This improveement needs more functions, but it could improve the control of robot's moviments and the control of the tokens' positions.

[sr-api]: https://studentrobotics.org/docs/programming/sr/
