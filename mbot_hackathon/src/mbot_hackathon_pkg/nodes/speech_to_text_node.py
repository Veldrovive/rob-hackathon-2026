#!/usr/bin/env python3
"""
Node that captures speech from the microphone in push-to-talk mode.
Press spacebar to start recording, press spacebar again to stop and process.
Uses the speech_recognition library to convert recorded audio to text and publishes
the recognized text to the speech_to_text topic.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import threading
import speech_recognition as sr
import pyaudio
import sys
import tty
import termios
import select

class SpeechToTextNode(Node):
    def __init__(self):
        super().__init__('speech_to_text_node')
        self.publisher_ = self.create_publisher(String, 'speech_to_text', 10)
        self.get_logger().info('Speech-to-Text Node started. Press spacebar to start/stop recording.')
        
        # Initialize recognizer and audio
        self.recognizer = sr.Recognizer()
        self.p = pyaudio.PyAudio()
        self.recording = False
        self.frames = []
        self.stream = None
        
        # Start keyboard monitoring thread
        self.keyboard_thread = threading.Thread(target=self.keyboard_loop, daemon=True)
        self.keyboard_thread.start()

    def keyboard_loop(self):
        """Monitor spacebar presses to toggle recording."""
        def getch():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setcbreak(sys.stdin.fileno())
                while rclpy.ok():
                    i, o, e = select.select([sys.stdin], [], [], 0.1)
                    if i:
                        return sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return None

        while rclpy.ok():
            try:
                ch = getch()
                if ch == ' ':
                    if self.recording:
                        self.recording = False
                        self.get_logger().info('Stopped recording')
                        # Process the recorded audio
                        self.process_audio()
                    else:
                        self.recording = True
                        self.frames = []
                        self.get_logger().info('Started recording')
                        # Start recording thread
                        threading.Thread(target=self.record_audio, daemon=True).start()
            except Exception as e:
                self.get_logger().error(f'Keyboard error: {e}')

    def record_audio(self):
        """Record audio while recording flag is True."""
        try:
            self.stream = self.p.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=16000,
                                      input=True,
                                      frames_per_buffer=1024)
            while self.recording and rclpy.ok():
                data = self.stream.read(1024, exception_on_overflow=False)
                self.frames.append(data)
        except Exception as e:
            self.get_logger().error(f'Recording error: {e}')
        finally:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None

    def process_audio(self):
        """Process recorded audio and publish recognized text."""
        if not self.frames:
            return
        
        try:
            audio_data = b''.join(self.frames)
            audio = sr.AudioData(audio_data, 16000, 2)  # 16kHz, 2 bytes per sample
            
            text = self.recognizer.recognize_google(audio)
            msg = String()
            msg.data = text
            self.publisher_.publish(msg)
            self.get_logger().info(f'Published: "{text}"')
        except sr.UnknownValueError:
            self.get_logger().warn('Could not understand audio')
        except sr.RequestError as e:
            self.get_logger().error(f'Speech recognition service error: {e}')
        except Exception as e:
            self.get_logger().error(f'Processing error: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = SpeechToTextNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.stream:
            node.stream.stop_stream()
            node.stream.close()
        node.p.terminate()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()