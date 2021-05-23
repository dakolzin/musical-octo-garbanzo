#!/usr/bin/env python

import rospy
import sys
import copy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
robot = moveit_commander.RobotCommander()

scene = moveit_commander.PlanningSceneInterface()

display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory)

arm_group = moveit_commander.MoveGroupCommander("arm_1")
arm_group.set_goal_tolerance(0.1)
arm_group.set_pose_target([-0.083, -0.039, 0.158, -1.772, 1.348, 1.527])
plan1 = arm_group.go()
print "============ Waiting while RVIZ displays ..."
rospy.sleep(5)

arm_group = moveit_commander.MoveGroupCommander("arm_1")
arm_group.set_goal_tolerance(0.1)
arm_group.set_named_target("candle")
plan1 = arm_group.go()

print "============ Waiting while RVIZ displays pose arm 'candle'..."
rospy.sleep(5)

hand_group = moveit_commander.MoveGroupCommander("arm_1_gripper")
arm_group.set_goal_tolerance(0.1)
hand_group.set_named_target("open")
plan2 = hand_group.go()

print "============ Waiting while RVIZ displays pose gripper 'open'..."
rospy.sleep(5)

arm_group = moveit_commander.MoveGroupCommander("arm_1")
arm_group.set_goal_tolerance(0.1)
arm_group.set_named_target("pick")
plan1 = arm_group.go()

print "============ Waiting while RVIZ displays pose gripper 'pick'..."
rospy.sleep(5)

hand_group = moveit_commander.MoveGroupCommander("arm_1_gripper")
hand_group.set_named_target("close")
plan2 = hand_group.go()

print "============ Waiting while RVIZ displays pose gripper 'close'..."
rospy.sleep(15)

arm_group = moveit_commander.MoveGroupCommander("arm_1")
arm_group.set_named_target("praise")
plan1 = arm_group.go()

print "============ Waiting while RVIZ displays pose arm 'zero'..."
rospy.sleep(15)

arm_group = moveit_commander.MoveGroupCommander("arm_1")
arm_group.set_named_target("pick")
plan1 = arm_group.go()

print "============ Waiting while RVIZ displays pose gripper 'go to pick'..."
rospy.sleep(15)

hand_group = moveit_commander.MoveGroupCommander("arm_1_gripper")
hand_group.set_named_target("close")
plan2 = hand_group.go()

print "============ Waiting while RVIZ displays pose gripper 'close'..."
rospy.sleep(15)

arm_group = moveit_commander.MoveGroupCommander("arm_1")
arm_group.set_named_target("praise")
plan1 = arm_group.go()

print "============ Waiting while RVIZ displays pose arm 'zero'..."
rospy.sleep(15)

arm_group = moveit_commander.MoveGroupCommander("arm_1")
arm_group.set_named_target("place")
plan1 = arm_group.go()

print "============ Waiting while RVIZ displays pose gripper 'go to place'..."
rospy.sleep(15)

hand_group = moveit_commander.MoveGroupCommander("arm_1_gripper")
hand_group.set_named_target("open")
plan2 = hand_group.go()

print "============ Waiting while RVIZ displays pose gripper 'open'..."
rospy.sleep(15)


print "============ grasp_demo2 is done..."
rospy.sleep(5)
moveit_commander.roscpp_shutdown()
