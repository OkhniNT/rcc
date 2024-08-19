#!/usr/bin/env python

import time
import threading

# fmt: off
import sys
sys.path.insert(0, "../lib_py")
import flexivrdk
# fmt: on

def loop(robot, log, file):
    # Data struct storing robot states
    robot_states = flexivrdk.RobotStates()

    while True:
        # Get the latest robot states
        robot.getRobotStates(robot_states)
        tcp = robot_states.tcpPose

        # Print all gripper states, round all float values to 2 decimals
        log.info("Current robot states:")
        # fmt: off
        print(['%.2f' % i for i in tcp])
        file.write(repr(tcp))
        # fmt: on
        time.sleep(1)


def main():
    # Program Setup
    # ==============================================================================================

    robot_ip = "192.168.2.100"
    local_ip = "192.168.2.102"

    # Define alias
    log = flexivrdk.Log()
    mode = flexivrdk.Mode

    try:
        # RDK Initialization
        # ==========================================================================================
        # Instantiate robot interface
        robot = flexivrdk.Robot(robot_ip, local_ip)

        # Clear fault on robot server if any
        if robot.isFault():
            log.warn("Fault occurred on robot server, trying to clear ...")
            # Try to clear the fault
            robot.clearFault()
            time.sleep(2)
            # Check again
            if robot.isFault():
                log.error("Fault cannot be cleared, exiting ...")
                return
            log.info("Fault on robot server is cleared")

        # Enable the robot, make sure the E-stop is released before enabling
        log.info("Enabling robot ...")
        robot.enable()

        # Wait for the robot to become operational
        seconds_waited = 0
        while not robot.isOperational():
            time.sleep(1)
            seconds_waited += 1
            if seconds_waited == 10:
                log.warn(
                    "Still waiting for robot to become operational, please check that the robot 1) "
                    "has no fault, 2) is in [Auto (remote)] mode")

        log.info("Robot is now operational")

        file = open("tcp_poses.txt", "w")

        # Print States
        # =============================================================================
        # Thread for printing robot states
        print_thread = threading.Thread(
            target=loop, args=[robot, log, file])
        print_thread.start()
        print_thread.join()

    except Exception as e:
        # Print exception error message
        log.error(str(e))


if __name__ == "__main__":
    main()
