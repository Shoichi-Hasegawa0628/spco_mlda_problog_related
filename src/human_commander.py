#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Terminal経由で探索すべき物体を送信するコード

import rospy
from std_msgs.msg import String
import random


class EnterCommand():
    def __init__(self):
        self.pub = rospy.Publisher('/human_command', String, queue_size=1) ## queue size is not important for sending just one messeage.
        self.name = ["blue_cup", "green_cup", "orange_cup",
                    "penguin_doll", "pig_doll", "sheep_doll",
                    "coffee_bottle", "fruits_bottle", "muscat_bottle"]


        """
        物体の名前一覧 (Problogに依存)
        
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
        #n = random.randint(0, len(self.name)-1)           
        #TeachingText = self.name[n]
        TeachingText = "pig_doll"
        print(TeachingText)
        print('Command: ' + 'Bring ' + TeachingText + ' for me')
        while not rospy.is_shutdown():
            self.pub.publish(TeachingText)


if __name__ == '__main__':
    rospy.init_node('enter_human_command', anonymous=False)
    enter = EnterCommand()
    enter.StartPublish()
    rospy.spin()