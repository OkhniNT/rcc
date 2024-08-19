#!/usr/bin/env python

import time
import threading
from os import system
import numpy as np

# fmt: off
import sys
sys.path.insert(0, "../lib_py")
import flexivrdk
# fmt: on

from utility import quat2eulerZYX

def loop(robot, log):
    robot_states = flexivrdk.RobotStates()

    poses = np.empty([6, 1])

    for i in range(0, 19):
        robot.getRobotStates(robot_states)
        pose_tcp = robot_states.tcpPose
        pose_pos = [pose_tcp[0], pose_tcp[1], pose_tcp[2]]
        pose_quat = [pose_tcp[3], pose_tcp[4], pose_tcp[5], pose_tcp[6]]
        pose_euler = quat2eulerZYX(pose_quat, degree=True)

        system("clear")
        log.info("TCP Pose:")
        # fmt: off
        pose_full = pose_pos + pose_euler
        print(pose_full)
        # fmt: on
        np.append(poses, pose_full)
        time.sleep(0.5)

    with open("poses.npy", "wb") as f:
        np.save(f, poses)

def main():
    robot_ip = "192.168.2.100"
    local_ip = "192.168.2.102"

    log = flexivrdk.Log()

    try:
        robot = flexivrdk.Robot(robot_ip, local_ip)

        if robot.isFault():
            log.warn("Fault occurred on robot server, trying to clear ...")
            robot.clearFault()
            time.sleep(2)
            if robot.isFault():
                log.error("Fault cannot be cleared, exiting ...")
                return
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

        print_thread = threading.Thread(
            target=loop, args=[robot, log])
        print_thread.start()
        print_thread.join()

    except Exception as e:
        log.error(str(e))


if __name__ == "__main__":
    main()
