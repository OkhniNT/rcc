#!/usr/bin/env python

# fmt: off
sys.path.insert(0, "../lib_py")
import flexivrdk
import sys
from utility import connect_robot
# fmt: on

robot_ip = "192.168.2.100"
local_ip = "192.168.2.102"

log = flexivrdk.Log()
mode = flexivrdk.Mode

try:
    robot = connect_robot(robot_ip, local_ip, log)

    robot.setMode(mode.NRT_PRIMITIVE_EXECUTION)
    robot.executePrimitive("Home()")


except Exception as e:
    log.error(str(e))
