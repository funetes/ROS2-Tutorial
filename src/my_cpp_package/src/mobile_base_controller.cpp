#include <rclcpp/rclcpp.hpp>
#include <rcl_interfaces/msg/set_parameters_result.hpp>

class MobileBaseController : public rclcpp::Node {
    public:
        MobileBaseController() : Node("mobile_base_controller") {
            this->declare_parameter<double>("max_linear_velocity", 0.6);
            this->declare_parameter<double>("max_angular_velocity", 1.2);
            this->declare_parameter<double>("obstacle_stop_distance", 0.5);
            this->declare_parameter<double>("control_frequency", 50.0);
            this->declare_parameter<std::string>("base_frame", "base_link");
            this->declare_parameter<std::string>("odom_frame", "odom");

            max_linear_velocity_ = this->get_parameter("max_linear_velocity").as_double();
            max_angular_velocity_ = this->get_parameter("max_angular_velocity").as_double();
            obstacle_stop_distance_ = this->get_parameter("obstacle_stop_distance").as_double();
            control_frequency_ = this->get_parameter("control_frequency").as_double();
            base_frame_ = this->get_parameter("base_frame").as_string();
            odom_frame_ = this->get_parameter("odom_frame").as_string();

            parameter_callback_handle_ = this->add_on_set_parameters_callback(
                std::bind(
                    &MobileBaseController::onParameterChanged,
                    this,
                    std::placeholders::_1
                )
            );

            printParameters();

        }

    private:
        double max_linear_velocity_;
        double max_angular_velocity_;
        double obstacle_stop_distance_;
        double control_frequency_;
        std::string base_frame_;
        std::string odom_frame_;

        OnSetParametersCallbackHandle::SharedPtr parameter_callback_handle_;

        void printParameters() {
            RCLCPP_INFO(this->get_logger(), "max_linear_velocity: %.2f" ,max_linear_velocity_);
            RCLCPP_INFO(this->get_logger(), "max_angular_velocity: %.2f" ,max_angular_velocity_);
            RCLCPP_INFO(this->get_logger(), "obstacle_stop_distance: %.2f" ,obstacle_stop_distance_);
            RCLCPP_INFO(this->get_logger(), "control_frequency: %.2f" ,control_frequency_);
            RCLCPP_INFO(this->get_logger(), "base_frame: %s" ,base_frame_.c_str());
            RCLCPP_INFO(this->get_logger(), "odom_frame: %s" ,odom_frame_.c_str());
        }

        rcl_interfaces::msg::SetParametersResult onParameterChanged(const std::vector<rclcpp::Parameter> &parameters) {
            rcl_interfaces::msg::SetParametersResult result;
            result.successful = true;

            for (auto &param : parameters) {
                if(param.get_name() == "max_linear_velocity") {
                    double value = param.as_double();

                    if(value < 0.0) {
                        result.successful = false;
                        result.reason = "max_linear_velocity must be greater than or equal to 0.0";
                        return result;
                    }

                    max_angular_velocity_ = value;
                    RCLCPP_INFO(
                        this->get_logger(),
                        "Updated max_linear_velocity: %.2f",
                        max_linear_velocity_
                    );
                }

                if(param.get_name() == "max_angular_velocity") {
                    double value = param.as_double();

                    if(value < 0.0) {
                        result.successful = false;
                        result.reason = "max_angular_velocity must be greater than or equal to 0.0";
                        return result;
                    }

                    max_angular_velocity_ = value;
                    RCLCPP_INFO(
                        this->get_logger(),
                        "Updated max_angular_velocity: %.2f",
                        max_linear_velocity_
                    );
                }

                if(param.get_name() == "obstacle_stop_distance") {
                    double value = param.as_double();

                    if(value < 0.0) {
                        result.successful = false;
                        result.reason = "obstacle_stop_distance must be greater than or equal to 0.0";
                        return result;
                    }

                    obstacle_stop_distance_ = value;
                    RCLCPP_INFO(
                        this->get_logger(),
                        "Updated obstacle_stop_distance: %.2f",
                        max_linear_velocity_
                    );
                }

                if(param.get_name() == "control_frequency") {
                    double value = param.as_double();

                    if(value < 0.0) {
                        result.successful = false;
                        result.reason = "control_frequency must be greater than  0.0";
                        return result;
                    }

                    control_frequency_ = value;
                    RCLCPP_INFO(
                        this->get_logger(),
                        "Updated control_frequency: %.2f",
                        max_linear_velocity_
                    );
                }
            }

            return result;
        }
};

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MobileBaseController>());
    rclcpp::shutdown();
    return 0;
}
