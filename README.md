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

## Setting up UTM image
Download UTM and an Ubuntu image (e.g. 24.04 LTS). Open UTM and create a new VM with the image.
Before actually starting the image, go to edit for the VM, select Network, and change the network mode to Bridged. Choose the wifi adapter you are using.

Boot into the VM and go through the install process. Once it is installed, shut down the VM and on the UTM main page scroll to the bottom of the VM where it says CD/DVD and clear the install medium. Boot back up.

Install ros by running the commands:
```bash
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

```bash
sudo apt install software-properties-common -y
sudo add-apt-repository universe -y
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

```bash
sudo apt update
sudo apt install ros-jazzy-desktop -y
```

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

check the install
```bash
ros2 run demo_nodes_cpp talker
# In another window
ros2 run demo_nodes_cpp listener
```