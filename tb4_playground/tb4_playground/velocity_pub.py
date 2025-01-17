import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TwistStamped
from std_srvs.srv import Trigger

class VelocityNode(Node):

    def __init__(self):
        super().__init__('velocity_node')
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10)
        self.subscription  # Prevent unused variable warning

        # Current position
        self.position_x = 0.00
        self.position_y = 0.00
        # Loop start position
        self.start_x = 0.00
        self.start_y = 0.00
        # Last location
        self.last_x = 0.00
        self.last_y = 0.00
        # Distance traveled, distance to the goal, and loop variable
        self.distance = 0.00
        self.nearness = 0.00
        self.do_loop = False

        # Cached parameter value
        self.z_angular_velocity = -3.0
        self.declare_parameter('z_angular_velocity', -3.0)

        # Velocity publisher
        self.publisher = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.srv = self.create_service(Trigger, 'do_loopy', self.do_loopy_callback)

        # Timer for loop callback
        timer_period = 0.1  # 10 Hz
        self.timer = self.create_timer(timer_period, self.loop_callback)

    def odom_callback(self, msg):
        """Update the current robot position from odometry."""
        self.position_x = msg.pose.pose.position.x
        self.position_y = msg.pose.pose.position.y

    def update_distance_and_nearness(self):
        """Calculate distance traveled and proximity to the goal."""
        self.distance += ((self.last_x - self.position_x)**2 + (self.last_y - self.position_y)**2)**0.5
        self.nearness = ((self.position_x - self.start_x)**2 + (self.position_y - self.start_y)**2)**0.5
        self.last_x = self.position_x
        self.last_y = self.position_y

    def loop_callback(self):
        """Main loop callback for controlling the robot."""
        if self.do_loop:
            self.update_distance_and_nearness()
            self.get_logger().info(
                "Traveled {:.2f}m, {:.2f}m to our goal.".format(self.distance, self.nearness))

            if self.distance > 0.1 and self.nearness < 0.05:
                self.do_loop = False
                self.get_logger().info("Stopping Looping")
            else:
                msg = TwistStamped()
                msg.twist.linear.x = 0.20
                msg.twist.linear.y = 0.00
                msg.twist.linear.z = 0.00
                msg.twist.angular.x = 0.00
                msg.twist.angular.y = 0.00
                msg.twist.angular.z = self.z_angular_velocity
                self.publisher.publish(msg)
        else:
            self._update_params()

    def _update_params(self):
        """Update the node's parameters."""
        new_value = self.get_parameter('z_angular_velocity').get_parameter_value().double_value
        if new_value != self.z_angular_velocity:
            self.get_logger().info(
                'Updated Z angular velocity from {0} to {1}'.format(self.z_angular_velocity, new_value))
            self.z_angular_velocity = new_value

    def do_loopy_callback(self, request, response):
        """Service callback for toggling the loop."""
        self.get_logger().info('Incoming loop request!')
        self.get_logger().info(
            "Loop starts at ({:.2f},{:.2f})".format(self.position_x, self.position_y))
        self.start_x = self.position_x
        self.start_y = self.position_y
        self.last_x = self.position_x
        self.last_y = self.position_y
        self.distance = 0.00
        self.do_loop = not self.do_loop
        response.success = True
        response.message = "Kicking off looping!" if self.do_loop else "Stopping looping!"
        return response

def main(args=None):
    rclpy.init(args=args)
    velocity_node = VelocityNode()
    rclpy.spin(velocity_node)
    velocity_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

