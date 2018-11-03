#!/usr/bin/env python
import rospy
import math
import time
import random
from geometry_msgs.msg import * # message type
from turtlesim.srv import *
from turtlesim.msg import Pose

x_first=0;y_first=0;theta_fisrt=0;
x=0;y=0;theta=0;
start_x=0.2;start_y=1.5;length=10.6;width=8
safe_distance=1
def pose_callback_first(data):
    global x_first,y_first,theta_fisrt
    x_first=data.x
    y_first=data.y
    theta_fisrt=data.theta

def pose_callback(data):
    #rospy.loginfo("%f %f %f"%(data.x,data.y,data.theta))
    global x,y,theta
    x=data.x
    y=data.y
    theta=data.theta

def move(distance,vel=0.5,is_forward=1):
    global x,y,theta
    x0=x
    y0=y
    rate = rospy.Rate(10) # 10hz
    vel_talker=rospy.Publisher("turtle2/cmd_vel",Twist,queue_size=10)#set vertical
    vel_msg=Twist()
    vel_msg.linear.x=vel
    if is_forward==0:
        vel_msg.linear.x *=-1

    distance_moved=0
    while(1):
        vel_talker.publish(vel_msg)
        distance_moved = math.sqrt((x-x0)*(x-x0)+(y-y0)*(y-y0))
        rospy.loginfo("distance_moved is %f  current:%f %f  x0=%f y0=%f"%(distance_moved,x,y,x0,y0))
        if distance_moved>=distance:
            rospy.loginfo("reached")
            break
        rate.sleep()
    vel_msg.linear.x=0
    vel_talker.publish(vel_msg)

def rotate(vel=0.5,angular=math.pi/2,is_forward=1):
    global x,y,theta
    theta0=theta
    rate = rospy.Rate(10) # 10hz

    vel_talker=rospy.Publisher("turtle2/cmd_vel",Twist,queue_size=10)#set vertical
    vel_msg=Twist()
    vel_msg.linear.x=0
    vel_msg.angular.z=vel
    if is_forward==0:
        vel_msg.linear.x *=-1

    angular_moved=0
    while(1):
        vel_talker.publish(vel_msg)
        angular_moved=theta-theta0
        rospy.loginfo("angular_moved is %f"%(angular_moved))
        if angular_moved>=angular:
            rospy.loginfo("reached")
            break
        rate.sleep()
    vel_msg.angular.z=0
    vel_talker.publish(vel_msg)

def set_absolute_pose(des_x,des_y,des_theta):
    try:
        set_absolute_pose_client=rospy.ServiceProxy("turtle2/teleport_absolute",TeleportAbsolute)
        resp=set_absolute_pose_client.call(des_x,des_y,des_theta)
        rospy.loginfo("set the turtle2 to position:%f %f"%(des_x,des_y))
    except rospy.ServiceException, e:
        rospy.logwarn("Service call failed: %s"%e)

def setPen(r,g,b,w,off):
    try:
        setPen_client=rospy.ServiceProxy("turtle2/set_pen",SetPen)
        resp=setPen_client.call(r,g,b,w,off)
        rospy.loginfo("the Pen has been turn on!")
    except rospy.ServiceException, e:
        rospy.logwarn("Service call failed: %s"%e)

if __name__ == '__main__':
    #global x,y,theta,length,width  #main function doesnot need

    rospy.init_node('another_turtle', anonymous=True)#node name
    rospy.wait_for_service("spawn")
    #create a new turtle
    try:
        greetings_client = rospy.ServiceProxy("spawn",Spawn)
        resp = greetings_client.call(start_x,start_y,0,"turtle2")
        rospy.loginfo("%s"%resp)
    except rospy.ServiceException, e:
        rospy.logwarn("Service call failed: %s"%e)

    #set the pen white and turn on the pen
    setPen(255,255,255,3,0)
    #get the current position
    pose_listener=rospy.Subscriber("turtle2/pose",Pose,pose_callback)
    pose_listener_first=rospy.Subscriber("turtle1/pose",Pose,pose_callback_first)

    time.sleep(2)#it is very important,otherwise the first move() function will be fault

    move(length)
    rotate()
    set_absolute_pose(x,y,math.pi/2)
    move(width)
    rotate()
    set_absolute_pose(x,y,math.pi)
    move(length)
    rotate()
    set_absolute_pose(x,y,-math.pi/2)
    move(width)
    rotate()
    set_absolute_pose(x,y,0)
    move(length/2)
    rotate()
    set_absolute_pose(x,y,math.pi/2)
    move(width)

    setPen(255,255,255,3,1)
    set_absolute_pose(start_x+length*0.75,start_y+width/2,0)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        vel_talker=rospy.Publisher("turtle2/cmd_vel",Twist,queue_size=10)#set vertical
        vel_msg=Twist()
        vel_msg.linear.x=2*random.random()
        vel_msg.linear.y=2*random.random()
        vel_msg.angular.z=2*(2*random.random()-1)
        vel_talker.publish(vel_msg)

        if x>=start_x+length or y>=start_y+width or x<=start_x or y<=start_y:
            set_absolute_pose(start_x+length*0.75,start_y+width/2,random.random()*math.pi*2-math.pi)
        if math.sqrt((x-x_first)*(x-x_first)+(y-y_first)*(y-y_first))<safe_distance:
            set_absolute_pose(start_x+length*0.75,start_y+width/2,random.random()*math.pi*2-math.pi)
            #let the first turtle go to the middle point
            try:
                set_absolute_pose_client=rospy.ServiceProxy("turtle1/teleport_absolute",TeleportAbsolute)
                resp=set_absolute_pose_client.call(start_x+length/4,start_y+width/2,0)
            except rospy.ServiceException, e:
                rospy.logwarn("Service call failed: %s"%e)
        rate.sleep()




