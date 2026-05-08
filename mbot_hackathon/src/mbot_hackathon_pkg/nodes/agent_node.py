#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from mbot_hackathon_lib.agent import Agent

try:
    from mbot_hackathon_pkg.srv import GetCommands
    from mbot_hackathon_pkg.msg import Command
except ImportError:
    raise ImportError("Could not import ROS 2 interfaces. Make sure you have sourced your workspace.")

class AgentServiceNode(Node):
    def __init__(self):
        super().__init__('agent_node')
        self.agent = Agent()
        
        # Create the service
        self.srv = self.create_service(
            GetCommands,
            'get_agent_commands',
            self.get_commands_callback
        )
        self.get_logger().info('Agent Service Node is ready to receive prompts.')

    def get_commands_callback(self, request, response):
        self.get_logger().info(f'Received prompt: "{request.prompt}"')
        
        try:
            # Get the actions from the LLM
            actions = self.agent.get_actions(request.prompt)
            self.get_logger().info(f'LLM returned {len(actions)} actions.')
            
            # Map AgentCommand Pydantic models to ROS 2 Command messages
            response.commands = []
            for action in actions:
                cmd_msg = Command()
                cmd_msg.action = action.action
                
                # Depending on the action, fill in the correct fields
                if action.action == "speak":
                    cmd_msg.content = action.content
                    cmd_msg.waypoint = ""
                elif action.action == "navigate":
                    cmd_msg.waypoint = action.waypoint
                    cmd_msg.content = ""
                
                response.commands.append(cmd_msg)
                
        except Exception as e:
            self.get_logger().error(f'Error processing prompt: {e}')
            
        return response

def main(args=None):
    rclpy.init(args=args)
    node = AgentServiceNode()
    
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
