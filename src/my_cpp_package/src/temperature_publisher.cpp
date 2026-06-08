#include <chrono>
#include <memory>
#include <random>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float32.hpp"

using namespace std::chrono_literals;

class TemperaturePublisher : public rclcpp::Node {
    public:
        TemperaturePublisher(): Node("temperature_publisher") {
            publisher_ = this->create_publisher<std_msgs::msg::Float32>("temperature", rclcpp::QoS(10));
            timer_ = this->create_wall_timer(1s, std::bind(&TemperaturePublisher::publish_temperature, this));
            RCLCPP_INFO(this->get_logger(), "Temperature publisher node has started.");
        }
    private:
        void publish_temperature() {
            std_msgs::msg::Float32 msg;
            msg.data = generate_temperature();

            publisher_->publish(msg);

            RCLCPP_INFO(this->get_logger(), "Published temperature: %.2f C", msg.data);
        };

        float generate_temperature() {
            static std::random_device rd;
            static std::mt19937 generator(rd());
            static std::uniform_real_distribution<float> distribution(20.0, 35.0);

            return distribution(generator);
        };
        rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr publisher_;
        rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TemperaturePublisher>();
    rclcpp::spin(node);

    rclcpp::shutdown();

    return 0;
}

