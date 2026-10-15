FROM osrf/ros:humble-desktop-full

# Arbeitsverzeichnis festlegen
WORKDIR /workspace

# Umgebungsvariablen für ROS2 und Display (GUI) einrichten
ENV ROS_DISTRO=humble
ENV QT_X11_NO_MITSHM=1

# Grundlegende Tools und ROS2-Pakete für TurtleBot3 installieren
RUN apt-get update && apt-get install -y \
    ros-humble-turtlebot3* \
    ros-humble-nav2-* \
    ros-humble-slam-toolbox \
    python3-colcon-common-extensions \
    nano \
    git \
    && rm -rf /var/lib/apt/lists/*

# ROS2 automatisch in die bashrc laden
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc

CMD ["bash"]
