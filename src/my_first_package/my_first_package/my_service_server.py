from my_first_package_msgs.srv import MultiSpawn
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import Spawn

import rclpy as rp
from rclpy.node import Node
import numpy as np
import time

class MultiSpawnClass(Node):
    def __init__(self):
        super().__init__('multi_spawn')

        self.server = self.create_service(
            MultiSpawn,
            'multi_spawn',
            self.callback_service
        )
        self.teleport = self.create_client(
            TeleportAbsolute,
            'turtle1/teleport_absolute'
        )
        self.req_teleport = TeleportAbsolute.Request()
        self.spawn = self.create_client(Spawn, '/spawn')

        while not self.spawn.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('/spawn service not available, waiting...')

        self.req_spawn = Spawn.Request()

        self.center_x = 5.54
        self.center_y = 5.54

    def calc_position(self, n ,r):
        get_theta = 2 * np.pi / n
        theta = [get_theta * n for n in range(n)]
        x = [r * np.cos(th) for th in theta]
        y = [r * np.sin(th) for th in theta]

        return x, y, theta

    def callback_service(self, req, res):
        # print('request: ',req)

        # res.x = [1., 2., 3.]
        # res.y = [10., 20., 30.]
        # res.theta = [100., 200., 300.]
        # self.req_teleport.x = 1.
        # self.teleport.call_async(self.req_teleport)

        if req.num <= 0:
            res.x = []
            res.y = []
            res.theta = []

            return res

        if req.num > 50:
            req.num = 50

        radius = 3.0

        if req.num <=4:
            radius = 2.0
        elif req.num <=10:
            radius = 3.0
        else:
            radius = 4.0

        x, y, theta = self.calc_position(req.num, radius)

        for n in range(len(theta)):
            self.req_spawn.x = x[n] + self.center_x
            self.req_spawn.y = y[n] + self.center_y
            self.req_spawn.theta = theta[n]
            self.spawn.call_async(self.req_spawn)

            time.sleep(0.1)

        res.x = x
        res.y = y
        res.theta = theta
        return res

def main(args=None):
    rp.init(args=args)

    multi_spawn = MultiSpawnClass()
    rp.spin(multi_spawn)

    rp.shutdown()

if __name__ == '__main__':
    main()
