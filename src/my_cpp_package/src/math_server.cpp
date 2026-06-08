#include <memory>
#include <string>
#include <functional>

#include "rclcpp/rclcpp.hpp"
#include "my_first_package_msgs/srv/calculate_twonumbers.hpp"

class MathServer: public rclcpp::Node {
    public:
        using CalculateTwoNumbers = my_first_package_msgs::srv::CalculateTwonumbers;

        MathServer(): Node("math_server") {
            service_ = this->create_service<CalculateTwoNumbers>(
                "Calculate_two_numbers",
                std::bind(&MathServer::handle_request,
                this,
                std::placeholders::_1,
                std::placeholders::_2)
            );
            RCLCPP_INFO(this->get_logger(), "Math service server is ready.");
        };
    private:
        void handle_request(
            const std::shared_ptr<CalculateTwoNumbers::Request> request,
            std::shared_ptr<CalculateTwoNumbers::Response> response) {
                const double x = request->x;
                const double y = request->y;
                const std::string op = request->arithmetic_operator;

                response->success = true;
                response->message = "calculatation completed.";

                if(op == "add") {
                    response->result = x + y;
                } else if (op == "subtract") {
                    response->result = x - y;
                } else if (op == "multifly") {
                    response->result = x * y;
                } else if ( op == "divide") {
                    if (y == 0) {
                        response->result = 0.0;
                        response->success = false;
                        response->message = "division by zero is not allowed.";
                    } else {
                        response->result = x / y;
                    }
                }else {
                    response->result = 0.0;
                    response->success = false;
                    response->message = "unknown operator";
                }

                RCLCPP_INFO(this->get_logger(),
                    "Request: %.2f %s %.2f -> Result: %.2f, Success: %s , Message: %s",
                    x,
                    op.c_str(),
                    y,
                    response->result,
                    response->success ? "true" : "false",
                    response->message.c_str()
                );
            }

        rclcpp::Service<CalculateTwoNumbers>::SharedPtr service_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MathServer>();
    rclcpp::spin(node);

    rclcpp::shutdown();

    return 0;
}
