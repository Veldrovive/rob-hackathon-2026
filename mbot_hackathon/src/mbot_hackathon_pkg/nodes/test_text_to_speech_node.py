#!/usr/bin/env python3
"""
Test service that listens for text_to_speech service calls and prints them.
Also delays for a time dependent on the length of the text to speech message before responding to the service call.
"""

import rclpy
from rclpy.node import Node
import time

try:
    from mbot_hackathon_pkg.srv import TextToSpeech
except ImportError:
    raise ImportError("Could not import ROS 2 interfaces. Make sure you have sourced your workspace.")

class TestTextToSpeechNode(Node):
    def __init__(self):
        super().__init__('test_text_to_speech_node')
        self.srv = self.create_service(TextToSpeech, 'text_to_speech', self.tts_callback)
        self.get_logger().info('Test Text-to-Speech Node started and ready to receive requests.')

    def tts_callback(self, request, response):
        self.get_logger().info(f'Speaking: "{request.text}"')
        
        # Delay based on length of message
        delay_time = len(request.text) * 0.05
        time.sleep(delay_time)
        
        self.get_logger().info('Finished speaking.')
        response.success = True
        return response

def main(args=None):
    rclpy.init(args=args)
    node = TestTextToSpeechNode()
    
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