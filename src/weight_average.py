#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ProbLogの確率とSpCoSLAM-MLDAの確率を重み平均してどの場所が一番高確率かを出力するコード

import rospy
import sys
sys.path.append('/root/RULO/catkin_ws/src/problog_ros/src')
#print (sys.path)
import global_knowledge
import cross_modal_object2place

class WeightAverageProbability():
    def __init__(self):
        self.logical = global_knowledge.LogicalInference()
        self.cross_modal = cross_modal_object2place.CrossModalObject2Place()
        pass


    def execute_weight_average(self):
        # Problogの呼び出し
        problog_probs = self.logical.word_callback()
        print(problog_probs)
 
        # Cross-modal Inferenceの呼び出し (cross_modal側のコードが出来次第変更)
        object_name = self.cross_modal.word_callback()
        print(object_name)


if __name__ == "__main__":
    rospy.init_node('weight_avarage')
    weight_average = WeightAverageProbability()
    weight_average.execute_weight_average()
    rospy.spin()