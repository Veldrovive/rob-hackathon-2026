```bash
apt update && apt install python3-pip -y
```

```bash
docker exec -it ros2_testing /bin/bash
```

```bash
source /opt/ros/jazzy/setup.bash
```

Install mbot lib
```bash
cd /workspace/mbot_hackathon_lib
python3 -m pip install -e . --break-system-packages
```

Build the ROS 2 packages
```bash
cd /workspace/mbot_hackathon
colcon build
```

```bash
source install/setup.bash
ros2 run mbot_hackathon_pkg agent_node.py
```