#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SpCoSLAM-MLDAとMLDAの学習済みパラメータを用いて、
# 物体の単語から場所の単語をクロスモーダル推論するコード
import rospy
from std_msgs.msg import String
from scipy.stats import dirichlet # ディリクレ分布を使用するためのライブラリ
from scipy.stats import multinomial # カテゴリ分布と多項分布を使用するためのライブラリ (多項は複数試行)
from scipy import stats
import csv
import numpy as np
import random

with open('../data/3LDK_01_w_index_1_0.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        pass
place_name_list = row
print(place_name_list)



"""
class CrossModalObject2Place():
    def __init__(self):
        self.object_name = 0
        pass



    def word_callback(self):
        word = rospy.wait_for_message("/human_command", String, timeout=None)
        object_name = word.data
        print(object_name)
        self.object_name = object_name
        #return object_name



    #def cross_modal_object2place(self):
    
target_name = "pig"
# w_sの伝承サンプリング

# π^oのサンプリング (ディリクレ分布)                        # どの物体のトピックが出現するかの確率を表現
# (π^o)_1 ~ P( (π^o)_1 | α^o )
alpha = np.array([1.0, 1.0, 1.0])
pi_o = dirichlet.rvs(alpha, size=1, random_state=None)
#print("(pi_o)_1 : {}".format(pi_o)) 



# (C^o)_tのサンプリング式
# P((C^o)_(t,1) | (w^o)_(t,1), θ^(o,w), (π^o)_1) ∝ P( (C^o)_(t,1) | (π^o)_1 ) P( (w^o)_(t,1) | (C^o)_(t,1), θ^(o,w))
## P( (C^o)_(t,1) | (π^o)_1 ) (カテゴリ分布)
objct_topic_num = 3
object_topic = np.arange(objct_topic_num)
co_t_1_k = np.identity(objct_topic_num)
cat_co_v1 = multinomial.pmf(x = co_t_1_k, n = 1, p = pi_o)                                          #物体トピックの確率分布
co_idx_pre = stats.rv_discrete(name='co_idx_pre', values=(object_topic, cat_co_v1)).rvs(size=1)     #物体のトピック(事前)を一つサンプリング
co_idx_pre = co_idx_pre[0]
#print(co_idx_pre)


## P( (w^o)_(t,1) | (C^o)_(t,1), θ^(o,w)) (カテゴリ分布) 
# 長谷川のやり方 (確率分布同士を計算)
object_dic = 71
wo_t_1_k = np.identity(object_dic)
theta_ow_data = np.loadtxt('../data/Pdw[1].txt')
theta_ow = theta_ow_data[:, co_idx_pre]
print(theta_ow.shape[0])
theta_ow = theta_ow.T
print(theta_ow.shape[0])
cat_wo = multinomial.pmf(x = wo_t_1_k, n = 1, p = theta_ow)                                         ##対象となる物体を選択し、物体語彙の確率分布 
#co = cat_co_v1 * cat_wo                                                                             #物体のトピック(事後)の確率分布
#co_idx_pos = stats.rv_discrete(name='co_idx_pos', values=(object_topic, co)).rvs(size=1)            #C^oを一つサンプリング
#co_idx_pos = co_idx_pos[0]
#print(co_idx_pos) 

## P( (w^o)_(t,1) | (C^o)_(t,1), θ^(o,w)) (カテゴリ分布) 
# 彰先生のやり方 (先にwoを入れて、coをサンプリングする)
object_dic = 71
wo_t_1_k = np.identity(object_dic)
theta_ow_data = np.loadtxt('../data/Pdw[1].txt')
#print(theta_ow_data)
with open('../data/word_dic.txt', 'r') as f:
    obj_name_list = f.read().split("\n")
    #print(obj_name_list)
#print(obj_name_list.index(target_name))
cat_wo = theta_ow_data[obj_name_list.index(target_name), co_idx_pre]
#print(cat_wo)
co = cat_co_v1 * cat_wo
co = [float(i)/sum(co) for i in co]                                                                   #正規化
#print(co)
co_idx_pos = stats.rv_discrete(name='co_idx_pos', values=(object_topic, co)).rvs(size=1)
co_idx_pos = co_idx_pos[0]
#print(co_idx_pos)



# (C^s)_tのサンプリング
# P((C^s)_t | (C^o)_(t,1), ξ, π^s) ∝ P((C^s)_t | π^s) P((C^o)_(t,1) | (C^s)_t, ξ)
## P((C^s)_t | π^s) (カテゴリ分布)
with open('../data/3LDK_01_pi_1_0.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        pass
pi_s_data = row
#print(pi_s_data)
del pi_s_data[-1]
pi_s = np.array(pi_s_data, dtype = np.float64)
#print(pi_s)
#print(type(pi_s[0]))
place_topic_num = len(pi_s_data)
place_topic = np.arange(place_topic_num)                              
cs_k = np.identity(place_topic_num)
cat_cs = multinomial.pmf(x = cs_k, n = 1, p = pi_s)
cs_idx_pre = stats.rv_discrete(name='cs_idx_pre', values=(place_topic, cat_cs)).rvs(size=1)
cs_idx_pre = cs_idx_pre[0]
#print(cs_idx_pre)

## P((C^o)_(t,1) | (C^s)_t, ξ) (カテゴリ分布)
#place_dic = 4
#co_t_1_k_v2 = np.identity(place_dic)
xi = []
#count = 0
with open('../data/xi16.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        del row[-1]
        xi.append(np.array(row, dtype = np.float64))
        #count += 1
#print(xi[0][0])                                                     
cat_co_v2 = xi[cs_idx_pre][co_idx_pos] #ここ見直す
#print(cat_co_v2)
cs = cat_cs * cat_co_v2
cs = [float(i)/sum(cs) for i in cs]
#print(cs)  
cs_idx_pos = stats.rv_discrete(name='cs_idx_pos', values=(place_topic, cs)).rvs(size=1)
cs_idx_pos = cs_idx_pos[0]



# (w^s)_tのサンプリング
# P((w^s)_t | (C^s)_t, theta_sw) (カテゴリ分布)
place_dic = 4
ws_t_k = np.identity(place_dic)
theta_sw = []
with open('../data/3LDK_01_W_1_0.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        del row[-1]
        theta_sw.append(np.array(row, dtype = np.float64))
#print(theta_sw)
cat_ws = multinomial.pmf(x = ws_t_k, n = 1, p = theta_sw[cs_idx_pos])
#print(cat_ws)
#print(np.argmax(cat_ws))
"
a = max(cat_ws)
#print(a)
b = np.where(cat_ws==a)
#print(b)
c = b[0]
#print(c[0])
#print(len(c))
if len(c) > 1:
    #print(c[1])
    #print(c[random.randrange(len(c))])
    target_place = c[random.randrange(len(c))]
else:
    target_place = c[0]
print(target_place)                                 #目的地の場所の番号
print(cat_ws[target_place])                         #目的地の場所に対象物が存在する確率

destination = {}
# spcoの場所の名前辞書を呼び出して、indexと対応させるコマンド追記
for i in range(len(cat_ws)):
    destination[i] = cat_ws[i]
print(destination)
#return destination



if __name__ == "__main__":
    rospy.init_node('cross_modal_object2place')
    cross_modal = CrossModalObject2Place()
    cross_modal.word_callback()
    target_place = cross_modal.cross_modal_object2place()
    #rospy.spin()
"""
