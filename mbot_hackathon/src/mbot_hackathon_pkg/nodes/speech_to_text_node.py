#!/usr/bin/env python3
"""
Node that captures speech from the microphone and publishes recognized text.
Uses the speech_recognition library to convert speech to text and publishes
the recognized text to the speech_to_text topic.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import threading
import speech_recognition as sr

class SpeechToTextNode(Node):
    def __init__(self):
        super().__init__('speech_to_text_node')
        self.publisher_ = self.create_publisher(String, 'speech_to_text', 10)
        self.get_logger().info('Speech-to-Text Node started. Listening for speech...')
        
        # Initialize recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Start listening thread
        self.listening_thread = threading.Thread(target=self.listen_loop, daemon=True)
        self.listening_thread.start()

    def listen_loop(self):
        """Continuously listen for speech and publish recognized text."""
        with self.microphone as source:
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        while rclpy.ok():
            try:
                with self.microphone as source:
                    # Listen for audio with a timeout of 10 seconds
                    audio = self.recognizer.listen(source, timeout=10)
                
                # Recognize speech using Google Speech Recognition
                try:
                    text = self.recognizer.recognize_google(audio)
                    self.get_logger().info(f'Recognized: "{text}"')
                    
                    # Publish the recognized text
                    msg = String()
                    msg.data = text
                    self.publisher_.publish(msg)
                    self.get_logger().info(f'Published: "{msg.data}"')
                    
                except sr.UnknownValueError:
                    self.get_logger().warn('Could not understand audio')
                except sr.RequestError as e:
                    self.get_logger().error(f'Speech recognition service error: {e}')
                    
            except sr.WaitTimeoutError:
                # Timeout waiting for speech, just continue listening
                pass
            except Exception as e:
                self.get_logger().error(f'Error in listen loop: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = SpeechToTextNode()
    
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