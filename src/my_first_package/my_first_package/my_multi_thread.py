import rclpy as rp
from rclpy.executors import MultiThreadedExecutor
from my_first_package.my_subscriber import TurtlesimSubscriber
from my_first_package.my_publisher import TurtlesimPublisher

def main():
    rp.init()
    executor = MultiThreadedExecutor()
    sub = TurtlesimSubscriber()
    pub = TurtlesimPublisher()

    executor.add_node(sub)
    executor.add_node(pub)

    try:
        executor.spin()
    finally:
        sub.destroy_node()
        pub.destroy_node()
        executor.shutdown()
        rp.shutdown()


if __name__ == "__main__":
    main()