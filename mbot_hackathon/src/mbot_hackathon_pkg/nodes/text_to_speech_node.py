#!/usr/bin/env python3
"""
Multilingual Robot Text-to-Speech service using pyttsx3 (espeak).
"""

import rclpy
from rclpy.node import Node
import pyttsx3

try:
    from mbot_hackathon_pkg.srv import TextToSpeech
except ImportError:
    raise ImportError("Could not import ROS 2 interfaces. Make sure you have sourced your workspace.")

class MultilingualTTSNode(Node):
    def __init__(self):
        super().__init__('multilingual_tts_node')
        
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 140) # Keep it slow and robotic

        self.set_language('en') 
        
        self.srv = self.create_service(TextToSpeech, 'text_to_speech', self.tts_callback)
        self.get_logger().info('Multilingual TTS Node started.')

    def set_language(self, language_code):
        """
        Switches the espeak voice to the requested language.
        Common codes: 'en' (English), 'es' (Spanish), 'fr' (French), 'de' (German)
        """
        voices = self.engine.getProperty('voices')
        
        for voice in voices:
            if language_code in voice.languages or language_code in voice.id:
                if language_code == "es" and "merican" not in voice.name:
                    continue
                self.engine.setProperty('voice', voice.id)
                self.get_logger().info(f"Voice changed to: {voice.name} ({language_code})")
                return True
                
        self.get_logger().warn(f"Language '{language_code}' not found. Sticking with default.")
        return False

    def tts_callback(self, request, response):
        self.get_logger().info(f'Speaking: "{request.text}" in {request.language}')
        
        try:
            self.set_language(request.language)
            
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
    node = MultilingualTTSNode()
    
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