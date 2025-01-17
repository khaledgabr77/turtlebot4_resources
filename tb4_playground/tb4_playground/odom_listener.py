import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

# Define a custom ROS 2 node that listens to odometry messages
class OdomListenerNode(Node):
    def __init__(self):
        super().__init__('odom_listener')  # Initialize the node with the name 'odom_listener'

        # Create a subscription to the '/odom' topic
        # Subscribes to Odometry messages and processes them with the 'odom_callback' method
        self.subscription = self.create_subscription(
            Odometry,         # Message type
            '/odom',          # Topic name
            self.odom_callback,  # Callback function
            10)               # Queue size
        self.subscription  # Prevent unused variable warning

    # Callback function to handle received odometry messages
    def odom_callback(self, msg):
        """
        Extracts the robot's position (x, y) from the odometry message and logs it.
        """
        self.position_x = msg.pose.pose.position.x  # Extract x-coordinate
        self.position_y = msg.pose.pose.position.y  # Extract y-coordinate

        # Log the current position
        self.get_logger().info(
            'Current position: x: %f, y: %f' % (self.position_x, self.position_y))

# Main function to initialize and run the node
def main(args=None):
    rclpy.init(args=args)  # Initialize ROS 2 client library

    # Create an instance of the OdomListenerNode
    odom_node = OdomListenerNode()

    # Keep the node running to process callbacks
    rclpy.spin(odom_node)

    # Cleanup: destroy the node and shutdown rclpy
    odom_node.destroy_node()
    rclpy.shutdown()

# Entry point of the program
if __name__ == '__main__':
    main()
