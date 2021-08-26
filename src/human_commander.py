#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Terminal経由で探索すべき物体を送信するコード

#from catkin_ws.src.problog_ros.src import global_knowledge
import rospy
from std_msgs.msg import String
import random
#import os
#import sys

#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../" + "../")
#sys.path.append('/root/RULO/catkin_ws/src/problog_ros/src')
#print (sys.path)
#import global_knowledge


class EnterCommand():
    def __init__(self):
        self.pub = rospy.Publisher('/human_command', String, queue_size=1) ## queue size is not important for sending just one messeage.
        #self.problog_code = global_knowledge.LogicalInference()
        #self._base_time = rospy.Time.now().to_sec()
        self.name = ["blue_cup", "green_cup", "orange_cup",
                    "penguin_doll", "pig_doll", "sheep_doll",
                    "coffee_bottle", "fruits_bottle", "muscat_bottle"]


        #物体の名前一覧 (Problogに依存)
        """
            cup>>>
                blue_cup
				green_cup
				orange_cup

			doll>>>
				penguin_doll
				pig_doll
				sheep_doll
			
            bottle>>>
				coffee_bottle
				fruits_bottle
				muscat_bottle
        """


    def StartPublish(self): 
        ## node initialization
        #rate = rospy.Rate(1) # 1 Hz
        n = random.randint(0, len(self.name)-1)
        #while not rospy.is_shutdown():
        #TeachingText = raw_input('Enter human command: ')               
        TeachingText = self.name[n]
        print(TeachingText)
        print('Command: ' + 'Bring ' + TeachingText + ' for me')
        #while rospy.Time.now().to_sec() - self._base_time < 10:
        while not rospy.is_shutdown():
            self.pub.publish(TeachingText)

if __name__ == '__main__':
    rospy.init_node('enter_human_command', anonymous=False)
    enter = EnterCommand()
    enter.StartPublish()
    rospy.spin()