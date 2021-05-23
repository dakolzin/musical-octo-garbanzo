#!/usr/bin/env python
 
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi 
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from math import radians
 
def all_close(goal, actual, tolerance):
  """
  Convenience method for testing if a list of values are within a tolerance of their counterparts in another list
  @param: goal       A list of floats, a Pose or a PoseStamped
  @param: actual     A list of floats, a Pose or a PoseStamped
  @param: tolerance  A float
  @returns: bool
  """
  all_equal = True
  if type(goal) is list:
    for index in range(len(goal)):
      if abs(actual[index] - goal[index]) > tolerance:
        return False
 
  elif type(goal) is geometry_msgs.msg.PoseStamped:
    return all_close(goal.pose, actual.pose, tolerance)
 
  elif type(goal) is geometry_msgs.msg.Pose:
    return all_close(pose_to_list(goal), pose_to_list(actual), tolerance)
 
  return True
 
class MoveGroupPythonInterfaceTutorial(object):
  """MoveGroupPythonInterfaceTutorial"""
  def __init__(self):
    super(MoveGroupPythonInterfaceTutorial, self).__init__()
 
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface_tutorial',
                    anonymous=True)
 
    robot = moveit_commander.RobotCommander()
 
    scene = moveit_commander.PlanningSceneInterface()
 
    group_name = "arm_1"
    group = moveit_commander.MoveGroupCommander(group_name)
 
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                   moveit_msgs.msg.DisplayTrajectory,
                                                   queue_size=20)
 
    planning_frame = group.get_planning_frame()
    print "============ Reference frame: %s" % planning_frame
 
    # We can also print the name of the end-effector link for this group:
    eef_link = group.get_end_effector_link()
    print "============ End effector: %s" % eef_link
 
    # We can get a list of all the groups in the robot:
    group_names = robot.get_group_names()
    print "============ Robot Groups:", robot.get_group_names()
 
    # Sometimes for debugging it is useful to print the entire state of the
    # robot:
    print "============ Printing robot state"
    print robot.get_current_state()
    print ""
 
    self.box_name = ''
    self.robot = robot
    self.scene = scene
    self.group = group
    self.display_trajectory_publisher = display_trajectory_publisher
    self.planning_frame = planning_frame
    self.eef_link = "arm_link_5"
    self.group_names = group_names
 
 
  def go_to_joint_state(self):
   
    group = self.group
 
    joint_goal = group.get_current_joint_values()
    joint_goal[0] = pi/4
    joint_goal[1] = 0.8799
    joint_goal[2] = 0
    joint_goal[3] = 0
    joint_goal[4] = 0
    joint_goal[5] = 0
 
    group.go(joint_goal, wait=True)
    group.stop()
    current_joints = self.group.get_current_joint_values()
    return all_close(joint_goal, current_joints, 0.1)
 
 
  def go_to_pose_goal(self):
 
    group = self.group
 
    pose_goal = geometry_msgs.msg.Pose()
    pose_goal.orientation.x = 0.000
    pose_goal.orientation.y = 0.000
    pose_goal.orientation.z = 0.707
    pose_goal.orientation.w = 0.707
    
    pose_goal.position.x = 0.000
    pose_goal.position.y = 0.191
    pose_goal.position.z = 1.001
    group.set_joint_value_target(pose_goal,True)
 
    plan = group.go(wait=True)
    group.stop()
    group.clear_pose_targets()
 
    current_pose = self.group.get_current_pose().pose
    return all_close(pose_goal, current_pose, 0.1)
 
  def plan_cartesian_path(self, scale=1):
    group = self.group
    waypoints = []
    wpose = group.get_current_pose().pose
    wpose.position.x = 0.549
    wpose.position.y = -0.171
    wpose.position.z = 0.628
    waypoints.append(copy.deepcopy(wpose))
    (plan, fraction) = group.compute_cartesian_path(
                                       waypoints,   # waypoints to follow
                                       0.01,        # eef_step
                                       0.0)         # jump_threshold
 
    return plan, fraction
#Nazar's Code
  def rad(self,rpy):
    rpyrad = [radians(rpy[0]),radians(rpy[1]),radians(rpy[2])]
    return rpyrad
  def moveto_xyzrpy(self,xyzrpy):
    self.group.set_pose_target(xyzrpy,end_effector_link = self.eef_link)
    plan = self.group.go(wait=True)
    self.group.stop()
    self.group.clear_pose_targets()
    current_pose = self.group.get_current_pose().pose
 
def main():
  try:
 
    armDriver = MoveGroupPythonInterfaceTutorial()
 
    #before pick pose
    xyz = [0.385, -0.000, 0.551]
    rpy = armDriver.rad([179.274, 39.769, 179.992])
    xyzrpy = xyz+rpy
    armDriver.moveto_xyzrpy(xyzrpy) 
    #pick pose
    xyz = [0.593, -0.000, 0.189]
    rpy = armDriver.rad([179.283, -0.801, 179.996])
    xyzrpy = xyz+rpy
    armDriver.moveto_xyzrpy(xyzrpy) 
    #after pick pose
    xyz = [0.385, -0.000, 0.551]
    rpy = armDriver.rad([179.274, 39.769, 179.992])
    xyzrpy = xyz+rpy
    armDriver.moveto_xyzrpy(xyzrpy) 
    #before place pose
    xyz = [-0.222, 0.314, 0.552]
    rpy = armDriver.rad([179.267, 39.769, -54.704])
    xyzrpy = xyz+rpy
    armDriver.moveto_xyzrpy(xyzrpy) 
    #place pose
    xyz = [-0.343, 0.485, 0.178]
    rpy = armDriver.rad([179.786, -2.323, -54.750])
    xyzrpy = xyz+rpy
    armDriver.moveto_xyzrpy(xyzrpy) 
    #after place pose
    xyz = [-0.222, 0.314, 0.552]
    rpy = armDriver.rad([179.267, 39.769, -54.704])
    xyzrpy = xyz+rpy
    armDriver.moveto_xyzrpy(xyzrpy) 
    #home pose
    xyz = [0.000, -0.000, 0.810]
    rpy = armDriver.rad([-0.000, -0.000, -0.000])
    xyzrpy = xyz+rpy
    armDriver.moveto_xyzrpy(xyzrpy) 
 
 
    print "============ demo complete=================="
  except rospy.ROSInterruptException:
    return
  except KeyboardInterrupt:
    return
 
if __name__ == '__main__':
  main()

