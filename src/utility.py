#!/usr/bin/env python

"""utility.py

Utility methods.
"""

__copyright__ = "Copyright (C) 2016-2021 Flexiv Ltd. All Rights Reserved."
__author__ = "Flexiv"

import flexivrdk
import time
from scipy.spatial.transform import Rotation as R

def connect_robot(robot_ip, local_ip, log):
    robot = flexivrdk.Robot(robot_ip, local_ip)

    if robot.isFault():
        log.warn("Fault occurred on robot server, trying to clear ...")
        robot.clearFault()
        time.sleep(2)
        if robot.isFault():
            log.error("Fault cannot be cleared, exiting ...")
            exit(1)
        log.info("Fault on robot server is cleared")

    log.info("Enabling robot ...")
    robot.enable()

    seconds_waited = 0
    while not robot.isOperational():
        time.sleep(1)
        seconds_waited += 1
        if seconds_waited == 10:
            log.warn(
                "Still waiting for robot to become operational, please check that the robot 1) "
                "has no fault, 2) is in [Auto (remote)] mode")

    log.info("Robot is now operational")
    return robot

def quat2eulerZYX(quat, degree=False):
    """
    Convert quaternion to Euler angles with ZYX axis rotations.

    Parameters
    ----------
    quat : float list
        Quaternion input in [w,x,y,z] order.
    degree : bool
        Return values in degrees, otherwise in radians.

    Returns
    ----------
    float list
        Euler angles in [x,y,z] order, radian by default unless specified otherwise.
    """

    # Convert target quaternion to Euler ZYX using scipy package's 'xyz' extrinsic rotation
    # NOTE: scipy uses [x,y,z,w] order to represent quaternion
    eulerZYX = R.from_quat([quat[1], quat[2],
                            quat[3], quat[0]]).as_euler('xyz', degrees=degree).tolist()

    return eulerZYX


def list2str(ls):
    """
    Convert a list to a string.

    Parameters
    ----------
    ls : list
        Source list of any size.

    Returns
    ----------
    str
        A string with format "ls[0] ls[1] ... ls[n] ", i.e. each value 
        followed by a space, including the last one.
    """

    ret_str = ""
    for i in ls:
        ret_str += str(i) + " "
    return ret_str


def parse_pt_states(pt_states, parse_target):
    """
    Parse the value of a specified primitive state from the pt_states string list.

    Parameters
    ----------
    pt_states : str list
        Primitive states string list returned from Robot::getPrimitiveStates().
    parse_target : str
        Name of the primitive state to parse for.

    Returns
    ----------
    str
        Value of the specified primitive state in string format. Empty string is 
        returned if parse_target does not exist.
    """
    for state in pt_states:
        # Split the state sentence into words
        words = state.split()

        if words[0] == parse_target:
            return words[-1]

    return ""
