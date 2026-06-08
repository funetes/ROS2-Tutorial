#include "rclcpp/rclcpp.hpp"
#include "my_first_package_msgs/srv/robot_command.hpp" // type

#include <memory>
#include <string>
#include <chrono>
#include <cstdlib>
#include <stdexcept>

using namespace std::chrono_literals;

class EmergencyStopClient : public rclcpp::Node {
    using RobotCommand = my_first_package_msgs::srv::RobotCommand;
    public:
        EmergencyStopClient() : Node("emergency_stop_node") {
            client_ = this->create_client<RobotCommand>(
                "/emergency_stop"
            );
        };

        bool send_request(bool emergency_stop) {
            auto request = std::make_shared<RobotCommand::Request>();
            RCLCPP_ERROR(this->get_logger(),
                    "%d", emergency_stop);
            request->data = emergency_stop;

            int retry_count = 0;

            while (!client_->wait_for_service(1s)) {
                if(!rclcpp::ok()) {
                    RCLCPP_ERROR(
                        this->get_logger(),
                        "ROS interrupted while waiting for service."
                    );
                    return false;
                }

                retry_count++;

                if(retry_count >= 5) {
                    RCLCPP_ERROR(this->get_logger(),
                        "/emergency_stop service is not available."
                    );
                    return false;
                }

                 RCLCPP_ERROR(
                    this->get_logger(),
                    "waiting for /emergency_stop service..."
                );
            }
            auto future = client_->async_send_request(request);

            auto result = rclcpp::spin_until_future_complete(this->get_node_base_interface(), future);

            if(result == rclcpp::FutureReturnCode::SUCCESS) {
                auto response = future.get();

                RCLCPP_INFO(
                    this->get_logger(),
                    "Response success: %s",
                    response->success == true ? "true" : "false"
                );

                RCLCPP_INFO(
                    this->get_logger(),
                    "Response message: %s",
                    response->message.c_str()
                );
                return response->success;
            }
            RCLCPP_ERROR(
                this->get_logger(),
                "Failed to call /emergency_stop service."
            );
            return false;
        };

    private:
        rclcpp::Client<RobotCommand>::SharedPtr client_;
};

bool parse_bool_argument(const std::string &arg) {
    if(arg == "true" || arg == "1" || arg == "on" || arg == "stop") {
        return true;
    }

    if(arg == "false" || arg == "0" || arg == "off" || arg == "release") {
        return false;
    }

    throw std::invalid_argument(
        "Invalid argument. use true/false, 1/0, on/off, stop/release."
    );
}

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);

    if(argc != 2) {
        RCLCPP_ERROR(
            rclcpp::get_logger("emergency_stop_client"),
            "Uasge: ros2 run my_cpp_package emergency_stop_client true"
        );
        rclcpp::shutdown();
        return 1;
    }

    bool emergency_stop = false;

    try {
        emergency_stop = parse_bool_argument(argv[1]);
        RCLCPP_ERROR(
            rclcpp::get_logger("emergency_stop_client"),
            "%d",
            emergency_stop
        );
    } catch(const std::exception& e) {
        RCLCPP_ERROR(
            rclcpp::get_logger("emergency_stop_client"),
            "%s",
            e.what()
        );
        rclcpp::shutdown();
        return 1;
    }
    auto node = std::make_shared<EmergencyStopClient>();
    bool success = node->send_request(emergency_stop);

    rclcpp::shutdown();

    return success ? 0 : 1;
}
