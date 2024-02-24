"""
    需求：订阅发布方发布的消息，并在终端输出
    流程：
        1. 导包
        2. 初始化ROS2客户端
        3. 自定义节点类
        4. 调用spin函数，并传入节点对象
        5. 资源释放
"""
#1. 导包
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist,Point
from gazebo_msgs.srv import SpawnModel,DeleteModel,SetModelState
from gazebo_msgs.msg import ModelState
from pynput import keyboard

#3. 自定义节点类
class BallControllerNode(Node):
    def __init__(self):
        super().__init__("position_node_node_py")
        self.get_logger().info("build！(python)")
        # Create a publisher object with Twist
        self.pub_model = self.create_publisher(ModelState,'/gazebo/set_model_state',10)
        # Define the execution rate object (10Hz)
        self.rate = self.create_rate(10)
        # Create message object with a specific type
        state_msg = ModelState()

        state_msg.pose.position.x = 4.0
        state_msg.pose.position.y = 0.0
        state_msg.model_name = 'cricket_ball'
        key = 'q'
        '''
            This is the main node loop
        '''

        while rclpy.ok():
            with keyboard.Events() as events:
                event = events.get(1e6)
                if event.key == keyboard.KeyCode.from_char('s'):
                    key = 's'
                elif event.key == keyboard.KeyCode.from_char('w'):
                    key = 'w'
                elif event.key == keyboard.KeyCode.from_char('a'):
                    key = 'a'
                elif event.key == keyboard.KeyCode.from_char('d'):
                    key = 'd'

            if key == 'w':
                state_msg.pose.position.y+=0.1
            elif key =='s':
                state_msg.pose.position.y-=0.1
            elif key == 'd':
                state_msg.pose.position.x += 0.1
            elif key == 'a':
                state_msg.pose.position.x -= 0.1
            
            
            self.set_state = self.create_client(SetModelState,'/gazebo/set_model_state')
            if not self.set_state.service_is_ready():
                self.set_state.wait_for_service()
                self.get_logger().info("...connected!")
            request = SetModelState.Request(state_msg)
            future = self.set_state.call_async(request)
            rclpy.spin_until_future_complete(self.set_state,future)
            if future.result() is not None:
                print('response: %r' & future.result())
            else:
                raise RuntimeError(
            'exception while calling service: %r' % future.exception())
            self.rate.sleep()
        
            



def main():
    #2. 初始化ROS2客户端
    rclpy.init()
    #4. 调用spin函数，并传入节点对象
    BallControllerNode()
    # rclpy.spin()
    #5. 资源释放
    rclpy.shutdown()

if __name__ =='__main__':
    main()