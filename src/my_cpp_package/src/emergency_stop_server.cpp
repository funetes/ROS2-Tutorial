#include "rclcpp/rclcpp.hpp"
#include "my_first_package_msgs/srv/robot_command.hpp" // type

#include <memory>
#include <string>

class EmergencyStopServer : public rclcpp::Node {
    public:
        using RobotCommand = my_first_package_msgs::srv::RobotCommand;
        EmergencyStopServer() : Node("emergency_stop_server") {
            // create_service<interface>
            service_ = this->create_service<RobotCommand>(
                "/emergency_stop",
                std::bind( // register callback function
                    &EmergencyStopServer::handle_emergency_stop,
                    this,
                    std::placeholders::_1,
                    std::placeholders::_2)
            );

            RCLCPP_INFO(this->get_logger(), "Emergency stop server is ready.");
        }
    private:
        rclcpp::Service<RobotCommand>::SharedPtr service_;

        void handle_emergency_stop(
            const std::shared_ptr<RobotCommand::Request> request,  // const <- read only, type parameter
            std::shared_ptr<RobotCommand::Response> response
        ) {
            if(request->data) {
                response->success = true;
                response->message = "Mobile robot emergency stop activated.";

                RCLCPP_WARN(this->get_logger(), "Emergency stop ACTIVATED.");
            } else {
                response->success = true;
                response->message = "Mobile robot emergency stop released.";

                RCLCPP_INFO(this->get_logger(), "Emergency stop RELEASED.");
            }
        }
};

int main(int argc, char * argv[]){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<EmergencyStopServer>();

    rclcpp::spin(node);

    rclcpp::shutdown();

    return 0;
}
