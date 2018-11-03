#include<ros/ros.h>
#include<geometry_msgs/Twist.h>
#include<turtlesim/Pose.h>
#include "turtlesim/TeleportAbsolute.h"
#include "turtlesim/SetPen.h"
#include <stdio.h>
#include <iostream>
#include <std_msgs/UInt8.h>
#include "../include/my_turtle/kbhit.h"

#define KEY_UP 65
#define KEY_DOWN 66
#define KEY_LEFT 68
#define KEY_RIGHT 67
#define PI 3.1415926535897932
using namespace std;
static const double start_x=0.2;
static const double start_y=1.5;
static const double length=10.6;
static const double width=8;

void setAbsolutePosition(double x,double y,double theta){
    ros::NodeHandle nh;
    ros::ServiceClient absolutePostionClient=nh.serviceClient<turtlesim::TeleportAbsolute>("turtle1/teleport_absolute");
    turtlesim::TeleportAbsolute srv;

    srv.request.x=x;
    srv.request.y=y;
    srv.request.theta=theta;

    if(absolutePostionClient.call(srv)){
        ROS_INFO("Response from server:success!");
    }else{
        ROS_ERROR("Failed to fetch!");
    }
}
void setPen(int r,int g,int b,int w,int off){
    ros::NodeHandle nh;
    ros::ServiceClient penClient=nh.serviceClient<turtlesim::SetPen>("turtle1/set_pen");
    turtlesim::SetPen srv;
    srv.request.r=r;
    srv.request.g=g;
    srv.request.b=b;
    srv.request.width=w;
    srv.request.off=off;

    if(penClient.call(srv)){
        ROS_INFO("Response from the turtle1/set_pen server");
    } else
        ROS_ERROR("Failed to fetch!");
}

void poseCallback(const turtlesim::Pose::ConstPtr &msg){
    double x=msg->x;
    double y=msg->y;
    //ROS_INFO("the current position is %f %f",x,y);
    if(x>=start_x+length ||y>start_y+width||x<=start_x||y<=start_y){
        setAbsolutePosition(start_x+length/4,start_y+width/2,0);
    }
}

int main(int argc,char **argv){
    init_keyboard();
    ros::init(argc,argv,"key_control_turtule_ndoe");//the node's name
    ros::NodeHandle nh;
    ros::service::waitForService("turtle1/set_pen");
    ros::Rate loop_rate(10);


    setPen(255,255,255,3,1);
    setAbsolutePosition(start_x+length/4,start_y+width/2,0);

    ros::Publisher keyTalker=nh.advertise<geometry_msgs::Twist>("turtle1/cmd_vel",1);//set the key event
    ros::Subscriber poseSub = nh.subscribe("turtle1/pose", 1, poseCallback); //subcribe current position event

    geometry_msgs::Twist msg,msg_up,msg_down,msg_left,msg_right;//the message info
    const int const_v=2;
    msg_up.linear.x=const_v;
    msg_down.linear.x=-const_v;
    msg_left.angular.z=const_v;
    msg_right.angular.z=-const_v;


    //ros::spin();//receive the positon of the turtle

    string tip="";

    while(ros::ok()){
        if(kbhit()) {
            int ch = readch();
            if(ch==27){
                int ch2=readch();
                int ch3=readch();
                switch (ch3){
                    case KEY_UP:
                        tip="up key been clicked\n";
                        msg=msg_up;
                        break;
                    case KEY_DOWN:
                        tip="down key been clicked\n";
                        msg=msg_down;
                        break;
                    case KEY_LEFT:
                        tip="left key been clicked\n";
                        msg=msg_left;
                        break;
                    case KEY_RIGHT:
                        tip="right key been clicked\n";
                        msg=msg_right;
                        break;
                }
                keyTalker.publish(msg);
                ROS_INFO("%s:x=%f,y=%f,z=%f,ax=%f,ay=%f,az=%f",tip.c_str(),msg.linear.x,msg.linear.y,msg.linear.z,msg.angular.x,msg.angular.y,msg.angular.z);
            }
        }
        ros::spinOnce();


        //loop_rate.sleep();
    }
    return 0;
}
