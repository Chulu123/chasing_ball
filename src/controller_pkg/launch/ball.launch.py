from launch import LaunchDescription
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
# 封装终端指令相关类--------------
# from launch.actions import ExecuteProcess
# from launch.substitutions import FindExecutable
# 参数声明与获取-----------------
# from launch.actions import DeclareLaunchArgument
# from launch.substitutions import LaunchConfiguration
# 文件包含相关-------------------
# from launch.actions import IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# 分组相关----------------------
# from launch_ros.actions import PushRosNamespace
# from launch.actions import GroupAction
# 事件相关----------------------
# from launch.event_handlers import OnProcessStart, OnProcessExit
# from launch.actions import ExecuteProcess, RegisterEventHandler,LogInfo
# 获取功能包下 share 目录路径-------
# from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    x = LaunchConfiguration('x', default='2.0')
    y = LaunchConfiguration('y', default='0.0')
    z = LaunchConfiguration('z', default='0.1')
    ball_controller = Node(package="controller_pkg",executable="ballcontroller",name="ballcontroll")
    spawn_ball_cmd = Node(
        package='gazebo_ros', 
        executable='spawn_entity.py',
        arguments=[ '-entity', 'demo', 
                    '-database', 'cricket_ball', 
                    '-x', x,  
                    '-y', y, 
                    '-z', z],
        output='screen')
    
    return LaunchDescription([spawn_ball_cmd,ball_controller])