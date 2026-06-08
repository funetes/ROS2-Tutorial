#include<cstdio>
#include<cstdlib>
#include<memory>
#include<string>

#include "rclcpp/rclcpp.hpp"
#include "rcutils/cmdline_parser.h"

class PatrolNode : public rclcpp::Node {
    public:
        PatrolNode(double speed, int count) : Node("patrol_node"), speed_(speed), count_(count) {
            RCLCPP_INFO(this->get_logger(), "Patrol node started.");
            RCLCPP_INFO(this->get_logger(), "Mobile robot speed: %.2f", speed_);
            RCLCPP_INFO(this->get_logger(), "Repeat count: %d", count_);
        };
    private:
        double speed_;
        int count_;
};

void print_help() {
    printf("Usage:\n");
    printf(" ros2 run my_cpp_package patrol_node [options]\n\n");


    printf("Options:\n");
    printf("  -h                         show help message\n");
    printf("  -s <speed>                 Set mobile robot speed. Default: 0.5\n");
    printf("  -c <count>                 Set repeat count. Default: 1\n");
}

int main(int argc, char *argv[]) {
    if(rcutils_cli_option_exist(argv, argv + argc, "-h")) {
        print_help();
        return 0;
    }

    rclcpp::init(argc, argv);

    double speed = 0.5;
    int count = 1;

    char * speed_option = rcutils_cli_get_option(argv, argv + argc, "-s");
    if(speed_option != nullptr) {
        try {
            speed = std::stod(speed_option);
        } catch(const std::exception& e) {
            fprintf(stderr, "Invalid speed value: %s\n\n\n", speed_option);
            print_help();
            return -1;
        }
    }

    char * count_option = rcutils_cli_get_option(argv, argv + argc, "-c");
    if(count_option != nullptr) {
        try {
            count = std::stoi(count_option);
        } catch(const std::exception& e) {
            fprintf(stderr, "Invalid count value: %s\n\n\n", count_option);
            print_help();
            return -1;
        }
    }

    auto node = std::make_shared<PatrolNode>(speed, count);

    rclcpp::spin(node);

    rclcpp::shutdown();

    return 0;
}
