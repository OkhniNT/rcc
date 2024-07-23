#!/usr/bin/env python

import time
import argparse
import threading

# fmt: off
import sys
sys.path.insert(0, "../lib_py")
import flexivrdk
# fmt: on

def loop(robot, log):
    # Data struct storing robot states
    robot_states = flexivrdk.RobotStates()

    while True:
        # Get the latest robot states
        robot.getRobotStates(robot_states)

        # Print all gripper states, round all float values to 2 decimals
        log.info("Current robot states:")
        # fmt: off
        print("q: ",  ['%.2f' % i for i in robot_states.q])
        print("theta: ", ['%.2f' % i for i in robot_states.theta])
        print("dq: ", ['%.2f' % i for i in robot_states.dq])
        print("dtheta: ", ['%.2f' % i for i in robot_states.dtheta])
        print("tau: ", ['%.2f' % i for i in robot_states.tau])
        print("tau_des: ", ['%.2f' % i for i in robot_states.tauDes])
        print("tau_dot: ", ['%.2f' % i for i in robot_states.tauDot])
        print("tau_ext: ", ['%.2f' % i for i in robot_states.tauExt])
        print("tcp_pose: ", ['%.2f' % i for i in robot_states.tcpPose])
        print("tcp_pose_d: ", ['%.2f' % i for i in robot_states.tcpPoseDes])
        print("tcp_velocity: ", ['%.2f' % i for i in robot_states.tcpVel])
        print("camera_pose: ", ['%.2f' % i for i in robot_states.camPose])
        print("flange_pose: ", ['%.2f' % i for i in robot_states.flangePose])
        print("FT_sensor_raw_reading: ", ['%.2f' % i for i in robot_states.ftSensorRaw])
        print("F_ext_tcp_frame: ", ['%.2f' % i for i in robot_states.extWrenchInTcp])
        print("F_ext_base_frame: ", ['%.2f' % i for i in robot_states.extWrenchInBase])
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

        # Print States
        # =============================================================================
        # Thread for printing robot states
        print_thread = threading.Thread(
            target=loop, args=[robot, log])
        print_thread.start()
        print_thread.join()

    except Exception as e:
        # Print exception error message
        log.error(str(e))


if __name__ == "__main__":
    main()
