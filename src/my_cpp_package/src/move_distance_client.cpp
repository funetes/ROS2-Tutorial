#include <chrono>
#include <memory>
#include <thread>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "my_first_package_msgs/action/move_distance.hpp"


using namespace std::chrono_literals;

class MoveDistanceClient : public rclcpp::Node {
    public:
        using MoveDistance = my_first_package_msgs::action::MoveDistance;
        using GoalHandleMoveDistance = rclcpp_action::ClientGoalHandle<MoveDistance>;

        MoveDistanceClient(): Node("move_distance_client") {
            action_client_ = rclcpp_action::create_client<MoveDistance>(
                this,
                "move_distance"
            );
        }

        void send_goal(float target_distance) {
            if(!action_client_->wait_for_action_server(5s)) {
                RCLCPP_ERROR(this->get_logger(), "Action server not available.");
                return;
            }

            auto goal_msg = MoveDistance::Goal();
            goal_msg.target_distance = target_distance;

            RCLCPP_INFO(
                this->get_logger(),
                "sending goal: move %.2f meters",
                target_distance
            );

            auto send_goal_options = rclcpp_action::Client<MoveDistance>::SendGoalOptions();

            send_goal_options.feedback_callback = std::bind(
                &MoveDistanceClient::feedback_callback,
                this,
                std::placeholders::_1,
                std::placeholders::_2
            );

            send_goal_options.result_callback = std::bind(
                &MoveDistanceClient::result_callback,
                this,
                std::placeholders::_1
            );

            action_client_->async_send_goal(goal_msg, send_goal_options);
        }
    private:
        rclcpp_action::Client<MoveDistance>::SharedPtr action_client_;

        void goal_response_callback(const GoalHandleMoveDistance::SharedPtr &goal_handle) {
            if (!goal_handle) {
                RCLCPP_ERROR(this->get_logger(), "Goal was rejected by server.");
            } else {
                RCLCPP_INFO(this->get_logger(), "Goal accepted by server.");
            }
        }

        void feedback_callback(
            GoalHandleMoveDistance::SharedPtr,
            const std::shared_ptr<const MoveDistance::Feedback> feedback
        ) {
            RCLCPP_INFO(
                this->get_logger(),
                "Feedback received: %.2f m, %.1f %%",
                feedback->current_distance,
                feedback->progress
            );
        }

        void result_callback(const GoalHandleMoveDistance::WrappedResult &result) {
            switch (result.code)
            {
            case rclcpp_action::ResultCode::SUCCEEDED:
                RCLCPP_INFO(this->get_logger(), "Result: success");
                break;
            case rclcpp_action::ResultCode::ABORTED:
                RCLCPP_ERROR(this->get_logger(), "Result: aborted");
                rclcpp::shutdown();
                return;
            case rclcpp_action::ResultCode::CANCELED:
                RCLCPP_WARN(this->get_logger(), "Result: canceled");
                rclcpp::shutdown();
                return;
            default:
                RCLCPP_ERROR(this->get_logger(), "Unkown result code");
                rclcpp::shutdown();
                return;
            }

            RCLCPP_INFO(this->get_logger(),
                "Message: %s",
                result.result->message.c_str()
            );

            rclcpp::shutdown();
        }
};

int main(int argc, char* argv[]) {
    rclcpp::init(argc, argv);

    float target_distance = 1.0;

    if(argc >= 2) {
        target_distance = std::atof(argv[1]);
    }
    auto action_client = std::make_shared<MoveDistanceClient>();

    action_client->send_goal(target_distance);

    rclcpp::spin(action_client);

    return 0;
}
