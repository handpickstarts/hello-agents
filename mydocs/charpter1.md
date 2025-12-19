# 智能体

## 入门

## 什么是智能体
Sensors 
Environment
auto
Actiuators
Action
Entity实体
人工智能领域，智能体被定义为任何

## 四要素

## 智能体发展
反射智能体-温度传感器
基于模型的反射智能体-自动驾驶
基于目标的智能体-GPS导航
基于效用的智能体-时间最短、路程最优的导航
学习型智能体-强化学习-下棋。alphaGo

## 大语音模型驱动新范式

## 大模型类别
1.基于内部决策架构的分类


2.基于时间和反应性的分类


~智能体设计中一个核心权衡：追求速度的反应性Reactivity和最求最优解的规划性Deliberation之间的平衡。

反应式智能体
规划式智能体
混合智能体Bybird
    分层设计。底层是快速反应模块。高层是审慎的规划模块。

3.基于知识的分类

## 智能体的构成和运行原理

### 任务环境定义
PEAS模型 来描述一个任务环境。
Performance
Environment
Actuators
Sensors


## 构建一个简单的agent
### 提示promt
目标aim
工具tools
思考与行为thoughts和action
观察observation
完成finish

### 工具


# 习题
## 1.智能体的定义 和 多维度分类智能体
区别是否是智能体有一定是"自主性"：
分类：a基于内部决策架构 b基于时间和反应性 c基于知识表示


case A 不是
case B 反应式
case C 规划式
case D 混合式

2.PEAS模型  
P:Performance ： 动态调整运动计划、运动过程中调整运动姿势、给出饮食建议
E:Environment ： 通过运动数据能得到的结果的算法或模型
A:Actuators ： 文字语音显示运动计划 或者饮食建议、语音或文字或者图像或者视频播放运动调整
S:Sensors ： 穿戴设备拿到心率、运动强度等数据

# 案列

简单的旅行助手

实现 aim-promt-thought-llm-tool-action-observetion