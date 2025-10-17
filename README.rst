Robot Cell Control
==================

This repository starts the robot controller for ur10e robot.

Make sure to download and install `robot_cell_description`_ package.

.. _robot_cell_description: https://github.com/pushkarkadam/robot_cell_description 

To start with actual hardware use the following::

    ros2 launch robot_cell_control start_robot.launch.py robot_ip:=0.0.0.0 use_fake_hardware:='False' use_fake_sensor:='False'

Make sure to use the correct IP address of the robot.

The default is the fake hardware which can be started as follows::

    ros2 launch robot_cell_control start_robot.launch.py