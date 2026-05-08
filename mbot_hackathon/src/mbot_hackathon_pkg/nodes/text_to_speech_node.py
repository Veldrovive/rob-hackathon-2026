#!/usr/bin/env python3
"""
Real Text-to-Speech service that listens for text_to_speech service calls 
and speaks them out loud using pyttsx3 (espeak).
"""

import rclpy
from rclpy.node import Node
import pyttsx3

try:
    from mbot_hackathon_pkg.srv import TextToSpeech
except ImportError:
    raise ImportError("Could not import ROS 2 interfaces. Make sure you have sourced your workspace.")

class RealTextToSpeechNode(Node):
    def __init__(self):
        super().__init__('real_text_to_speech_node')
        
        # Initialize the TTS engine
        self.engine = pyttsx3.init()
        
        # --- Robot Voice Tuning ---
        # eSpeak is naturally robotic, but we can tweak it
        # Slow down the speech rate a bit for that deliberate, mechanical feel
        self.engine.setProperty('rate', 140) # Default is usually around 200
        
        self.srv = self.create_service(TextToSpeech, 'text_to_speech', self.tts_callback)
        self.get_logger().info('Real Text-to-Speech Node started. Awaiting text...')

    def tts_callback(self, request, response):
        self.get_logger().info(f'Speaking: "{request.text}"')
        
        try:
            # Queue the text and block until it finishes speaking
            self.engine.say(request.text)
            self.engine.runAndWait()
            
            self.get_logger().info('Finished speaking.')
            response.success = True
            
        except Exception as e:
            self.get_logger().error(f'Failed to speak: {e}')
            response.success = False
            
        return response

def main(args=None):
    rclpy.init(args=args)
    node = RealTextToSpeechNode()
    
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