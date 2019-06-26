# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 10:44:47 2019

@author: dddd
"""

#NaSch模型
#Author Dong Jiakuan
#Date 2019.04.20

import numpy as np
import matplotlib.pyplot as plt
import random

############################ 函数定义 #########################################
# 根据只包含车路位置和速度的一维数组转换成包含速度和位置的二维数组
def transfer(vehicle_number,road_length,vehicle_position,vehicle_velocity):
    cells_data = np.zeros((2,road_length),dtype = int)
    for i in range(vehicle_number):
        index = int(vehicle_position[i])
        cells_data[0,index] = 1
        cells_data[1,index] = vehicle_velocity[i]
    return cells_data
    
############################ 参数定义 #########################################
v_max = 5 #最大速度
road_length = 120 #道路长度
vehicle_length = 1 #车辆长度
p = 0.25 #随机慢化概率
#density = 0.3 #密度,后期可以改成一个列表，循环仿真
steps = 2000 #仿真步长
#vehicle_number = int(road_length*density) #车辆数
velocities = np.zeros(0,dtype=float)
densities = np.linspace(0.02,1,num=49,endpoint=False)
np.delete(densities,0)
for density in densities:
############################ 声明过程数据 #####################################
    velocity_avg = 0
    vehicle_number = int(road_length*density)
    vehicle_velocity = np.zeros((vehicle_number),dtype = int) #存储车辆速度
    vehicle_position = np.zeros((vehicle_number),dtype = int) #存储车辆的位置
    data = np.zeros((0,2,road_length),dtype = int) #用于存储元胞过程状态数据

######################### 初始化 ##############################################
#随机生成车辆位置，并记录到vehicle_position中，按照大小排序
    vehicle_position = np.array(random.sample(range(road_length),vehicle_number))
    vehicle_position.sort()
#赋予车辆随机初始速度
    vehicle_velocity = np.random.randint(v_max+1,size=vehicle_number)
#将初始化数据放入data中
    cells_data = transfer(vehicle_number,road_length,vehicle_position,vehicle_velocity)
    data = np.append(data,[cells_data],axis = 0)

########################## 迭代 ###############################################
    for i in range(steps):
    #第一步：加速
        vehicle_velocity = np.min(np.vstack((vehicle_velocity+1,\
                                         v_max*np.ones_like(vehicle_velocity))),axis=0)
    #第二步：减速
        dis = np.delete(vehicle_position,0)
        dis = np.append(dis,vehicle_position[0]+road_length)
        dis = dis - vehicle_position
        dis = dis - vehicle_length
        vehicle_velocity = np.min(np.vstack((vehicle_velocity,dis)),axis=0)
    # 第三步：随机慢化
        prob = np.random.random(vehicle_number)
        v_above = np.multiply(vehicle_velocity,np.array(prob>=p,dtype=int))
        v_below = np.multiply(vehicle_velocity,np.array(prob<p,dtype=int))
        v_slow = np.amax(np.vstack((v_below-1,np.zeros(vehicle_number))),axis=0)
        vehicle_velocity = v_slow + v_above
    # 第四步：位置更新
        vehicle_position = vehicle_position + vehicle_velocity
        if vehicle_position[-1] >= road_length:
            temp_pos = vehicle_position[-1] - road_length
            vehicle_position = np.delete(vehicle_position,-1,0)
            vehicle_position = np.insert(vehicle_position,0,temp_pos,0)
            temp_vel = vehicle_velocity[-1]
            vehicle_velocity = np.delete(vehicle_velocity,-1,0)
            vehicle_velocity = np.insert(vehicle_velocity,0,temp_vel,0)
        cells_data = transfer(vehicle_number,road_length,vehicle_position,vehicle_velocity)
        data = np.append(data,[cells_data],axis = 0)
####################### 计算密度、流量 ################################
    for i in range(1500,2000):
        velocity_avg += np.sum(data[i,1,:])/vehicle_number
    velocity_avg = velocity_avg/500
    velocities = np.append(velocities,velocity_avg)
    del data

############################# 画图 ################################### 
plt.plot(densities,np.multiply(densities,velocities),'*')
plt.title('Flow-Density Diagram')
plt.xlabel('Denstity')
plt.ylabel('Flow')