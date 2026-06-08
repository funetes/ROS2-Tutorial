#include <memory>
#include <string>
#include <chrono>

#include "rclcpp/rclcpp.hpp"
#include "my_first_package_msgs/srv/calculate_twonumbers.hpp"

using namespace std::chrono_literals;

class MathClient : public rclcpp::Node {
    public:
        using CalculateTwonumbers = my_first_package_msgs::srv::CalculateTwonumbers;

        MathClient() : Node("math_client") {
            client_ = this->create_client<CalculateTwonumbers>("Calculate_two_numbers");
        };

        void send_request(double x, double y, const std::string & op) {
            while (!client_->wait_for_service(1s)) {
                if(!rclcpp::ok()) {
                    RCLCPP_ERROR(this->get_logger(), "Error..");
                    return;
                }

                RCLCPP_INFO(this->get_logger(), "waiting...");
            };

            auto request = std::make_shared<CalculateTwonumbers::Request>();

            request->x = x;
            request->y = y;
            request->arithmetic_operator = op;

            auto future = client_->async_send_request(request);

            if(rclcpp::spin_until_future_complete(this->get_node_base_interface(), future) == rclcpp::FutureReturnCode::SUCCESS) {
                auto response = future.get();

                RCLCPP_INFO(this->get_logger(),
                    "Result: %.2f, Success: %s, Message: %s",
                    response->result,
                    response->success ? "true" : "false",
                    response->message.c_str()
                );
            } else {
                RCLCPP_ERROR(this->get_logger(), "Failed to call service.");
            }
        };
    private:
        rclcpp::Client<CalculateTwonumbers>::SharedPtr client_;
};

int main(int argc, char * argv[]){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MathClient>();
    node->send_request(12.0, 5.0, "divide");

    rclcpp::shutdown();

    return 0;
}

