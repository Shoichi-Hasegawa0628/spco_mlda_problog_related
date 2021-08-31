#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SpCoSLAM-MLDAとMLDAの学習済みパラメータを用いて、
# 物体の単語から場所の単語をクロスモーダル推論するコード

import rospy
from std_msgs.msg import String
from scipy.stats import dirichlet
from scipy import stats
import numpy as np

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


    def cross_modal_object2place(self):
        # w_sの伝承サンプリング

        # π^oのサンプリング (ディリクレ分布)
        # (π^o)_1 ~ P( (π^o)_1 | α^o )
        alpha = np.array([1.0])
        pi_o = dirichlet.rvs(alpha, size=1, random_state=None)
        print("(π^o)_1 : {}".format(pi_o)) 



        # (C^o)_tのサンプリング 
        # (C^o)_(t,1) ~ P( (C^o)_(t,1) | (π^o)_1 ) P( (w^o)_(t,1) | (C^o)_(t,1), θ^(o,w))
        ## P( (C^o)_(t,1) | (π^o)_1 ) (カテゴリ分布)
        obj_topic = 3
        for j in range(obj_topic):
            obj_num = np.arange(1)
            c_o_pre_1 = stats.rv_discrete(name='c_o_pre_1', values=(obj_num, pi_o))
            print(c_o_pre_1.rvs(size=1))

            ## P( (w^o)_(t,1) | (C^o)_(t,1), θ^(o,w)) (カテゴリ分布)
            obj_dic = 71
            for v in range(obj_dic):
                theta_ow = 0                                                                #編集必要 (ダミー変数) theta_ow = Theta_ow[j] (学習済みのデータから格納)
                w_o_pre = stats.rv_discrete(name='w_o_pre', values=(obj_num, theta_ow))
                print(w_o_pre.rvs(size=1))
            c_o = c_o_pre_1 * w_o_pre


            # (C^s)_tのサンプリング
            # (C^s)_t ~ P((C^s)_t | π^s) P((C^o)_(t,1) | (C^s)_t, xi)
            ## P((C^s)_t | π^s) (カテゴリ分布)
            place_topic = 4                                                                 #編集必要 (ダミー変数)
            for l in range(place_topic):
                place_num = np.arrange(4)
                pi_s = 0                                                                    #編集必要 (ダミー変数) pi_s = Pi_s[l] (学習済みのデータから格納)
                c_s_pre = stats.rv_discrete(name='c_s_pre', values=(place_num, pi_s))
                print(c_s_pre.rvs(size=1))

                ## P((C^o)_(t,1) | (C^s)_t, xi) (カテゴリ分布)
                for j in range(obj_topic):
                    xi = 0                                                                  #編集必要 (ダミー変数) xi = Xi[l] (学習済みのデータから格納)
                    c_o_pre_2 = stats.rv_discrete(name='c_o_pre_2', values=(obj_num, xi))
                    print(c_o_pre_2.rvs(size=1))
                c_s = c_s_pre * c_o_pre_2


                # (w^s)_tのサンプリング
                # (w^s)_t ~ P((w^s)_t | (C^s)_t, theta_sw) (カテゴリ分布)
                place_dic = 4
                for k in range(place_dic):
                    theta_sw = 0                                                            #編集必要 (ダミー変数) theta_sw = Theta_sw[l] (学習済みのデータから格納)
                    w_s = stats.rv_discrete(name='w_s', values=(place_num, theta_sw))
                    print(w_s.rvs(size=1))



if __name__ == "__main__":
    rospy.init_node('cross_modal_object2place')
    cross_modal = CrossModalObject2Place()
    cross_modal.word_callback()
    cross_modal.cross_modal_object2place()
    rospy.spin()