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
import sys
import cv2
import numpy as np 

from geometry_msgs.msg import Twist,Point
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge,CvBridgeError 

#3. 自定义节点类
class TrackRedBall(Node):
    def __init__(self):
        super().__init__("track_red_ball_node_py")
        self.get_logger().info("build！(python)")
        self.rate = self.create_rate(10)
        self.bridge = CvBridge()
        self.publisher = self.create_publisher(Twist,'cmd_vel',10)
        # self.client = self.create_client(DriveToTarget,"command_robot")
        self.img_sub = self.create_subscription(Image,"camera/image_raw",self.process_img,10)

    # def send_request(self):
    #     request = DriveToTarget.Request()
    #     request.linear_x = float(sys.argv[1])
    #     request.angular_z = float(sys.argv[2])
    #     self.future = self.client.call_async(request)

    def process_img(self,data):
        try:
            twist = Twist()
            img = self.bridge.imgmsg_to_cv2(data,"bgr8")
            h,w,d = img.shape
    
            redLower = np.array([0,100,20]) # 红色的HSV阈值下限
            redUpper = np.array([179,255,255]) # 红色的HSV阈值上限
            hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)  # 图像从BGR颜色模型转换为HSV模型
            mask = cv2.inRange(hsv,redLower,redUpper) # 图像二值化

            gray_img = cv2.GaussianBlur(mask,(5,5),0)
            edges = cv2.Canny(gray_img,35,125)

            contours,hierachy = cv2.findContours(edges.copy(),cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)# 图像中轮廓检测

            # Calculating centroid of the circle using moment method
            M = cv2.moments(mask)

            try:
                self.cx = int(M['m10']//M['m00'])
                self.cy = int(M['m01']//M['m00'])

            # Defining the case in which m00 = 0
            except ZeroDivisionError:
                self.cx, self.cy = 0, 0

             # Drawing a circle around the object
            # and drawing centroid for visualization
            cv2.circle(img, (self.cx, self.cy), 20, (0, 100, 100), -1)
            cv2.putText(img, "centroid", (self.cx - 25, self.cy - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

            # Calculating x coordinate from center of axis
            xx = (930 - self.cx)

            # Storing intermediate xx values here
            prev_xx = 0

            # If the centroid is not visible in the image, this condition is satisfied
            if (self.cx == 0 and self.cy == 0):
                # Rotating the robot if ball is not visible in x range
                if prev_xx > 930:
                    twist.angular.z = 0.02
                    twist.linear.x = 0.0
                    self.publisher.publish(twist)
                # Rotating the robot in opposite direction if prev_xx is in the opposite
                # direction
                else:
                    twist.angular.z = -0.02
                    twist.linear.x = 0.0
                    self.publisher.publish(twist)
            # This condition is executed when centroid is visible 
            else:
                # Setting an arbitrary value less than which we move the robot towards the centroid
                if self.cy <= 700:
                    # Checking if the absolute distance is in range and then rotating 
                    # robot in a tuned angular velocity
                    if xx >= 20 and xx <= 20:
                        # Setting a proportional angular velocity
                        twist.angular.z = (0.01 * xx) * 0.02
                        twist.linear.x = 0.2
                        self.publisher.publish(twist)

                        prev_xx = xx

                    # If ball is in x range, and in front of the robot
                    # move in a straight line
                    elif xx < 20 and xx > -20:
                        twist.angular.z = 0.0
                        twist.linear.x = 0.02
                        self.publisher.publish(twist)

                        prev_xx = xx

                # This condition is satisfied if the ball is too close to the robot
                elif self.cy > 700:
                    # Stopping the robot
                    twist.angular.z = 0.0
                    twist.angular.x = 0
                    self.publisher.publish(twist)

            # Showing the live camera view from the robot in openCV window
            cv2.namedWindow('window',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('window', 500, 500)
            cv2.imshow('window', img)
            cv2.waitKey(5)

        except CvBridgeError as e:
            print(e)

def main():
    #2. 初始化ROS2客户端
    rclpy.init()
    #4. 调用spin函数，并传入节点对象
    rclpy.spin(TrackRedBall())
    #5. 资源释放
    rclpy.shutdown()

if __name__ =='__main__':
    main()