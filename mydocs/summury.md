2022-2024 是LLM
2025-?是智能体agent

1.system_promt
系统引导(理论)：专家系统：基础理论支撑
提供总体把控，尽量使用专业知识(够强，够专业，够全面)和丰富的实战经验，结合强大的逻辑表述语言，引导大模型进行思考推理。
而且尽量避免产生幻觉等等。

2.tool-action
工具(工程)：程序员、工人：具体落实
提供具体的操作，在程序员工作软件就是编码、硬件就是操作设备(机器人难不成是具身智能)、还有其他业务场景吗？？？上课教学？
像工具有：tts，ocr、asr等等，这些小模型其实可以大模型结合起来用！！！

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

# 实战
1.for example：you neet build one agent for trip at a city base on the weather；

## first: system_promt

> 专业知识 + promt输出结构

代码：

> ```
你是一个

> ```

## second：tool
getWeather(city) -> result

getTripResult(city,weather)

> 经验及工具的使用知识


代码：



## third： 数据解构

针对tool返回结果进行数据解析，获取有用信息放入user_promt中。
比如getWeather中需要获取到天气变量。
getTripResult中需要获取到返回的搜索结果。然后进行解析。放入user_promt中。

> json+regex

代码：



## fourth: llm


## fifth: 步骤 + user_promt
针对system_promt中定义的返回数据结构。
需要进行自定义的逻辑代码限制。将

比如：对于llm的返回，需要按照自己的逻辑规则，对结果进行解析，很关键。第4步中的步骤，thought、action、observation等等key的。


# 疑问
> 1.LLM是如何可以调用本地的工具tool的
llm不是输出文字吗，本地tool getWeather是本地的一个脚本scrpt？