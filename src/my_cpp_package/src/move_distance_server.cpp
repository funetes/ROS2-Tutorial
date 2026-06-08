#include <chrono>
#include <memory>
#include <thread>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "my_first_package_msgs/action/move_distance.hpp"

using namespace std::chrono_literals;

class MoveDistanceServer : public rclcpp::Node {
    public:
        using MoveDistance = my_first_package_msgs::action::MoveDistance;
        using GoalHandleMoveDistance = rclcpp_action::ServerGoalHandle<MoveDistance>;

        MoveDistanceServer() : Node("move_distance_server") {
            action_server_ = rclcpp_action::create_server<MoveDistance>(
                this,
                "move_distance",
                std::bind(&MoveDistanceServer::handle_goal, this, std::placeholders::_1, std::placeholders::_2),
                std::bind(&MoveDistanceServer::handle_cancel, this, std::placeholders::_1),
                std::bind(&MoveDistanceServer::handle_accepted, this, std::placeholders::_1)
            );

            RCLCPP_INFO(this->get_logger(), "Move Distance Action server started.");
        }
    private:
        rclcpp_action::Server<MoveDistance>::SharedPtr action_server_;

        rclcpp_action::GoalResponse handle_goal(
            const rclcpp_action::GoalUUID &uuid,
            std::shared_ptr<const MoveDistance::Goal> goal
        ) {
            (void)uuid;

            RCLCPP_INFO(
                this->get_logger(),
                "Received goal: move %.2f meters",
                goal->target_distance
            );

            if (goal->target_distance <= 0.0) {
                RCLCPP_WARN(this->get_logger(), "rejected goal, Distance must be grater than 0.");
                return rclcpp_action::GoalResponse::REJECT;
            }

            return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
        };

        rclcpp_action::CancelResponse handle_cancel(
            const std::shared_ptr<GoalHandleMoveDistance> goal_handle
        ) {
            (void)goal_handle;
            RCLCPP_INFO(this->get_logger(), "goal canceled");
            return rclcpp_action::CancelResponse::ACCEPT;
        };

        void handle_accepted(
            const std::shared_ptr<GoalHandleMoveDistance> goal_handle
        ) {
            std::thread {
                std::bind(&MoveDistanceServer::execute, this, std::placeholders::_1),
                goal_handle
            }.detach();
        };

        void execute(const std::shared_ptr<GoalHandleMoveDistance> goal_handle) {
            RCLCPP_INFO(this->get_logger(), "executed");

            const auto goal = goal_handle->get_goal();

            auto feedback = std::make_shared<MoveDistance::Feedback>();
            auto result = std::make_shared<MoveDistance::Result>();

            rclcpp::Rate loop_rate(2);

            float current_distance = 0.0;
            const float step_distance = 0.1;

            while (current_distance < goal->target_distance)
            {
                if(goal_handle->is_canceling()) {
                    result->success = false;
                    result->message = "Goal canceled.";
                    goal_handle->canceled(result);

                    RCLCPP_INFO(this->get_logger(), "Goal canceled.");
                    return;
                }

                current_distance += step_distance;

                if(current_distance > goal->target_distance) {
                    current_distance = goal->target_distance;
                }

                feedback->current_distance = current_distance;
                feedback->progress = current_distance / goal->target_distance * 100.0;

                goal_handle->publish_feedback(feedback);

                RCLCPP_INFO(
                    this->get_logger(),
                    "Feedback: current_distance = %.2f m , progress = %.1f %%",
                    feedback->current_distance,
                    feedback->progress
                );

                loop_rate.sleep();
            }

            if(rclcpp::ok()) {
                result->success = true;
                result->message = "Target distance reached.";
                goal_handle->succeed(result);

                RCLCPP_INFO(this->get_logger(), "Goal Succedded.");
            }
        }
};

int main(int argc, char* argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MoveDistanceServer>();
    rclcpp::spin(node);

    rclcpp::shutdown();
    return 0;
}
