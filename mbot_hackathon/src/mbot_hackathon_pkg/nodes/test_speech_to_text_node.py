#!/usr/bin/env python3
"""
Node that publishes on the speech_to_text topic for testing.
Takes user input and publishes it to the speech_to_text topic.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import threading
import sys

class TestSpeechToTextNode(Node):
    def __init__(self):
        super().__init__('test_speech_to_text_node')
        self.publisher_ = self.create_publisher(String, 'speech_to_text', 10)
        self.get_logger().info('Test Speech-to-Text Node started. Type your message and press Enter.')
        
        self.input_thread = threading.Thread(target=self.input_loop, daemon=True)
        self.input_thread.start()

    def input_loop(self):
        while rclpy.ok():
            try:
                user_input = sys.stdin.readline()
                if not user_input:
                    break
                user_input = user_input.strip()
                if user_input:
                    msg = String()
                    msg.data = user_input
                    self.publisher_.publish(msg)
                    self.get_logger().info(f'Published: "{msg.data}"')
            except Exception:
                pass

def main(args=None):
    rclpy.init(args=args)
    node = TestSpeechToTextNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()