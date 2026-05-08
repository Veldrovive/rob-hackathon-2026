#!/usr/bin/env python3
"""
This node manages the robot.
It subscribes to the speech_to_text topic to get user input.
When a command comes in, it sends it to the agent node via a service call.
When it gets the commands back, we run through the commands in sequence and split into two streams.
If the command is "speak", we make a service call to the text_to_speech node and wait for a response.
If the command is "navigate", we publish the waypoint to the navigation topic.

If a new command comes in during execution of the previous command, we ignore the new command for now.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

try:
    from mbot_hackathon_pkg.srv import GetCommands, TextToSpeech
except ImportError:
    raise ImportError("Could not import ROS 2 interfaces. Make sure you have sourced your workspace.")

class ManagerNode(Node):
    def __init__(self):
        super().__init__('manager_node')
        
        # Subscriptions
        self.speech_sub = self.create_subscription(
            String,
            'speech_to_text',
            self.speech_callback,
            10
        )
        
        # Publishers
        self.nav_pub = self.create_publisher(
            String,
            'navigate',
            10
        )
        
        # Service Clients
        self.agent_client = self.create_client(GetCommands, 'get_agent_commands')
        self.tts_client = self.create_client(TextToSpeech, 'text_to_speech')
        
        self.is_executing = False
        self.command_queue = []
        
        self.get_logger().info('Manager Node initialized.')

    def speech_callback(self, msg):
        if self.is_executing:
            self.get_logger().info('Currently executing commands, ignoring new input.')
            return
            
        self.get_logger().info(f'Received speech: "{msg.data}"')
        self.is_executing = True
        
        # Send to agent node
        if not self.agent_client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('Agent service not available')
            self.is_executing = False
            return
            
        request = GetCommands.Request()
        request.prompt = msg.data
        
        future = self.agent_client.call_async(request)
        future.add_done_callback(self.agent_response_callback)

    def agent_response_callback(self, future):
        try:
            response = future.result()
            self.command_queue = response.commands
            self.get_logger().info(f'Received {len(self.command_queue)} commands from agent.')
            self.execute_next_command()
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')
            self.is_executing = False

    def execute_next_command(self):
        if not self.command_queue:
            self.get_logger().info('Finished executing all commands.')
            self.is_executing = False
            return
            
        command = self.command_queue.pop(0)
        
        if command.action == 'speak':
            self.get_logger().info(f'Executing speak command: "{command.content}" in language {command.language}')
            if not self.tts_client.wait_for_service(timeout_sec=5.0):
                self.get_logger().error('TextToSpeech service not available, skipping.')
                self.execute_next_command()
                return
                
            request = TextToSpeech.Request()
            request.text = command.content
            request.language = command.language
            future = self.tts_client.call_async(request)
            future.add_done_callback(self.tts_response_callback)
            
        elif command.action == 'navigate':
            self.get_logger().info(f'Executing navigate command to waypoint: "{command.waypoint}"')
            
            def nav_callback(future):
                try:
                    future.result()
                except Exception as e:
                    self.get_logger().error(f'TTS service call failed: {e}')
                
                msg = String()
                msg.data = command.waypoint
                self.nav_pub.publish(msg)
                self.execute_next_command()

            if self.tts_client.wait_for_service(timeout_sec=1.0):
                request = TextToSpeech.Request()
                request.text = f"Navigating to {command.waypoint}"
                request.language = "en"
                future = self.tts_client.call_async(request)
                future.add_done_callback(nav_callback)
            else:
                self.get_logger().warn('TextToSpeech service not available for announcement.')
                msg = String()
                msg.data = command.waypoint
                self.nav_pub.publish(msg)
                self.execute_next_command()
            
        else:
            self.get_logger().warn(f'Unknown command action: {command.action}')
            self.execute_next_command()

    def tts_response_callback(self, future):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info('TTS completed successfully.')
            else:
                self.get_logger().warn('TTS reported failure.')
        except Exception as e:
            self.get_logger().error(f'TTS service call failed: {e}')
            
        self.execute_next_command()

def main(args=None):
    rclpy.init(args=args)
    node = ManagerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()