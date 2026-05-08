```bash
sudo apt update && sudo apt install python3-pip -y
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

```bash
sudo apt install python3-colcon-common-extensions -y
```

check the install
```bash
ros2 run demo_nodes_cpp talker
# In another window
ros2 run demo_nodes_cpp listener
```

Install dev essentails
```bash
sudo apt update
sudo apt install -y git build-essential
```

```bash
sudo apt install -y libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev libxml2-dev \
libxmlsec1-dev libffi-dev liblzma-dev
```

```bash
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
sudo apt update && sudo apt install python3-pip -y
```

```bash
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
```

Getting the port forwarded
```bash
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
```

```bash
ifconfig
```
Get the ip

```bash
ssh -R 8000:localhost:8000 <vm_username>@<vm_ip>
```

Installing the mbot hackathon project
```bash
git clone https://github.com/Veldrovive/rob-hackathon-2026.git
```

```bash
cd ./rob-hackathon-2026/mbot_hackathon_lib
python3 -m pip install -e . --break-system-packages
python3 -m pip install pyttsx3 --break-system-packages
```

```bash
sudo apt update
sudo apt install espeak alsa-utils -y
```

```bash
cd ./rob-hackathon-2026/mbot_hackathon
colcon build
```

```bash
source install/setup.bash
```

```bash
source install/setup.bash
ros2 run mbot_hackathon_pkg agent_node.py
```

```bash
source install/setup.bash
ros2 run mbot_hackathon_pkg manager_node.py
```

For testing
```bash
source install/setup.bash
ros2 run mbot_hackathon_pkg test_speech_to_text_node.py
```

```bash
source install/setup.bash
ros2 run mbot_hackathon_pkg test_text_to_speech_node.py
```

For real
```bash
source install/setup.bash
ros2 run mbot_hackathon_pkg text_to_speech_node.py
```