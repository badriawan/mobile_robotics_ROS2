#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"

using namespace std::chrono_literals;

/* This example creates a subclass of Node and uses std::bind() to register a
* member function as a callback from the timer. */

class Drive : public rclcpp::Node
{
  public:
    Drive()
    : Node("drive_publisher") //count_(0)
    {
      this->declare_parameter<std::string>("cmd_vel_topic", "/turtle1/cmd_vel");
      this->declare_parameter<double>("linear_velocity", 2.0);

      std::string cmd_vel_topic = this->get_parameter("cmd_vel_topic").as_string();
      linear_velocity_ = this->get_parameter("linear_velocity").as_double();


      
      publisher_1 = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
      timer_1 = this->create_wall_timer(
      500ms, std::bind(&Drive::timer_callback, this));
      publisher_2 = this->create_publisher<geometry_msgs::msg::Twist>("/turtle2/cmd_vel", 10);
      timer_2 = this->create_wall_timer(
      500ms, std::bind(&Drive::timer_callback2, this));
    }

  private:
    double linear_velocity_;

    void timer_callback()
    {
      auto message = geometry_msgs::msg::Twist();
      message.linear.x = linear_velocity_;
      RCLCPP_INFO(this->get_logger(), "Publishing: '%d'", message);
      publisher_1->publish(message);
    }
    
    void timer_callback2()
    {
      auto message = geometry_msgs::msg::Twist();
      message.linear.x = linear_velocity_;
      publisher_2->publish(message);
    }
    
    rclcpp::TimerBase::SharedPtr timer_1;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_1;
    rclcpp::TimerBase::SharedPtr timer_2;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_2;
    
    
    //size_t count_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Drive>());
  rclcpp::shutdown();
  return 0;
}
