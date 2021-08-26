#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SpCoSLAM-MLDAとMLDAの学習済みパラメータを用いて、
# 物体の単語から場所の単語をクロスモーダル推論するコード

import rospy
from std_msgs.msg import String

class CrossModalObject2Place():
    def __init__(self):
        self.object_name = 0
        pass


    def word_callback(self):
        word = rospy.wait_for_message("/human_command", String, timeout=None)
        object_name = word.data
        print(object_name)
        self.object_name = object_name
        return object_name

    def cross_modal_name(self):
        pass



if __name__ == "__main__":
    rospy.init_node('cross_modal_object2place')
    cross_modal = CrossModalObject2Place()
    cross_modal.word_callback()
    cross_modal.cross_modal_name()
    rospy.spin()