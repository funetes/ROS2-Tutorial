#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float32.hpp"

class TemperatureSubscriber : public rclcpp::Node {
    public:
        TemperatureSubscriber(): Node("temperature_subscriber") {
            subscription_ = this->create_subscription<std_msgs::msg::Float32>(
                "temperature",
                rclcpp::QoS(10),
                std::bind(
                    &TemperatureSubscriber::temperature_callback,
                    this,
                    std::placeholders::_1
                )
            );
            RCLCPP_INFO(this->get_logger(), "Temperature subscriber node has started.");
        };
    private:

        void temperature_callback(const std_msgs::msg::Float32::SharedPtr msg) {
            RCLCPP_INFO(this->get_logger(), "Received temperature: %.2f C", msg->data);

            if (msg->data >= 30.0) {
                RCLCPP_WARN(this->get_logger(), "Tempertatue is high. Cooling check is recommended");
            }
        }

        rclcpp::Subscription<std_msgs::msg::Float32>::SharedPtr subscription_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TemperatureSubscriber>();

    rclcpp::spin(node);

    rclcpp::shutdown();

    return 0;
}
