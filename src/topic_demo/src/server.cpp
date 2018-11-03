#include<ros/ros.h>
// all function with ros head are all in ros/ros.h headfile
#include<topic_demo/Greeting.h>
//topic_demo/srv/Greetin.srv    srv file generate .h

bool handle_function(topic_demo::Greeting::Request &req,topic_demo::Greeting::Response &res){
	ROS_INFO("Reques from client: %s,%d",req.name.c_str(),req.age);
	res.feedback="HI "+req.name+" I am a service";
	return true;
}

int main(int argc,char **argv){
	ros::init(argc,argv,"greeting_server");
	ros::NodeHandle nh;
	ros::ServiceServer service=nh.advertiseService("greetings",handle_function);
	ros::spin();
	return 0;
}
