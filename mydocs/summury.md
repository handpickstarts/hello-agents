2022-2024 是LLM
2025-?是智能体agent

1.system_promt
系统引导(理论)：专家系统：基础理论支撑
提供总体把控，尽量使用专业知识(够强，够专业，够全面)和丰富的实战经验，结合强大的逻辑表述语言，引导大模型进行思考推理。
而且尽量避免产生幻觉等等。

2.tool-action
工具(工程)：程序员、工人：具体落实
提供具体的操作，在程序员工作软件就是编码、硬件就是操作设备(机器人难不成是具身智能)、还有其他业务场景吗？？？上课教学？

3.aim、obseration、finish
目标：总体目标与阶段目标

4.step
步骤：智能体的抽象步骤；
有多种方式，react，plan-action......


3.llm_output解析
thought
action

action-result ->context-user_promt
observation

thought
observation
action


迭代循环，知道llm知道finish 或者超过限制的maxStep阈值


4.llm选型
token？
上下文限制？