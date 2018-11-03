#include "ros/ros.h"
#include "topic_demo/Greeting.h"

int main(int argc,char **argv){
	ros::init(argc,argv,"greeting_client");
	ros::NodeHandle nh;
	ros::ServiceClient client=nh.serviceClient<topic_demo::Greeting>("greetings");
	topic_demo::Greeting srv;

	srv.request.name="xu";
	srv.request.age=20;
	if(client.call(srv)){
		ROS_INFO("Response from server:%s",srv.response.feedback.c_str());
	}else{
		ROS_ERROR("Failed to fetch!");
	}
	return 0;
}
