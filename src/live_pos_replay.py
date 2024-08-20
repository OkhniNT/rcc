#!/usr/bin/env python

import time
import threading
import numpy as np

# fmt: off
import sys
sys.path.insert(0, "../lib_py")
import flexivrdk
# fmt: on

from utility import list2str
from utility import parse_pt_states

# Maximum contact wrench [fx, fy, fz, mx, my, mz] [N][Nm]
MAX_CONTACT_WRENCH = [50.0, 50.0, 50.0, 15.0, 15.0, 15.0]

def loop(robot, log, mode):
    poses = np.load("poses.npy")

    robot.setMode(mode.NRT_PRIMITIVE_EXECUTION)
    robot.executePrimitive("Home()")

    for i in range(0, len(poses) - 1):
        target_pos = [poses[i][0], poses[i][1], poses[i][2]]
        target_euler = [poses[i][3], poses[i][4], poses[i][5]]
        
        robot.executePrimitive(
            "MoveCompliance(target="
            + list2str(target_pos)
            + list2str(target_euler)
            + "WORLD WORLD_ORIGIN, maxVel=0.1, enableMaxContactWrench=1, maxContactWrench="
            + list2str(MAX_CONTACT_WRENCH) + ")")

        # Wait for robot to reach target location by checking for "reachedTarget = 1"
        # in the list of current primitive states
        while (parse_pt_states(robot.getPrimitiveStates(), "reachedTarget") != "1"):
            time.sleep(0.05)

def main():
    robot_ip = "192.168.2.100"
    local_ip = "192.168.2.102"

    log = flexivrdk.Log()
    mode = flexivrdk.Mode

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
            target=loop, args=[robot, log, mode])
        print_thread.start()
        print_thread.join()

    except Exception as e:
        log.error(str(e))


if __name__ == "__main__":
    main()
